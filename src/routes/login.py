from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash, Blueprint
import bcrypt

loging_bp = Blueprint("login", __name__, url_prefix='/')

# para teste, depois remover
usuarios = {
    "teste@email.com": bcrypt.hashpw("123456".encode("utf-8"), bcrypt.gensalt())
}

@loging_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("password").encode("utf-8")

        if email in usuarios and bcrypt.checkpw(senha, usuarios[email]):
            session["usuario"] = email
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("login.dashboard"))
        else:
            flash("Email ou senha inválidos", "danger")
            return redirect(url_for("login.index"))

    return render_template("login.html")

@loging_bp.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login.index"))
    return f"Bem-vindo, {session['usuario']}!"
