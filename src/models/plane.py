import math
import random

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
class PlaneModel:
    amountOfSeats : int = 60;
    speedkmh : float = 800;
    costKm : float = 0.05;

@dataclass
class Plane:
    model : PlaneModel;
    airport : "Airport | None" = None;
    flights : list["FlightSegment"] = field(default_factory=list);

#Valores negativos para o sul e positivos para o norte
#Valores negativos para o oeste e positivos para o leste
@dataclass
class Coordinate:
    latitude : float = 0;
    longitude : float = 0;

#Cidade
@dataclass(eq=False)
class Airport:
    name : str = "Cidade";
    routes : list["Airport"] = field(default_factory=list);
    flights : list["FlightSegment"] = field(default_factory=list);
    planes : list[Plane] = field(default_factory=list);
    coordinate : Coordinate = field(default_factory=Coordinate);

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Airport({self.name})"

@dataclass
class FlightSegment:
    origin : Airport;
    destination: Airport;
    plane: Plane;
    price : float;
    departure: datetime = datetime(year=1000, month=1, day=1, hour=0);
    arrival: datetime = datetime(year=1000, month=1, day=1, hour=0);
    seatsTaken : int = 0;

    def __repr__(self):
        return f"{self.plane.airport.name} -> {self.destination.name} ({self.departure:%H:%M})" if self.plane  and self.plane.airport and self.destination else "";

@dataclass 
class Flight:
    path : list[FlightSegment];

    price : float;

    departure: datetime;
    arrival: datetime;


def distance(a: Coordinate, b: Coordinate) -> float:
    R = 6371.0

    lat1 = math.radians(a.latitude)
    lon1 = math.radians(a.longitude)
    lat2 = math.radians(b.latitude)
    lon2 = math.radians(b.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))

    return R * c


@dataclass
class AirportSystem:
    airports : list[Airport] = field(default_factory=list);
    planes : list[Plane] = field(default_factory=list);

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

            price : float = dist * plane.model.costKm;
            flight = FlightSegment(
                origin=currentAirport,
                destination=nextAirport,
                plane=plane,
                departure=departure,
                arrival=arrival,
                price = price
            );

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
        flights : list[FlightSegment] | None = self.findShortestPath(origin, destination, start_time);
        if flights == None: 
            return None;
        price: float = 0;
        departure: datetime = flights[0].departure;
        arrival: datetime = flights[0].arrival;
        for f in flights:
            price += f.price;
            arrival += f.arrival - arrival;
            arrival += f.arrival - f.departure;
        flight : Flight = Flight(path = flights, price=price, departure=departure, arrival=arrival);

        return flight;


airportSystem : AirportSystem = AirportSystem();

airportSystem.airports.append(Airport(name="Rio Branco",        coordinate=Coordinate(-9.97499, -67.8243)))
airportSystem.airports.append(Airport(name="Maceió",            coordinate=Coordinate(-9.66599, -35.7350)))
airportSystem.airports.append(Airport(name="Macapá",            coordinate=Coordinate(0.034934, -51.0694)))
airportSystem.airports.append(Airport(name="Manaus",            coordinate=Coordinate(-3.39289, -57.7067)))
airportSystem.airports.append(Airport(name="Salvador",          coordinate=Coordinate(-12.9718, -38.5011)))
airportSystem.airports.append(Airport(name="Fortaleza",         coordinate=Coordinate(-3.71664, -38.5423)))
airportSystem.airports.append(Airport(name="Brasília",          coordinate=Coordinate(-15.7795, -47.9297)))
airportSystem.airports.append(Airport(name="Vitória",           coordinate=Coordinate(-20.3155, -40.3128)))
airportSystem.airports.append(Airport(name="Goiânia",           coordinate=Coordinate(-16.6864, -49.2643)))
airportSystem.airports.append(Airport(name="São Luís",          coordinate=Coordinate(-2.53874, -44.2825)))
airportSystem.airports.append(Airport(name="Cuiabá",            coordinate=Coordinate(-15.6010, -56.0974)))
airportSystem.airports.append(Airport(name="Campo Grande",      coordinate=Coordinate(-20.4486, -54.6295)))
airportSystem.airports.append(Airport(name="Belo Horizonte",    coordinate=Coordinate(-19.9102, -43.9266)))
airportSystem.airports.append(Airport(name="Belém",             coordinate=Coordinate(-1.4554, -48.4898)))
airportSystem.airports.append(Airport(name="João Pessoa",       coordinate=Coordinate(-7.11509, -34.8641)))
airportSystem.airports.append(Airport(name="Curitiba",          coordinate=Coordinate(-25.4195, -49.2646)))
airportSystem.airports.append(Airport(name="Recife",            coordinate=Coordinate(-8.04666, -34.8771)))
airportSystem.airports.append(Airport(name="Teresina",          coordinate=Coordinate(-5.09194, -42.8034)))
airportSystem.airports.append(Airport(name="Rio de Janeiro",    coordinate=Coordinate(-22.9129, -43.2003)))
airportSystem.airports.append(Airport(name="Natal",             coordinate=Coordinate(-5.79357, -35.1986)))
airportSystem.airports.append(Airport(name="Porto Alegre",      coordinate=Coordinate(-30.0318, -51.2065)))
airportSystem.airports.append(Airport(name="Porto Velho",       coordinate=Coordinate(-8.76077, -63.8999)))
airportSystem.airports.append(Airport(name="Boa Vista",         coordinate=Coordinate(2.82384, -60.6753)))
airportSystem.airports.append(Airport(name="Florianópolis",     coordinate=Coordinate(-27.5945, -48.5477)))
airportSystem.airports.append(Airport(name="São Paulo",         coordinate=Coordinate(-23.5329, -46.6395)))
airportSystem.airports.append(Airport(name="Aracaju",           coordinate=Coordinate(-10.9091, -37.0677)))
airportSystem.airports.append(Airport(name="Palmas",            coordinate=Coordinate(-10.24,   -48.3558)))

defaultPlaneModel : PlaneModel = PlaneModel();

for airport in airportSystem.airports:
    airport.planes.append(Plane(model=defaultPlaneModel, airport=airport))

for airport in airportSystem.airports:
    airportSystem.makeAirportRoutes(airport, 3);

for airport in airportSystem.airports:
    for plane in airport.planes:
        airportSystem.makePlaneRoutes(plane, 1, systemTime);

for a in airportSystem.airports:
    for b in airportSystem.airports:
        if a == b: continue;
        availableFlights = airportSystem.findShortestPath(a, b, systemTime + timedelta());
        if not availableFlights:
            print(f"Voo possível entre {a.name} e {b.name}: ");
            continue;

        print(f"Voo possível entre {a.name} e {b.name}: ", end="");
        for flight in availableFlights:
            if flight.destination:
                print(f"{flight.origin.name} -> {flight.destination.name}, ", end="");
        print("");


import folium
from folium.plugins import PolyLineTextPath

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


