from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from Utils.Utils import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@login_required
@dashboard_bp.route('/', methods=['GET','POST'])
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html")