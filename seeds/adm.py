import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utils.Utils import Status, Privilege
from src.user.user import User 
from src.user.userService import userService

adm = User(
    cpf="62971312011",
    name="lucas dos santos dias",
    password="123",
    privilege=Privilege.Adm,
    status=Status.Ativo
)

normal = User(
    cpf="12345678909",
    name="teste",
    password="123",
    privilege=Privilege.Normal,
    status=Status.Ativo
)

try:
    userService.createUser(adm);
    userService.createUser(normal);
except:
    pass;

def update():
    return;

