from . import authRepository
from flask import session

class AuthService:
    def __init__(self):
        self.auth_repo = authRepository.authRepository()

    def login(self, data: dict):
        cpf = data.get("cpf")
        password = data.get("password")

        if not cpf or not password:
            raise ValueError("CPF ou senha não preenchidos!")

        user_auth = self.auth_repo.login(cpf, password)

        if user_auth and user_auth.get("status"):
            session["usuario"] = cpf
            session["privilege"] = user_auth["Privileg"] 
            return user_auth["Privileg"]  
        else:
            raise ValueError(user_auth['message'])
