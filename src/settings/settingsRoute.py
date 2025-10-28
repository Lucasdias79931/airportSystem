from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from ..models import flights 
from Utils.Utils import admin_required

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@admin_required
@settings_bp.route("/", methods=["GET", "POST"])
def settings():
    flights.loadFlights()
    
    if request.method == "POST":
        flights.lastId += 1
        newId = flights.lastId
        source = request.form.get("source")
        destination = request.form.get("destination")
        entryTime = request.form.get("entryTime")
        exitTime = request.form.get("exitTime")
        price = request.form.get("price")

        flights.flights[newId] = flights.Flight(newId, price, source, destination, entryTime, exitTime)
        flights.saveFlights()

    return render_template("setings.html", usuario=session["usuario"], flights = flights.flights)

@settings_bp.route("/flight", methods=["GET", "POST"])
def flightEdit():
    flightId = int(request.args.get("id"))

    if request.method == "POST":
        source = request.form.get("source")
        destination = request.form.get("destination")
        entryTime = request.form.get("entryTime")
        exitTime = request.form.get("exitTime")
        price = request.form.get("price")

        flights.flights[flightId] = flights.Flight(flightId, price, source, destination, entryTime, exitTime)

        return redirect(url_for("menu.menu"))

    return render_template("flights.html", flight = flights.flights[flightId])

@settings_bp.route("/delete_flight", methods=["POST"])
def deleteFlight():
    flightId = int(request.args.get("id"))
    del flights.flights[flightId]
    flights.saveFlights()
    return redirect(url_for("settings.settings"))

