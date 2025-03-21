import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file, jsonify
import xml.etree.ElementTree as ET
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.services.document_parser import extract_text_from_document
from app.services.ai_processor import process_project_overview
from app.services.ms_project import create_project_schedule
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
            
            # Create Microsoft Project schedule
            project_file_path = create_project_schedule(project_data, project_name)
            
            # Save project info
            project = Project.create(
                project_name=project_name,
                owner_id=current_user.id,
                overview_file=file_path,
                project_file=project_file_path
            )
            
            return redirect(url_for('projects.project_details', project_id=project.id))
    
    return render_template('upload.html')

@projects.route('/projects/<project_id>')
@login_required
def project_details(project_id):
    project = Project.get(project_id)
    if not project or project.owner_id != current_user.id:
        flash('Project not found')
        return redirect(url_for('main.dashboard'))
    
    # Parse the XML file
    try:
        tree = ET.parse(project.project_file)
        root = tree.getroot()
        
        # Extract tasks
        tasks = []
        task_dict = {}  # Dictionary to store tasks by ID for easier reference
        
        for task_elem in root.findall('./Tasks/Task'):
            task_id = task_elem.find('ID').text
            task = {
                'id': task_id,
                'name': task_elem.find('Name').text,
                'duration': int(task_elem.find('Duration').text.replace('d', '')),  # Convert "5d" to 5
                'predecessors': [],
                'resources': [],
                'early_start': 0,
                'early_finish': 0
            }
            
            # Get predecessors
            pred_elems = task_elem.findall('./Predecessors/Predecessor/ID')
            if pred_elems:
                task['predecessors'] = [pred.text for pred in pred_elems]
            
            # Find resources assigned to this task
            for assign_elem in root.findall(f'./Assignments/Assignment[TaskID="{task_id}"]'):
                resource_id = assign_elem.find('ResourceID').text
                resource_name = root.find(f'./Resources/Resource[ID="{resource_id}"]/Name').text
                task['resources'].append(resource_name)
            
            tasks.append(task)
            task_dict[task_id] = task
        
        # Calculate early start and early finish times (forward pass)
        for task in tasks:
            if not task['predecessors']:
                # No predecessors, start at time 0
                task['early_start'] = 0
                task['early_finish'] = task['duration']
            else:
                # Find the maximum early finish time of all predecessors
                max_pred_finish = 0
                for pred_id in task['predecessors']:
                    if pred_id in task_dict:
                        pred_finish = task_dict[pred_id]['early_finish']
                        if pred_finish > max_pred_finish:
                            max_pred_finish = pred_finish
                
                task['early_start'] = max_pred_finish
                task['early_finish'] = max_pred_finish + task['duration']
        
        # Project duration is the maximum early finish time of any task
        project_duration = max(task['early_finish'] for task in tasks) if tasks else 0
        
        # Extract resources
        resources = []
        for res_elem in root.findall('./Resources/Resource'):
            resources.append({
                'name': res_elem.find('Name').text,
                'capacity': int(res_elem.find('Capacity').text.replace('%', ''))
            })
        
        # Add tasks, resources, and calculated duration to project
        project.tasks = tasks
        project.resources = resources
        project.total_duration = project_duration
        
    except Exception as e:
        flash(f'Error parsing project file: {str(e)}')
        project.tasks = []
        project.resources = []
        project.total_duration = 0
    
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
        # Return file as an attachment
        return send_file(
            project.project_file,
            as_attachment=True,
            download_name=f"{project.project_name}.mpp",
            mimetype='application/vnd.ms-project'
        )
    except Exception as e:
        print(f"Download error: {str(e)}")
        flash(f"Error downloading file: {str(e)}")
        return redirect(url_for('projects.project_details', project_id=project_id))