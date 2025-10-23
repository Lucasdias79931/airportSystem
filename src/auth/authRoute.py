from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from .authService import AuthService


auth_bp = Blueprint("auth", __name__, url_prefix='/auth')
auth_service = AuthService() 

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ...

    return render_template("login.html")



@auth_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("auth.login"))
