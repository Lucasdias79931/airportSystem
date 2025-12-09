from typing import Dict
from dataclasses import dataclass, field

from Utils.Utils import Status, Privilege

@dataclass
class User:
    cpf: str
    name: str
    password: str
    flightsCreated: int = 0
    flightsBooked: int = 0
    flightsBookedIDS: Dict[int, int] = field(default_factory=dict) 
    status: Status = Status.Ativo
    privilege: Privilege = Privilege.Normal
