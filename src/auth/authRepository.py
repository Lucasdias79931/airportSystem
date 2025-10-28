import bcrypt
import os
import json
from dotenv import load_dotenv

load_dotenv()

class authRepository:
    def __init__(self):
        self.user_db = os.path.join(os.getenv("DATABASE"), "user.json")

    def login(self, cpf: str, password: str):
        try:
            with open(self.user_db, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao ler o JSON: {e}")

        for user in data:
            if user.get('cpf') == cpf:
                stored_hash = user.get('password')

                # Verifica se há hash armazenado
                if not stored_hash:
                    continue

                # Verifica a senha (hash armazenado é string, precisa codificar em bytes)
                if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                    return {'status': True, 'Privileg': user.get('privilege')}

                # Senha incorreta
                return {'status': False, 'message': 'Senha inválida' }

        # CPF não encontrado
        return {'status': False, 'message': 'Usuário não encontrado'}
