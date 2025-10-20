import pickle

class User:
    #string
    cpf = None
    name = None

    #senha (apenas o hashing)
    password = None

    #lista de voos
    flightsCreated = None
    flightsBooked = None

    def __init__(self, cpf, name, password, flightsCreated, flightsBooked):
        self.cpf = cpf
        self.name = name
        self.password = password
        self.flightsCreated = flightsCreated
        self.flightsBooked = flightsBooked
        return

usersDict = {}

def saveUsers():
    with open("users.bin", "wb") as f:   # "wb" = write binary
        pickle.dump(usersDict, f)

    return

def loadUsers():
    global usersDict

    try:
        with open("users.bin", "rb") as f:   # "rb" = read binary
            usersDict = pickle.load(f)
    except FileNotFoundError:
        a = None

    return
