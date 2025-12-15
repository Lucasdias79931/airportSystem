import math
import random

from src.models.otherModels import distance, PlaneModel, Plane, FlightSegment, Airport, Coordinate
import src.models.flights as flightModule 
from itertools import count
from typing import List, Tuple
from heapq import heappush, heappop
from datetime import datetime, timedelta
from dataclasses import dataclass, field

#Eu tenho que formalizar o que exatamente vai ser esse
#"name" que eu tô colocando como atributos de várias 
#classes. Talvez possa ser o nome da cidade apenas e 
#continuar sendo uma string

systemTime : datetime = datetime.now();
counter = count()

lastid : int = 0;

cityNames: list[str] = [
    "Rio Branco",
    "Maceió",
    "Macapá",
    "Manaus",
    "Salvador",
    "Fortaleza",
    "Brasília",
    "Vitória",
    "Goiânia",
    "São Luís",
    "Cuiabá",
    "Campo Grande",
    "Belo Horizonte",
    "Belém",
    "João Pessoa",
    "Curitiba",
    "Recife",
    "Teresina",
    "Rio de Janeiro",
    "Natal",
    "Porto Alegre",
    "Porto Velho",
    "Boa Vista",
    "Florianópolis",
    "São Paulo",
    "Aracaju",
    "Palmas",
]
@dataclass
class AirportSystem:
    airports : list[Airport] = field(default_factory=list);
    planes : list[Plane] = field(default_factory=list);

    def makeAirport(self):
        defaultPlaneModel : PlaneModel = PlaneModel();
        self.airports.append(Airport(name="Rio Branco",        coordinate=Coordinate(-9.97499, -67.8243)))
        self.airports.append(Airport(name="Maceió",            coordinate=Coordinate(-9.66599, -35.7350)))
        self.airports.append(Airport(name="Macapá",            coordinate=Coordinate(0.034934, -51.0694)))
        self.airports.append(Airport(name="Manaus",            coordinate=Coordinate(-3.39289, -57.7067)))
        self.airports.append(Airport(name="Salvador",          coordinate=Coordinate(-12.9718, -38.5011)))
        self.airports.append(Airport(name="Fortaleza",         coordinate=Coordinate(-3.71664, -38.5423)))
        self.airports.append(Airport(name="Brasília",          coordinate=Coordinate(-15.7795, -47.9297)))
        self.airports.append(Airport(name="Vitória",           coordinate=Coordinate(-20.3155, -40.3128)))
        self.airports.append(Airport(name="Goiânia",           coordinate=Coordinate(-16.6864, -49.2643)))
        self.airports.append(Airport(name="São Luís",          coordinate=Coordinate(-2.53874, -44.2825)))
        self.airports.append(Airport(name="Cuiabá",            coordinate=Coordinate(-15.6010, -56.0974)))
        self.airports.append(Airport(name="Campo Grande",      coordinate=Coordinate(-20.4486, -54.6295)))
        self.airports.append(Airport(name="Belo Horizonte",    coordinate=Coordinate(-19.9102, -43.9266)))
        self.airports.append(Airport(name="Belém",             coordinate=Coordinate(-1.4554, -48.4898)))
        self.airports.append(Airport(name="João Pessoa",       coordinate=Coordinate(-7.11509, -34.8641)))
        self.airports.append(Airport(name="Curitiba",          coordinate=Coordinate(-25.4195, -49.2646)))
        self.airports.append(Airport(name="Recife",            coordinate=Coordinate(-8.04666, -34.8771)))
        self.airports.append(Airport(name="Teresina",          coordinate=Coordinate(-5.09194, -42.8034)))
        self.airports.append(Airport(name="Rio de Janeiro",    coordinate=Coordinate(-22.9129, -43.2003)))
        self.airports.append(Airport(name="Natal",             coordinate=Coordinate(-5.79357, -35.1986)))
        self.airports.append(Airport(name="Porto Alegre",      coordinate=Coordinate(-30.0318, -51.2065)))
        self.airports.append(Airport(name="Porto Velho",       coordinate=Coordinate(-8.76077, -63.8999)))
        self.airports.append(Airport(name="Boa Vista",         coordinate=Coordinate(2.82384, -60.6753)))
        self.airports.append(Airport(name="Florianópolis",     coordinate=Coordinate(-27.5945, -48.5477)))
        self.airports.append(Airport(name="São Paulo",         coordinate=Coordinate(-23.5329, -46.6395)))
        self.airports.append(Airport(name="Aracaju",           coordinate=Coordinate(-10.9091, -37.0677)))
        self.airports.append(Airport(name="Palmas",            coordinate=Coordinate(-10.24,   -48.3558)))

        defaultPlaneModel : PlaneModel = PlaneModel();

        for airport in self.airports:
            airport.planes.append(Plane(model=defaultPlaneModel, airport=airport))

        for airport in self.airports:
            self.makeAirportRoutes(airport, 3);

        for airport in self.airports:
            for plane in airport.planes:
                self.makePlaneRoutes(plane, 1, systemTime);

        for a in self.airports:
            for b in self.airports:
                if a == b: continue;
                availableFlights = self.findShortestPath(a, b, systemTime + timedelta());
                if not availableFlights:
                    print(f"Voo possível entre {a.name} e {b.name}: ");
                    continue;

                print(f"Voo possível entre {a.name} e {b.name}: ", end="");
                for flight in availableFlights:
                    if flight.destination:
                        print(f"{flight.origin.name} -> {flight.destination.name}, ", end="");
                print("");

    def addPlane(self, airport : Airport, plane : Plane):
        self.planes.append(plane);
        airport.planes.append(plane);
        pass;

    def sortedAirportsDistances(self, a : Airport) -> list[Airport]:
        return sorted( (b for b in self.airports if b != a), key=lambda b: distance(a.coordinate, b.coordinate));

    #Essa função faz com que aeroportos perto tenham rotas para
    #aeroportos pertos.
    def makeAirportRoutes(self, airportA : Airport, n : int):
        n -= len(airportA.routes);

        sorted = self.sortedAirportsDistances(airportA);
        i : int = 0;
        for airportB in sorted:
            if not airportB in airportA.routes:
                airportA.routes.append(airportB);

            if not airportA in airportB.routes:
                airportB.routes.append(airportA);

            i += 1;
            if n < i: 
                break;

    def makePlaneRoutes(self, plane: Plane, daysForward: int, startTime : datetime):
        if plane.airport is None:
            return;

        currentAirport : Airport = plane.airport;

        speed = plane.model.speedkmh if plane.model else 800;

        limitTime = startTime + timedelta(days=daysForward);

        currentTime = startTime;

        restTime : float = 1;

        index : int = 0;
        while currentTime < limitTime:
            index+=1;
            if not currentAirport.routes:
                break;

            nextAirport : Airport = random.choice(currentAirport.routes);

            # distância e tempo
            dist : float = distance(currentAirport.coordinate, nextAirport.coordinate);
            constantDelay : float = 0.25;
            hours : float = dist / speed + constantDelay;
            travelTime : timedelta = timedelta(hours=hours);

            departure : datetime = currentTime;
            arrival : datetime = currentTime + travelTime;

            if arrival > limitTime:
                break;

            global lastid
            price : float = dist * plane.model.costKm;
            flight = FlightSegment(
                id=lastid + 1,
                origin=currentAirport,
                destination=nextAirport,
                plane=plane,
                departure=departure,
                arrival=arrival,
                price = price
            );

            lastid+=1;

            currentAirport.flights.append(flight);
            plane.flights.append(flight);

            currentAirport = nextAirport;
            currentTime = arrival + timedelta(hours=restTime);
        
        print("index: ", index);

        plane.airport = currentAirport;

    def getAirportByName(self, name : str) -> Airport | None:
        for airport in self.airports:
            if airport.name.lower() == name.lower():
                return airport;

        return None;

    def findShortestPath(self, origin: Airport, destination: Airport, start_time: datetime) -> list[FlightSegment] | None:
        # Min-heap ordered by earliest arrival time
        queue: list[tuple[datetime, int, Airport, list[FlightSegment]]] = []
        heappush(queue, (start_time, next(counter), origin, []))

        best: dict[Airport, datetime] = {origin: start_time}

        while queue:
            current_time, _, airport, path = heappop(queue)

            # Destination reached
            if airport == destination:
                return path;

            # Explore outgoing flights
            for flight in airport.flights:
                assert flight.origin == airport;
                if not flight.destination:
                    continue;
                if flight.seatsTaken >= flight.plane.model.amountOfSeats:
                    continue;

                # Must depart after we arrive
                if flight.departure < current_time:
                    continue

                arrival = flight.arrival
                next_airport = flight.destination

                # If we already found a faster way to this airport, skip
                if next_airport in best and best[next_airport] <= arrival:
                    continue

                best[next_airport] = arrival
                heappush(queue, (arrival, next(counter), next_airport, path + [flight]))

        return None

    def getShortestFlight(self, origin: Airport, destination: Airport, start_time: datetime):
        path : list[FlightSegment] | None = self.findShortestPath(origin, destination, start_time);
        if path == None: 
            return None;
        price: float = 0;
        departure: datetime = path[0].departure;
        arrival: datetime = path[0].arrival;
        for fli in path:
            price += fli.price;
            arrival += fli.arrival - arrival;
            arrival += fli.arrival - fli.departure;
        pathIds : list[int] = [];
        for fSeg in path:
            pathIds.append(fSeg.id);
        f : flightModule.Flight = flightModule.Flight(path=pathIds, departure=departure, arrival=arrival, price=price);

        return f;

