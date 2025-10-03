from src.routes import login


class ConfigFlask:
    def __init__(self):
        pass
    
    @staticmethod
    def configApp(app):
        app.secret_key = " "
        app.register_blueprint(login.loging_bp)
        