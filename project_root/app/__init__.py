from flask import Flask
from flask_login import LoginManager
from config import Config
from datetime import datetime

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login_manager.init_app(app)
    
    # Add context processor to make 'now' available in all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    from app.routes.auth import auth as auth_blueprint
    from app.routes.main import main as main_blueprint
    from app.routes.projects import projects as projects_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(projects_blueprint)
    
    return app