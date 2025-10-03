from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")

@menu_bp.route("/")
def menu():
    if "usuario" not in session:
        flash("Você precisa fazer login primeiro.", "warning")
        return redirect(url_for("auth.login"))
    return render_template("Menu.html", usuario=session["usuario"])
