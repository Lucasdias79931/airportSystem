from dotenv import load_dotenv
from datetime import timedelta
from src.home.homeRoute import home_bp
from src.user.authRoute import auth_bp
from src.user.registerRoute import user_bp
from src.settings.settingsRoute import settings_bp
from src.dashboard.dashboardRoute import dashboard_bp
from src.dashboardADM.dashboardADMRoute import dashboardADM_bp
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
        app.register_blueprint(settings_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(dashboardADM_bp)
