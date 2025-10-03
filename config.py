from dotenv import load_dotenv
from datetime import timedelta
from src.auth.authRoute import auth_bp
from src.menu.menuRoute import menu_bp
from src.home.homeRoute import home_bp
import os


class ConfigFlask:
    def __init__(self):
        load_dotenv()

    @staticmethod
    def configApp(app):
        app.secret_key = os.getenv('secret_key', 'fallback-secret-key')
        app.permanent_session_lifetime = timedelta(minutes=30)
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(menu_bp)
        
