import os, json, bcrypt
from dotenv import load_dotenv
from src.user.userDTO.createUserDTO import createUserDto

load_dotenv()

class UserRepository:
    def __init__(self):
        self.user_db = os.path.join(os.getenv("DATABASE"), "user.json")

    def save(self, user: createUserDto):
        os.makedirs(os.path.dirname(self.user_db), exist_ok=True)

        if os.path.exists(self.user_db):
            with open(self.user_db, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append({
            "cpf": user.cpf,
            "password": bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            "name": user.name,
            "flightsCreated": user.flightsCreated,
            "flightsBooked": user.flightsBooked,
            "status": user.status.value if hasattr(user.status, "value") else user.status,
            "privilege": user.privilege.value if hasattr(user.privilege, "value") else user.privilege
        })

        with open(self.user_db, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return {"message": "User saved successfully!"}
