from .database import DiskBTree
from dataclasses import field
from dataclasses import dataclass 
from src.user.userService import userService 
from src.user.user import User

from typing import Dict
import random 

def main():
    userServ : userService = userService();
    names = [
    "Adriano Costa",
    "Bianca Ribeiro",
    "Carla Mendes",
    "Daniel Faria",
    "Elisa Nogueira",
    "Felipe Duarte",
    "Gabriel Soares",
    "Helena Silveira",
    "Isabela Cruz",
    "Javier Martins",
    "Karla Benevides",
    "Lucas Moretti",
    "Marina Almeida",
    "Nicolas Cardoso",
    "Olívia Ramos"
    ]

    user = User(
        cpf = "12345678909",
        name= names[random.randint(0, len(names) - 1)],
        password="123"
    );


    print(userServ.userRepository.tree.search(int(user.cpf)))
    return;

    for i in range(1, 10):
        names = [
        "Adriano Costa",
        "Bianca Ribeiro",
        "Carla Mendes",
        "Daniel Faria",
        "Elisa Nogueira",
        "Felipe Duarte",
        "Gabriel Soares",
        "Helena Silveira",
        "Isabela Cruz",
        "Javier Martins",
        "Karla Benevides",
        "Lucas Moretti",
        "Marina Almeida",
        "Nicolas Cardoso",
        "Olívia Ramos"
        ]

        user = User(
            cpf = f"{i}",
            name= names[random.randint(0, len(names) - 1)],
            password="123"
        );

        tree.insert(user.cpf, user);

        found = tree.search(f"{i}");

        print(found);


