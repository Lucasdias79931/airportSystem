from flask import Blueprint, session, render_template, redirect, url_for
import src.models.flights as flights

home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/")
def index():
    return redirect(url_for("dashboard.dashboard"))
