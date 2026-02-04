import os
from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from datetime import datetime

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Fix for running behind Heroku's proxy (HTTPS)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Session cookie settings for HTTPS on Heroku
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True

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