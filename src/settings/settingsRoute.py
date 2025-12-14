from flask import Blueprint, request, render_template, session, redirect, url_for, flash, Response
from ..models import flights 
from Utils.Utils import admin_required
from src.user.userService import userService;

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@admin_required
@settings_bp.route("/", methods=["GET", "POST"])
def settings():
    return render_template("setings.html", usuario=session["usuario"], flights = flights.flights)


@admin_required
@settings_bp.route('/users', methods=['GET','POST'])
@settings_bp.route('/users')
def getUsers():
    order = request.args.get("order", "cpf")

    if order == "name":
        users = userService.getAllByName()
    else:
        users = userService.treeCPF.getAll()

    return render_template("usersManagement.html", users=users, order=order)

