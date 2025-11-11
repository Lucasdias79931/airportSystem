import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utils.Utils import Status, Privileg
from src.user.userDTO.createUserDTO import createUserDto
from src.auth.authRoute import auth_service 
from src.user.userDTO.userRepository import UserRepository

adm = createUserDto(
    cpf="62971312011",
    name="lucas dos santos dias",
    password="123",
    privilege=Privileg.Adm,
    status=Status.Ativo
)

normal = createUserDto(
    cpf="12345678909",
    name="teste",
    password="123",
    privilege=Privileg.Normal,
    status=Status.Ativo
)


seed= UserRepository()

def update():
    return;

