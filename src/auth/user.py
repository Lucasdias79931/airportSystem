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


