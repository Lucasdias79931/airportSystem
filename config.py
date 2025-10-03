from src.auth.authRoute import auth_bp
from src.menu.menuRoute import menu_bp

class ConfigFlask:
    def __init__(self):
        pass

    @staticmethod
    def configApp(app):
        app.secret_key = "super-secret-key"  # depois troca por algo seguro
        app.register_blueprint(auth_bp)
        app.register_blueprint(menu_bp)
