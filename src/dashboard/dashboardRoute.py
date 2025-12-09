from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from Utils.Utils import login_required
import src.models.flights as flights
from src.user.authRoute import userService 
from src.user.user import User
import json

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@login_required
@dashboard_bp.route('/', methods=['GET','POST'])
def dashboard():
    cpf = session.get('usuario');

    user : User | None = userService.loadUser(cpf);
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

    temp = userService.loadUser(cpf)
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

    


