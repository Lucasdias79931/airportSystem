import os, bcrypt

from flask import session
from typing import Dict

from Utils.Utils import validateCpf
from src.database.database import DiskBTree
from .user import User

class UserService:
    tree : DiskBTree;

    def __init__(self):
        self.tree = DiskBTree(path=os.getenv("DATABASE"), t=16)

    def cpfExists(self, cpf:str) -> bool:
        #cpf_numbers = re.sub(r"\D", "", cpf)
        cpf_numbers = int(cpf)

        if self.tree.search(cpf_numbers) == None:
            return False
        else:
            return True 

    def createUser(self, user: User): # Validate CPF format and checksum
        cpf_validated = validateCpf(user.cpf)
        if not cpf_validated['status']:
            raise ValueError("Invalid CPF")

        # Check duplicate
        if self.cpfExists(user.cpf):
            raise ValueError("CPF already exists in the system")

        # Use normalized CPF
        user.cpf = cpf_validated['cpf']

        # Persist user
        user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8");
        self.tree.insert(int(user.cpf), user);

        return {"message": "User created successfully!"}

    def login(self, data : Dict):
        cpf = data.get("cpf")
        password = data.get("password")

        if not cpf or not password:
            raise ValueError("CPF ou senha não preenchidos!")

        user : User | None = userService.tree.search(int(cpf))
        if not user:
            raise ValueError('Usuário não existe');
        
        storedHash : str = user.password;

        # Verifica se há hash armazenado
        if not storedHash:
            raise ValueError('Não há hashing');

        # Verifica a senha (hash armazenado é string, precisa codificar em bytes)
        if not bcrypt.checkpw(password.encode("utf-8"), storedHash.encode("utf-8")):
            raise ValueError('Senha inválida')

        session["usuario"] = cpf;
        session["privilege"] = user.privilege.value; 
        return user.privilege.value;

    def loadUser(self, cpf : str) -> User | None:
        return self.tree.search(int(cpf));

    def saveUser(self, user: User):
        self.tree.update(int(user.cpf), user);

userService = UserService();
