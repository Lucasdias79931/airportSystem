from dataclasses import dataclass
import os, sys
from Utils.Utils import Status, Privileg

@dataclass
class createUserDto:
    cpf: str
    name: str
    password: str
    flightsCreated: int = 0
    flightsBooked: int = 0
    status: Status = Status.Ativo
    privilege: Privileg = Privileg.Normal
