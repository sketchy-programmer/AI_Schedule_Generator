import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    MS_PROJECT_CLIENT_ID = os.environ.get('MS_PROJECT_CLIENT_ID')
    MS_PROJECT_CLIENT_SECRET = os.environ.get('MS_PROJECT_CLIENT_SECRET')