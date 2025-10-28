from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from Utils.Utils import admin_required

dashboardADM_bp = Blueprint("dashboardADM", __name__, url_prefix="/dashboardADM")


@admin_required
@dashboardADM_bp.route('/', methods=['GET','POST'])
def dashboardADM():
    if request.method == "GET":
        return render_template("dashboardADM.html")