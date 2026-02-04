import datetime
import json
from app.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    overview_file = db.Column(db.String(500))
    project_file = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    tasks_json = db.Column(db.Text, default='[]')
    resources_json = db.Column(db.Text, default='[]')

    @property
    def tasks(self):
        return json.loads(self.tasks_json or '[]')

    @tasks.setter
    def tasks(self, value):
        self.tasks_json = json.dumps(value)
        db.session.commit()

    @property
    def resources(self):
        return json.loads(self.resources_json or '[]')

    @resources.setter
    def resources(self, value):
        self.resources_json = json.dumps(value)
        db.session.commit()

    @staticmethod
    def get(project_id):
        return Project.query.get(int(project_id))

    @staticmethod
    def get_by_owner(owner_id):
        return Project.query.filter_by(owner_id=owner_id).all()

    @staticmethod
    def create(project_name, owner_id, overview_file, project_file=None):
        project = Project(
            project_name=project_name,
            owner_id=owner_id,
            overview_file=overview_file,
            project_file=project_file
        )
        db.session.add(project)
        db.session.commit()
        return project

    def add_task(self, name, duration, predecessors=None, resources=None):
        tasks = self.tasks
        task_id = len(tasks) + 1
        task = {
            'id': task_id,
            'name': name,
            'duration': duration,
            'predecessors': predecessors or [],
            'resources': resources or []
        }
        tasks.append(task)
        self.tasks_json = json.dumps(tasks)
        db.session.commit()
        return task

    def add_resource(self, name, capacity=100):
        resources = self.resources
        resource_id = len(resources) + 1
        resource = {
            'id': resource_id,
            'name': name,
            'capacity': capacity
        }
        resources.append(resource)
        self.resources_json = json.dumps(resources)
        db.session.commit()
        return resource