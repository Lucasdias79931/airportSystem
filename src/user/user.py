from typing import Dict
from dataclasses import dataclass, field

from Utils.Utils import Status, Privilege
from src.models.flights import Flight;

@dataclass
class User:
    cpf: str
    name: str
    password: str
    flightsBookedIDS: list[Flight] = field(default_factory=list) 
    status: Status = Status.Ativo
    privilege: Privilege = Privilege.Normal
