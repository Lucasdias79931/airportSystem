import pickle

class Flight:
    #inteiros
    id = None
    price = None

    #Strings 
    source = None
    destination = None 

    #datas/tempo
    entryTime = None
    exitTime = None

    def __init__(self, id, price, source, destination, entryTime, exitTime):
        self.id = id
        self.price = price
        self.source = source
        self.destination = destination
        self.entryTime = entryTime
        self.exitTime = exitTime
        return 

#local onde irá ser colocado todos os voos
#chave vai ser o id do voo e o conteúdo vai ser a struct do voo em si
flights = {
} 

lastId = 1

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
        a = None

    lastId = len(flights)

    return

