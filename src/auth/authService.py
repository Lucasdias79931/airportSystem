from . import authRepository
class AuthService:
    def __init__(self):
        self.auth_repo = authRepository.authRepository()


    def login(self, cpf, senha):
        return self.auth_repo.validPassword(cpf, senha)
