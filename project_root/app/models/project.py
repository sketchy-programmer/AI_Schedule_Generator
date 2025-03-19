import uuid
import datetime

# Simple in-memory project store (replace with a database in production)
projects_db = {}

class Project:
    def __init__(self, id, project_name, owner_id, overview_file, project_file=None):
        self.id = id
        self.project_name = project_name
        self.owner_id = owner_id
        self.overview_file = overview_file
        self.project_file = project_file
        self.created_at = datetime.datetime.now()
        self.tasks = []
        self.resources = []
    
    @staticmethod
    def get(project_id):
        return projects_db.get(project_id)
    
    @staticmethod
    def get_by_owner(owner_id):
        return [p for p in projects_db.values() if p.owner_id == owner_id]
    
    @staticmethod
    def create(project_name, owner_id, overview_file, project_file=None):
        project_id = str(uuid.uuid4())
        project = Project(project_id, project_name, owner_id, overview_file, project_file)
        projects_db[project_id] = project
        return project
    
    def add_task(self, name, duration, predecessors=None, resources=None):
        task_id = len(self.tasks) + 1
        task = {
            'id': task_id,
            'name': name,
            'duration': duration,
            'predecessors': predecessors or [],
            'resources': resources or []
        }
        self.tasks.append(task)
        return task
    
    def add_resource(self, name, capacity=100):
        resource_id = len(self.resources) + 1
        resource = {
            'id': resource_id,
            'name': name,
            'capacity': capacity
        }
        self.resources.append(resource)
        return resource