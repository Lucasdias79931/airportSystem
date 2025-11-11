from flask import Blueprint, session, render_template, redirect, url_for
from seeds.adm import update

home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/")
def index():
    update();
    return render_template("home.html")
