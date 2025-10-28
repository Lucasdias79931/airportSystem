from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from .authService import AuthService
from Utils.Utils import Privileg

auth_bp = Blueprint("auth", __name__, url_prefix='/auth')
auth_service = AuthService() 

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            data = request.form.to_dict() if request.form else request.get_json()
            response = auth_service.login(data)
            
            if response == 2:
                return redirect(url_for("settings.settings"))
            
            elif response == 1:
                return redirect(url_for("dashboard.dashboard"))
            
            else:
                flash("Ocorreu um erro interno. Tente novamente mais tarde.", "danger")
                print(f"[ERRO LOGIN]: tipo response:{type(response)}, response:{response}")  
                return redirect(url_for("auth.login"))
        
        return render_template("login.html")
    except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("auth.login"))
        
    except Exception as e:
        flash("Ocorreu um erro interno. Tente novamente mais tarde.", "danger")
        print(f"[ERRO LOGIN] {e}")  
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("home.index"))
