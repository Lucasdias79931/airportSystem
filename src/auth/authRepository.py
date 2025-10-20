import bcrypt

__all__ = ['authRepository']

# Apenas para teste
ALLUSERS = [
    {
        "cpf": "06485000551",
        "password": bcrypt.hashpw("123456".encode("utf-8"), bcrypt.gensalt())
    }
]

usersDict = {}

class authRepository:
    def __init__(self):
        pass

  
    def validPassword(self, cpf, password):
        for user in ALLUSERS:
            if user['cpf'] == cpf:
                return bcrypt.checkpw(password.encode('utf-8'), user['password'])
        return False

