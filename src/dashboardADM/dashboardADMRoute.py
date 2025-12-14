from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from Utils.Utils import admin_required
from src.user.userService import userService;

import src.models.flights as flights;


dashboardADM_bp = Blueprint("dashboardADM", __name__, url_prefix="/dashboardADM")

@admin_required
@dashboardADM_bp.route('/', methods=['GET','POST'])
def dashboardADM():
    flights.loadFlights()

    if request.method == "GET":
        return render_template("dashboardADM.html", flights = flights.flights)

@admin_required
@dashboardADM_bp.route("/flight_add", methods=["GET", "POST"])
def addFlight():
    if request.method == "POST":
        #Talvez mudar o modo de adicionar o id
        flights.lastId += 1
        print(flights.lastId);
        newId = flights.lastId
        source = request.form.get("source")
        destination = request.form.get("destination")
        entryTime = request.form.get("entryTime")
        exitTime = request.form.get("exitTime")
        price = request.form.get("price")

        flights.flights[newId] = flights.Flight(newId, price, source, destination, entryTime, exitTime)
        flights.saveFlights()

        return redirect(url_for("dashboardADM.dashboardADM"));

    return redirect(url_for("dashboardADM.dashboardADM"));

@dashboardADM_bp.route("/flight_edit", methods=["GET", "POST"])
def editFlight():
    flights.loadFlights();
    flightId = int(request.args.get("id"))

    if request.method == "POST":
        source = request.form.get("source")
        destination = request.form.get("destination")
        entryTime = request.form.get("entryTime")
        exitTime = request.form.get("exitTime")
        price = request.form.get("price")

        flights.flights[flightId] = flights.Flight(flightId, price, source, destination, entryTime, exitTime)
        flights.saveFlights();

        return redirect(url_for("dashboardADM.dashboardADM"))

    return render_template("flights.html", flight = flights.flights[flightId])

@dashboardADM_bp.route("/flight_delete", methods=["GET", "POST"])
def deleteFlight():
    flightId = int(request.args.get("id"))
    del flights.flights[flightId]
    flights.saveFlights()
    return redirect(url_for("dashboardADM.dashboardADM"))

