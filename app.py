from flask import Flask, render_template
from config import ConfigFlask
from src.menu import flights
from src.auth.user import saveUsers, loadUsers

app = Flask(__name__)
ConfigFlask.configApp(app)

@app.route("/")
def home():
    flights.loadFlights()
    loadUsers()
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

