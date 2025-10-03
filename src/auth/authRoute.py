from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from .authService import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix='/auth')
auth_service = AuthService() 

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf = request.form.get("cpf")       
        senha = request.form.get("password")  

        if auth_service.login(cpf, senha):
            session["usuario"] = cpf
            session.permanent = True
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("menu.menu"))
        else:
            flash("CPF ou senha inválidos", "danger")
            return redirect(url_for("home.index"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("home.index"))
