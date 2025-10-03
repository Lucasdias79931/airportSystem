from dataclasses import dataclass
import bcrypt

@dataclass
class CreateUserDto:
    NAME: str
    CPF: str
    AGE: int
    PASSWORD: str
    EMAIL: str


class UserRepository:
    def __init__(self, user_dbPath):
        self.csv_file = user_dbPath
        self.lock_file = self.csv_file + ".lock"

        
    def create(self, user: CreateUserDto):
        # valida se CPF já existe
        if any(u['CPF'] == user.CPF for u in self.user_db):
            raise ValueError("CPF já cadastrado")

        # valida campos obrigatórios
        for field in user.__dataclass_fields__:
            value = getattr(user, field)
            if value is None or value == "":
                raise ValueError(f"Campo obrigatório ausente: {field}")