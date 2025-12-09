from flask import Flask, render_template, session
from config import ConfigFlask
import src.database.databaseTest as d;

app = Flask(__name__)
ConfigFlask.configApp(app)

@app.before_request
def refresh_session():
    if "usuario" in session:
        session.permanent = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

