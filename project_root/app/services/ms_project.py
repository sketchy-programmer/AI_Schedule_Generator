import os
import uuid
import datetime
import requests
import json
from flask import current_app
from werkzeug.utils import secure_filename
from xml.etree import ElementTree as ET

class MSProjectClient:
    """Client for Microsoft Project integration"""
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires = datetime.datetime.now()
    
    def get_access_token(self):
        """Get Microsoft Graph API access token"""
        if self.access_token and datetime.datetime.now() < self.token_expires:
            return self.access_token
            
        # Microsoft OAuth token endpoint
        token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        
        # Request body
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        # Make request
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            # Set token expiration time (subtract 5 minutes for safety)
            expires_in = token_data.get('expires_in', 3600) - 300
            self.token_expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
            return self.access_token
        else:
            raise Exception(f"Failed to get token: {response.text}")
    
    def create_project(self, project_name):
        """Create a new project in Microsoft Project"""
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Project creation endpoint
        api_url = "https://graph.microsoft.com/v1.0/me/drive/root:/Projects"
        
        # Project data
        data = {
            "name": f"{project_name}.mpp",
            "description": f"Project created by AI assistant on {datetime.datetime.now()}"
        }
        
        # Make request
        response = requests.post(f"{api_url}", headers=headers, json=data)
        if response.status_code in (200, 201):
            return response.json()
        else:
            raise Exception(f"Failed to create project: {response.text}")
    
    def add_tasks(self, project_id, tasks):
        """Add tasks to a Microsoft Project file"""
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Tasks endpoint
        api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{project_id}/tasks"
        
        results = []
        for task in tasks:
            # Task data
            task_data = {
                "name": task["name"],
                "description": task.get("description", ""),
                "duration": f"P{task['duration']}D",  # ISO 8601 duration format
            }
            
            # Add predecessors if any
            if task.get("predecessors"):
                task_data["predecessors"] = [{"id": pred_id} for pred_id in task["predecessors"]]
            
            # Make request
            response = requests.post(api_url, headers=headers, json=task_data)
            if response.status_code in (200, 201):
                results.append(response.json())
            else:
                print(f"Failed to add task: {response.text}")
        
        return results
    
    def add_resources(self, project_id, resources):
        """Add resources to a Microsoft Project file"""
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Resources endpoint
        api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{project_id}/resources"
        
        results = []
        for resource in resources:
            # Resource data
            resource_data = {
                "name": resource["name"],
                "capacity": resource.get("capacity", 100) / 100,  # Convert percentage to decimal
            }
            
            # Make request
            response = requests.post(api_url, headers=headers, json=resource_data)
            if response.status_code in (200, 201):
                results.append(response.json())
            else:
                print(f"Failed to add resource: {response.text}")
        
        return results
    
    def assign_resources(self, project_id, task_id, resource_id, units=100):
        """Assign a resource to a task"""
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Assignment endpoint
        api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{project_id}/assignments"
        
        # Assignment data
        assignment_data = {
            "taskId": task_id,
            "resourceId": resource_id,
            "percentWorkComplete": 0,
            "units": units / 100  # Convert percentage to decimal
        }
        
        # Make request
        response = requests.post(api_url, headers=headers, json=assignment_data)
        if response.status_code in (200, 201):
            return response.json()
        else:
            print(f"Failed to assign resource: {response.text}")
            return None

def create_project_schedule(project_data, project_name):
    """Create a Microsoft Project schedule from project data"""
    try:
        # Initialize MS Project client
        client = MSProjectClient(
            client_id=current_app.config['MS_PROJECT_CLIENT_ID'],
            client_secret=current_app.config['MS_PROJECT_CLIENT_SECRET']
        )
        
        # Create new project
        project = client.create_project(project_name)
        project_id = project.get("id")
        
        # Add resources
        resource_mapping = {}
        ms_resources = client.add_resources(project_id, project_data["resources"])
        for i, resource in enumerate(ms_resources):
            resource_mapping[project_data["resources"][i]["name"]] = resource["id"]
        
        # Add tasks
        task_mapping = {}
        ms_tasks = client.add_tasks(project_id, project_data["tasks"])
        for i, task in enumerate(ms_tasks):
            task_mapping[project_data["tasks"][i]["id"]] = task["id"]
        
        # Assign resources to tasks
        for i, task in enumerate(project_data["tasks"]):
            ms_task_id = task_mapping.get(task["id"])
            if not ms_task_id:
                continue
                
            for resource_name in task.get("resources", []):
                ms_resource_id = resource_mapping.get(resource_name)
                if ms_resource_id:
                    client.assign_resources(project_id, ms_task_id, ms_resource_id)
        
        # In a real application, you would download the generated .mpp file or provide a link
        # For this example, we'll just return a placeholder file path
        return f"generated/{project_name}_{uuid.uuid4()}.mpp"
        
    except Exception as e:
        print(f"Error creating MS Project schedule: {e}")
        # Fallback: Generate XML-based schedule file in MPP format
        return generate_xml_project_file(project_data, project_name)


def generate_xml_project_file(project_data, project_name):
    """Generate an XML file in Microsoft Project-compatible format"""
    # Create root element
    root = ET.Element("Project")
    
    # Add project information
    project_info = ET.SubElement(root, "ProjectInfo")
    ET.SubElement(project_info, "Name").text = project_name
    ET.SubElement(project_info, "CreationDate").text = datetime.datetime.now().isoformat()
    
    # Add tasks
    tasks = ET.SubElement(root, "Tasks")
    for task in project_data["tasks"]:
        task_elem = ET.SubElement(tasks, "Task")
        ET.SubElement(task_elem, "ID").text = str(task["id"])
        ET.SubElement(task_elem, "Name").text = task["name"]
        ET.SubElement(task_elem, "Duration").text = f"{task['duration']}d"
        
        if task.get("description"):
            ET.SubElement(task_elem, "Description").text = task["description"]
        
        if task.get("predecessors"):
            preds = ET.SubElement(task_elem, "Predecessors")
            for pred_id in task["predecessors"]:
                pred = ET.SubElement(preds, "Predecessor")
                ET.SubElement(pred, "ID").text = str(pred_id)
    
    # Add resources
    resources = ET.SubElement(root, "Resources")
    for resource in project_data["resources"]:
        res_elem = ET.SubElement(resources, "Resource")
        ET.SubElement(res_elem, "ID").text = str(resource["id"])
        ET.SubElement(res_elem, "Name").text = resource["name"]
        ET.SubElement(res_elem, "Capacity").text = str(resource["capacity"]) + "%"
    
    # Add assignments
    assignments = ET.SubElement(root, "Assignments")
    for task in project_data["tasks"]:
        for resource_name in task.get("resources", []):
            # Find resource ID by name
            resource_id = None
            for resource in project_data["resources"]:
                if resource["name"] == resource_name:
                    resource_id = resource["id"]
                    break
            
            if resource_id:
                assignment = ET.SubElement(assignments, "Assignment")
                ET.SubElement(assignment, "TaskID").text = str(task["id"])
                ET.SubElement(assignment, "ResourceID").text = str(resource_id)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(current_app.instance_path, 'generated')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the file path
    file_name = f"{project_name.replace(' ', '_')}_{uuid.uuid4()}.xml"
    file_path = os.path.join(output_dir, file_name)
    
    # Write the XML to file
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    
    return file_path