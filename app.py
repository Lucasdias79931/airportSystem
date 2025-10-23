from flask import Flask, render_template
from config import ConfigFlask

app = Flask(__name__)
ConfigFlask.configApp(app)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

