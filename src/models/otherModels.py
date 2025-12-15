import math

from dataclasses import dataclass, field
from datetime import datetime

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
    id : int;
    origin : Airport;
    destination: Airport;
    plane: Plane;
    price : float;
    departure: datetime = datetime(year=1000, month=1, day=1, hour=0);
    arrival: datetime = datetime(year=1000, month=1, day=1, hour=0);
    seatsTaken : int = 0;

    def __repr__(self):
        return f"{self.plane.airport.name} -> {self.destination.name} ({self.departure:%H:%M})" if self.plane  and self.plane.airport and self.destination else "";

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


