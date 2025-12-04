from dataclasses import dataclass, field
import os, sys
from typing import Dict
from Utils.Utils import Status, Privileg

@dataclass
class createUserDto:
    cpf: str
    name: str
    password: str
    flightsCreated: int = 0
    flightsBooked: int = 0
    flightsBookedIDS: Dict[int, int] = field(default_factory=dict) 
    status: Status = Status.Ativo
    privilege: Privileg = Privileg.Normal
