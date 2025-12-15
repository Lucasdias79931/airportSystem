import pickle
from dataclasses import dataclass
from src.models.otherModels import FlightSegment
from datetime import datetime

@dataclass 
class Flight:
    path : list[int];

    price : float;

    departure: datetime;
    arrival: datetime;

    id : int = 0;
    userId : str = "";

#local onde irá ser colocado todos os voos
#chave vai ser o id do voo e o conteúdo vai ser a struct do voo em si
flights : dict[int, Flight] = {} 

lastId : int = 1
def addFlight(flight : Flight, userCpf : str):
    global lastId;
    flight.id = lastId + 1;
    flight.userId = userCpf;
    lastId += 1;
    return flight;

def getFlightById(id : int):
    return flights[id];

def saveFlights():
    with open("flights.bin", "wb") as f:   # "wb" = write binary
        pickle.dump(flights, f)
    return

def loadFlights():
    global lastId, flights

    try:
        with open("flights.bin", "rb") as f:   # "rb" = read binary
            flights = pickle.load(f)
    except FileNotFoundError:
        print("error opening flights file.");
        flights = {}

    lastId = max(flights.keys(), default=0)

    return

