from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
import uuid

# Simple in-memory user store (replace with a database in production)
users_db = {}

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = None
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get(user_id):
        return users_db.get(user_id)
    
    @staticmethod
    def create(username, email, password):
        user_id = str(uuid.uuid4())
        user = User(user_id, username, email)
        user.set_password(password)
        users_db[user_id] = user
        return user
    
    @staticmethod
    def get_by_email(email):
        for user in users_db.values():
            if user.email == email:
                return user
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)