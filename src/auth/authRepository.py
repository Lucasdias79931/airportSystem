import bcrypt
import os
import json
from dotenv import load_dotenv
from src.models.flights import Flight
from src.user.createUserDTO import createUserDto
from src.user.userRoute import user_service 
from Utils.Utils import Status, Privileg

load_dotenv()

class authRepository:
    def __init__(self):
        self.user_db = os.path.join(os.getenv("DATABASE"), "user.json")

    def login(self, cpf: str, password: str):
        user : createUserDto | None = user_service.userRepository.tree.search(int(cpf))
        if user == None: 
            return;

        if not user:
            return {'status': False, 'message': 'Usuário não existe' }
        
        stored_hash : str = user.password;

        # Verifica se há hash armazenado
        if not stored_hash:
            return {'status': False, 'message': 'Não há hashing' }


        # Verifica a senha (hash armazenado é string, precisa codificar em bytes)
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return {'status': True, 'Privileg': user.privilege.value}
        else:
            return {'status': False, 'message': 'Senha inválida' }


        return;
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

    def loadUser(self, cpf : str):
        try:
            with open(self.user_db, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None

        for u in data:
            if u.get("cpf") == cpf:
                # Handles both int `.value` and str `.name`

                status_val = u.get("status")
                privilege_val = u.get("privilege")


                status = Status(status_val) if isinstance(status_val, int) else Status[status_val]
                privilege = Privileg(privilege_val) if isinstance(privilege_val, int) else Privileg[privilege_val]

                return createUserDto(
                        cpf=u.get("cpf"),
                        password=u.get("password"),
                        name=u.get("name"),
                        flightsCreated=u.get("flightsCreated"),
                        flightsBooked=u.get("flightsBooked"),
                        flightsBookedIDS =u.get("flightsBookedContent"),
                        status=status,
                        privilege=privilege
                        )
        return None


    def saveUser(self, user: createUserDto):
        try:
            with open(self.user_db, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []

        # Convert DTO → dict
        user_dict = {
                "cpf": user.cpf,
                "password": user.password,
                "name": user.name,
                "flightsCreated": user.flightsCreated,
                "flightsBooked": user.flightsBooked,
                "flightsBookedContent": user.flightsBookedIDS,
                "status": user.status.value,
                "privilege": user.privilege.value
                }

        # Update or insert
        for i, u in enumerate(data):
            if u.get("cpf") == user.cpf:
                data[i] = user_dict  # update existing
                break
        else:
            data.append(user_dict)  # add new user

        # Save file
        with open(self.user_db, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