import pickle

airportFile : str = "./airport";
airportSystem : AirportSystem = AirportSystem();

def saveAirportSystem() -> None:
    global airportSystem, airportFile
    with open(airportFile, "wb") as f:
        pickle.dump(airportSystem, f)

def loadAirportSystem():
    global airportSystem, airportFile
    with open(airportFile, "rb") as f:
        airportSystem = pickle.load(f)

if len(airportSystem.airports) != 0:
    saveAirportSystem();
else:
    loadAirportSystem();


import folium
from folium.plugins import PolyLineTextPath

m = folium.Map(location=[-14.2, -51.9], zoom_start=4)
start = (-23.53, -46.63)  # São Paulo
end   = (-22.91, -43.20)  # Rio
m = folium.Map(location=[-14.2, -51.9], zoom_start=4)

start = (-23.53, -46.63)  # São Paulo
end   = (-22.91, -43.20)  # Rio

line = folium.PolyLine(
    [start, end],
    weight=3
).add_to(m)

PolyLineTextPath(
    line,
    "▶",
    repeat=True,
    offset=7,
    attributes={"font-size": "14px"}
).add_to(m)

m.save("map.html")

m = folium.Map(location=[-14.2, -51.9], zoom_start=4)

for a in airportSystem.airports:
    folium.Marker(
        [a.coordinate.latitude, a.coordinate.longitude],
        popup=a.name
    ).add_to(m)

for a in airportSystem.airports:
    for f in a.flights:
        line = folium.PolyLine([
            (a.coordinate.latitude, a.coordinate.longitude),
            (f.destination.coordinate.latitude, f.destination.coordinate.longitude)
        ]).add_to(m)

        PolyLineTextPath(
            line,
            "➤",
            repeat=False,
            offset=6
        ).add_to(m)

m.save("map.html")

