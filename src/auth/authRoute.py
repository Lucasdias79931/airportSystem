from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from .authService import AuthService
from .authRepository import usersDict 
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix='/auth')
auth_service = AuthService() 

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf = request.form.get("cpf")       
        senha = request.form.get("password")  

        if cpf in usersDict and bcrypt.checkpw(senha.encode('utf-8'), usersDict[cpf]):
            session["usuario"] = cpf
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("menu.menu"))
        else:
            flash("CPF ou senha inválidos", "danger")
            #retornando nada ao invés de redirecionar pra a mesma página pra não ter que renderizar a página denovo toda vez
            return ('', 204)

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        cpf   = request.form.get("cpf")       
        senha = request.form.get("password")  

        if cpf not in usersDict:
            usersDict[cpf] = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
            session["usuario"] = cpf
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("menu.menu"))
        else:
            flash("Já há um usuário como esse cpf", "danger")
            #retornando nada ao invés de redirecionar pra a mesma página pra não ter que renderizar a página denovo toda vez
            return ('', 204)

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("auth.login"))
