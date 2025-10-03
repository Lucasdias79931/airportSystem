from . import authRepository

class AuthService:
    def __init__(self):
        self.auth_repo = authRepository.authRepository()

    def findCpf(self, cpf):
        return self.auth_repo.findCpf(cpf)

    def login(self, cpf, senha):
        
        return self.auth_repo.validPassword(cpf, senha)
