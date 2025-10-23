from Utils.Utils import Status,Privileg
import pickle
from dotenv import load_dotenv
import os


load_dotenv()

class User:
    def __init__(self, cpf, name, password, flightsCreated, flightsBooked, status, privilege):
        self.cpf = cpf
        self.name = name
        self.password = password
        self.flightsCreated = flightsCreated
        self.flightsBooked = flightsBooked
        self.status = status
        self.privilege = privilege

