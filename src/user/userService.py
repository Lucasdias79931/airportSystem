import os, bcrypt

from flask import session
from typing import Dict

from Utils.Utils import validateCpf
from src.database.database import DiskBTree
from .user import User

class UserService:
    tree : DiskBTree;
    treeName: DiskBTree
    def __init__(self):
        base = os.getenv("DATABASE")

        self.treeCPF = DiskBTree(path=os.path.join(base, "cpf"), t=16)
        self.treeName = DiskBTree(path=os.path.join(base, "name"), t=16)

    def cpfExists(self, cpf:str) -> bool:
        #cpf_numbers = re.sub(r"\D", "", cpf)
        cpf_numbers = cpf

        if self.tree.search(cpf_numbers) == None:
            return False
        else:
            return True 
    def normalize_name(self, name: str) -> str:
        return name.strip().lower()

    def createUser(self, user: User):
        cpf_validated = validateCpf(user.cpf)
        if not cpf_validated["status"]:
            raise ValueError("Invalid CPF")

        user.cpf = cpf_validated["cpf"]

        if self.treeCPF.search(user.cpf):
            raise ValueError("CPF already exists")

        user.password = bcrypt.hashpw(
            user.password.encode(), bcrypt.gensalt()
        ).decode()

        self.treeCPF.insert(user.cpf, user)

        name_key = self.normalize_name(user.name)

        cpfs = self.treeName.search(name_key)
        if cpfs is None:
            self.treeName.insert(name_key, [user.cpf])
        else:
            cpfs.append(user.cpf)
            self.treeName.update(name_key, cpfs)
    
    def findByName(self, name: str):
        name_key = self.normalize_name(name)

        cpfs = self.treeName.search(name_key)
        if not cpfs:
            return []

        return [self.treeCPF.search(cpf) for cpf in cpfs]

    def getAllByName(self) -> list[User]:
        users = []
        name_index = self.treeName.getAll() 

        
        for cpf_list in name_index:
            
            for cpf in cpf_list:
                users.append(self.treeCPF.search(cpf))

        return users

    def getAllByCpf(self) -> list[User]:
        return self.treeCPF.getAll()

    def login(self, data : Dict):
        try:
            cpf = data.get("cpf")
            password = data.get("password")

            if not cpf or not password:
                raise ValueError("CPF ou senha não preenchidos!")

            user : User | None = self.treeCPF.search(cpf)
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

        except Exception as e:
            raise


    def findByCpf(self, cpf : str) -> User | None:
        return self.treeCPF.search(cpf);

    def saveUser(self, user: User):
        self.treeCPF.update(user.cpf, user)

        name_key = self.normalize_name(user.name)

        cpfs = self.treeName.search(name_key)
        if cpfs is None:
            self.treeName.insert(name_key, [user.cpf])
        else:
            if user.cpf not in cpfs:
                cpfs.append(user.cpf)
            self.treeName.update(name_key, cpfs)



userService = UserService()
