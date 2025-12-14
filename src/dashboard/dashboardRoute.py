import src.models.flights as flights
import json

from flask import Blueprint, request, render_template, session, redirect, url_for, flash, Flask
from Utils.Utils import login_required
from src.user.authRoute import userService 
from src.user.user import User
from datetime import datetime
from src.models.plane import airportSystem;

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@login_required
@dashboard_bp.route('/i', methods=['GET','POST'])
def dashboardi():
    cpf = session.get('usuario');

    user : User | None = userService.findByCpf(cpf);
    if(user == None):
        return render_template("dashboard.html", flights = flights.flights, bookedFlights = None);

    flights.loadFlights();
    print("Viagens compradas pelo usuário: ", user.flightsBookedIDS);
    if request.method == "GET":
        return render_template("dashboard.html", flights = flights.flights, bookedFlights = user.flightsBookedIDS);


@login_required
@dashboard_bp.route('/book_flight', methods=['GET','POST'])
def bookFlight():
    cpf = session.get('usuario');
    flightId = int(request.args.get("id"));

    flights.loadFlights();
    flight = flights.flights[flightId];
    if flight == None:
        return redirect(url_for("dashboard.dashboard"));

    temp = userService.findByCpf(cpf)
    if( temp == None):
        return redirect(url_for("dashboard.dashboard"));

    user : User = temp; 
    if(user.flightsBookedIDS == None):
        user.flightsBookedIDS = {}

    if(flightId in user.flightsBookedIDS):
        return redirect(url_for("dashboard.dashboard"));


    user.flightsBookedIDS[flightId] = flightId;
    userService.saveUser(user);

    return redirect(url_for("dashboard.dashboard"));


@dashboard_bp.route("/", methods=['GET', 'POST'])
def dashboard():
    airports = [a.name for a in airportSystem.airports]
    path = None
    error = None

    if request.method == "POST":
        try:
            origin_name = request.form["origin"]
            dest_name = request.form["destination"]
            departure = datetime.fromisoformat(request.form["departure"])

            origin = airportSystem.getAirportByName(origin_name)
            dest = airportSystem.getAirportByName(dest_name)

            if not origin or not dest:
                error = "Invalid airport name."
            else:
                path = airportSystem.getShortestFlight(
                    origin, dest, departure
                )
                if not path:
                    error = "No available route for the selected time."

        except Exception as e:
            error = "Invalid search parameters."

    return render_template(
        "dashboard_cool.html",
        airports=airports,
        path=path,
        error=error
    )

