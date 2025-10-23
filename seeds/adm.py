import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utils.Utils import Status, Privileg
from src.user.userDTO.createUserDTO import createUserDto
from src.user.userDTO.userRepository import UserRepository

adm = createUserDto(
    cpf="62971312011",
    name="Administrador",
    password="krakqp1234",
    privilege=Privileg.Adm,
    status=Status.Ativo
)


seed= UserRepository()
seed.save(adm)
