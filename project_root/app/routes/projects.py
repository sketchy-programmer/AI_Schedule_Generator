import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.services.document_parser import extract_text_from_document
from app.services.ai_processor import process_project_overview
from app.services.spreadsheet_export import create_project_schedule
from app.models.project import Project

projects = Blueprint('projects', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@projects.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_project():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            project_name = request.form.get('project_name', 'Untitled Project')
            
            # Create upload folder if it doesn't exist
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text from document
            document_text = extract_text_from_document(file_path)
            
            # Process with AI
            project_data = process_project_overview(document_text)
            
            # Create spreadsheet schedule
            project_file_path = create_project_schedule(project_data, project_name)

            # Save project info
            project = Project.create(
                project_name=project_name,
                owner_id=current_user.id,
                overview_file=file_path,
                project_file=project_file_path
            )

            # Store tasks and resources directly in the project model
            project.tasks = project_data.get("tasks", [])
            project.resources = project_data.get("resources", [])

            return redirect(url_for('projects.project_details', project_id=project.id))
    
    return render_template('upload.html')

@projects.route('/projects/<project_id>')
@login_required
def project_details(project_id):
    project = Project.get(project_id)
    if not project or project.owner_id != current_user.id:
        flash('Project not found')
        return redirect(url_for('main.dashboard'))

    # Calculate schedule from stored tasks
    tasks = project.tasks or []
    task_dict = {task['id']: task for task in tasks}

    # Calculate early start and early finish times (forward pass)
    for task in tasks:
        if not task.get('predecessors'):
            task['early_start'] = 0
            task['early_finish'] = task['duration']
        else:
            max_pred_finish = 0
            for pred_id in task['predecessors']:
                if pred_id in task_dict:
                    pred_finish = task_dict[pred_id].get('early_finish', 0)
                    if pred_finish > max_pred_finish:
                        max_pred_finish = pred_finish
            task['early_start'] = max_pred_finish
            task['early_finish'] = max_pred_finish + task['duration']

    # Project duration is the maximum early finish time of any task
    project.total_duration = max((task.get('early_finish', 0) for task in tasks), default=0)

    return render_template('project_details.html', project=project)

@projects.route('/projects/<project_id>/download')
@login_required
def download_project_file(project_id):
    project = Project.get(project_id)
    if not project or project.owner_id != current_user.id:
        flash('Project not found')
        return redirect(url_for('main.dashboard'))
    
    # Check if project file path exists
    if not project.project_file or not os.path.exists(project.project_file):
        flash('Project file not found')
        return redirect(url_for('projects.project_details', project_id=project_id))
    
    try:
        # Determine file type and mimetype
        if project.project_file.endswith('.xlsx'):
            download_name = f"{project.project_name}.xlsx"
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif project.project_file.endswith('.csv'):
            download_name = f"{project.project_name}.csv"
            mimetype = 'text/csv'
        else:
            download_name = f"{project.project_name}.xlsx"
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        # Return file as an attachment
        return send_file(
            project.project_file,
            as_attachment=True,
            download_name=download_name,
            mimetype=mimetype
        )
    except Exception as e:
        print(f"Download error: {str(e)}")
        flash(f"Error downloading file: {str(e)}")
        return redirect(url_for('projects.project_details', project_id=project_id))