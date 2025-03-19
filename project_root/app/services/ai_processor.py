import os
import json
import openai
from flask import current_app

class ProjectTask:
    def __init__(self, name, duration, description=None, predecessors=None, resources=None):
        self.name = name
        self.duration = duration  # in days
        self.description = description
        self.predecessors = predecessors or []
        self.resources = resources or []

class ProjectResource:
    def __init__(self, name, role=None, capacity=100):
        self.name = name
        self.role = role
        self.capacity = capacity  # percentage

def process_project_overview(document_text):
    """Process project overview with OpenAI and extract structured project data"""
    openai.api_key = current_app.config['OPENAI_API_KEY']
    
    # Prepare the system prompt
    system_prompt = """
    You are a professional project manager assistant that helps plan projects. 
    Your task is to analyze a project overview and identify:
    1. Main project tasks and subtasks
    2. Dependencies between tasks
    3. Estimated duration for each task (in days)
    4. Required resources for each task
    5. A logical project schedule
    
    Return the results in the following JSON format:
    {
        "project_name": "Project name extracted from the overview",
        "tasks": [
            {
                "id": 1,
                "name": "Task name",
                "description": "Task description",
                "duration": 5,
                "predecessors": [task_ids],
                "resources": ["Resource names"]
            }
        ],
        "resources": [
            {
                "id": 1,
                "name": "Resource name",
                "role": "Resource role",
                "capacity": 100
            }
        ]
    }
    """
    
    # Prepare user message
    user_message = f"Here's a project overview. Please analyze it and create a project schedule:\n\n{document_text}"
    
    # Call OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    
    # Parse the response
    try:
        response_content = response.choices[0].message.content
        # Find the JSON part (in case there's explanatory text)
        json_start = response_content.find('{')
        json_end = response_content.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_content = response_content[json_start:json_end]
            project_data = json.loads(json_content)
            return project_data
        else:
            # Fallback if JSON is not found
            return process_unstructured_response(response_content)
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return create_default_project()
        
def process_unstructured_response(response_text):
    """Process unstructured text response from OpenAI"""
    # Create a basic project structure with any information we can extract
    project_data = {
        "project_name": "Extracted Project",
        "tasks": [],
        "resources": []
    }
    
    # Very basic parsing - in a real system, you'd want more robust parsing
    lines = response_text.split('\n')
    current_task_id = 1
    current_resource_id = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Very simplistic task detection
        if "task" in line.lower() and ":" in line:
            parts = line.split(":", 1)
            task_name = parts[0].replace("Task", "").strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            
            # Try to extract duration if mentioned
            duration = 5  # default
            if "day" in description.lower():
                for word in description.split():
                    if word.isdigit():
                        duration = int(word)
                        break
            
            project_data["tasks"].append({
                "id": current_task_id,
                "name": task_name,
                "description": description,
                "duration": duration,
                "predecessors": [],
                "resources": []
            })
            current_task_id += 1
            
        # Very simplistic resource detection
        elif "resource" in line.lower() and ":" in line:
            parts = line.split(":", 1)
            resource_name = parts[0].replace("Resource", "").strip()
            role = parts[1].strip() if len(parts) > 1 else ""
            
            project_data["resources"].append({
                "id": current_resource_id,
                "name": resource_name,
                "role": role,
                "capacity": 100
            })
            current_resource_id += 1
    
    # If we couldn't extract anything, create a default structure
    if not project_data["tasks"]:
        return create_default_project()
    
    return project_data

def create_default_project():
    """Create a default project structure if parsing fails"""
    return {
        "project_name": "New Project",
        "tasks": [
            {
                "id": 1,
                "name": "Planning",
                "description": "Initial project planning",
                "duration": 5,
                "predecessors": [],
                "resources": ["Project Manager"]
            },
            {
                "id": 2,
                "name": "Development",
                "description": "Main development phase",
                "duration": 20,
                "predecessors": [1],
                "resources": ["Developer"]
            },
            {
                "id": 3,
                "name": "Testing",
                "description": "Quality assurance and testing",
                "duration": 10,
                "predecessors": [2],
                "resources": ["QA Engineer"]
            },
            {
                "id": 4,
                "name": "Deployment",
                "description": "Project deployment",
                "duration": 2,
                "predecessors": [3],
                "resources": ["DevOps Engineer", "Project Manager"]
            }
        ],
        "resources": [
            {
                "id": 1,
                "name": "Project Manager",
                "role": "Management",
                "capacity": 100
            },
            {
                "id": 2,
                "name": "Developer",
                "role": "Development",
                "capacity": 100
            },
            {
                "id": 3,
                "name": "QA Engineer",
                "role": "Quality Assurance",
                "capacity": 100
            },
            {
                "id": 4,
                "name": "DevOps Engineer",
                "role": "Operations",
                "capacity": 50
            }
        ]
    }