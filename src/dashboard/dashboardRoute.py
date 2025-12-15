import src.models.flights as flights
import json

from flask import Blueprint, request, render_template, session, redirect, url_for, flash, Flask
from Utils.Utils import login_required
from src.user.authRoute import userService 
from src.user.user import User
from datetime import datetime
from src.models.plane import airportSystem;
import src.models.flights as flightModule;

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

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
        "dashboard.html",
        airports=airports,
        path=path,
        error=error
    )


@dashboard_bp.route("/book", methods=["POST"])
def book_flight():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cpf = session["usuario"]
    user = userService.findByCpf(cpf);

    # data coming from hidden form fields
    path_ids = request.form.getlist("path_ids")
    price = float(request.form["price"])
    departure = datetime.fromisoformat(request.form["departure"])
    arrival = datetime.fromisoformat(request.form["arrival"])

    flight = flightModule.Flight(
        path=[int(i) for i in path_ids],
        price=price,
        departure=departure,
        arrival=arrival
    )

    booking = flightModule.addFlight(userCpf=user.cpf, flight=flight)

    return redirect(url_for("dashboard.confirmation"))
