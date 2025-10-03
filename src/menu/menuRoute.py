from flask import Blueprint, render_template
from Utils import login_required

menu_bp = Blueprint("menu", __name__, url_prefix="/menu") 
@menu_bp.route("/", methods=['GET'])
@login_required
def menu():
    return render_template("Menu.html")
