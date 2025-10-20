from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from . import flights 

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")

@menu_bp.route("/", methods=["GET", "POST"])
def menu():
    if "usuario" not in session:
        flash("Você precisa fazer login primeiro.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        flights.lastId += 1
        newId = flights.lastId
        source = request.form.get("source")
        destination = request.form.get("destination")
        entryTime = request.form.get("entryTime")
        exitTime = request.form.get("exitTime")
        price = request.form.get("price")


        flights.flights[newId] = flights.Flight(newId, price, source, destination, entryTime, exitTime)

    return render_template("Menu.html", usuario=session["usuario"], flights = flights.flights)
