from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
import bcrypt
from config import ConfigFlask

app = Flask(__name__)
ConfigFlask.configApp(app)

usuarios = {
    "teste@email.com": bcrypt.hashpw("123456".encode("utf-8"), bcrypt.gensalt())
}

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    senha = request.form.get("password").encode("utf-8")

    if email in usuarios and bcrypt.checkpw(senha, usuarios[email]):
        session["usuario"] = email
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Email ou senha inválidos", "danger")
        return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("index"))
    return f"Bem-vindo, {session['usuario']}!"
    
if __name__ == "__main__":
    app.run(debug=True)
