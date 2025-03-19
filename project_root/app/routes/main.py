from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.project import Project  # Import the correct Project model
import xml.etree.ElementTree as ET

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Get the projects here, not in the template
    projects = Project.get_by_owner(current_user.id)
    return render_template('dashboard.html', projects=projects)

def parse_project_xml(xml_string):
    """Parse XML string into a project object structure"""
    root = ET.fromstring(xml_string)
    
    project = {
        'project_name': root.find('./ProjectInfo/Name').text,
        'created_at': root.find('./ProjectInfo/CreationDate').text,
        'tasks': [],
        'resources': [],
        'project_file': '#'  # You might want to set this to the actual file path
    }
    
    # Parse tasks
    for task_elem in root.findall('./Tasks/Task'):
        task = {
            'id': task_elem.find('ID').text,
            'name': task_elem.find('Name').text,
            'duration': int(task_elem.find('Duration').text.rstrip('d')),
            'predecessors': [pred.find('ID').text for pred in task_elem.findall('./Predecessors/Predecessor')],
            'resources': []  # Will be populated from assignments
        }
        project['tasks'].append(task)
    
    # Parse resources
    for res_elem in root.findall('./Resources/Resource'):
        resource = {
            'id': res_elem.find('ID').text,
            'name': res_elem.find('Name').text,
            'capacity': res_elem.find('Capacity').text
        }
        project['resources'].append(resource)
    
    # Parse assignments and link resources to tasks
    for assign_elem in root.findall('./Assignments/Assignment'):
        task_id = assign_elem.find('TaskID').text
        resource_id = assign_elem.find('ResourceID').text
        
        # Find the resource name
        resource_name = next((r['name'] for r in project['resources'] if r['id'] == resource_id), None)
        
        # Find the task and add the resource
        for task in project['tasks']:
            if task['id'] == task_id and resource_name:
                task['resources'].append(resource_name)
    
    return project

def get_project_xml(project_id):
    """Retrieve the XML data for a project"""
    # This implementation depends on how you're storing the XML data
    # You might be storing it in a database, a file, or elsewhere
    # For example, if it's in your Project model:
    project = Project.query.get(project_id)
    if project:
        return project.xml_data
    return None

@main.route('/project/<project_id>')
@login_required  # Add this if you want to restrict access to logged-in users
def project_details(project_id):
    # Get the XML data from wherever you're storing it
    xml_data = get_project_xml(project_id)
    
    if not xml_data:
        # Handle the case where the project doesn't exist or has no XML data
        return render_template('error.html', message="Project not found or has no data")
    
    # Parse the XML into a project object
    project = parse_project_xml(xml_data)
    
    # Pass the project object to the template
    return render_template('project_details.html', project=project)