import src.models.flights as flights
import json

import traceback
from flask import Blueprint, request, render_template, session, redirect, url_for, flash, Flask
from Utils.Utils import login_required
from src.user.authRoute import userService 
from src.user.user import User
from datetime import datetime, date
from src.models.plane import airportSystem;
import src.models.flights as flightModule;
from src.models.otherModels import FlightSegment;


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=['GET', 'POST'])
def dashboard():
    airports = [a.name for a in airportSystem.airports]
    path = None
    bought = False;
    legs : list[FlightSegment] = []
    error = None
        
    if request.method == "POST":
        try:
            origin_name = request.form["origin"]
            dest_name = request.form["destination"]
            d = date.fromisoformat(request.form["departure"])
            departure = datetime.combine(d, datetime.min.time())


            origin = airportSystem.getAirportByName(origin_name)
            dest = airportSystem.getAirportByName(dest_name)

            if not origin or not dest:
                error = "Nome de aeroporto inválido."
            else:
                path : flightModule.Flight | None = airportSystem.getShortestFlight(
                    origin, dest, departure
                )

                if not path:
                    error = "Não há rota."
                else:
                    for leg in path.path:
                        newLeg = airportSystem.getFlightById(leg);
                        if not newLeg:
                            continue;
                        legs.append(newLeg);
                    user = userService.findByCpf(session["usuario"]);
                    print(user);

                    if user and user.flightsBookedIDS:
                        bought = False 
                        for f in user.flightsBookedIDS:
                            if f.path == path.path:
                                bought = True;
                                break;

                        print ("user flights: ", user.flightsBookedIDS);
                        print ("path flights: ", path.path);

        except Exception as e:
            traceback.print_exc()
            error = "Invalid search parameters."

    return render_template(
        "dashboard.html",
        airports=airports,
        path=path,
        error=error,
        legs=legs,
        bought=bought
    )


@dashboard_bp.route("/book", methods=["POST"])
def book_flight():
    cpf = session["usuario"]
    user = userService.findByCpf(cpf);
    if not user:
        return redirect(url_for("dashboard.dashboard"))

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

    for pathId in flight.path:
        tempFlight = airportSystem.getFlightById(pathId);

        if not tempFlight: continue;

        print(tempFlight.seatsTaken);
        assert tempFlight.getSeat();

    booking = flightModule.addFlight(userCpf=user.cpf, flight=flight)
    user.flightsBookedIDS.append(booking);
    userService.saveUser(user);

    return redirect(url_for("dashboard.dashboard"))
