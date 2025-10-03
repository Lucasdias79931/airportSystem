from flask import Flask
from config import ConfigFlask

app = Flask(__name__)
ConfigFlask.configApp(app)



if __name__ == "__main__":
    app.run(debug=True)
