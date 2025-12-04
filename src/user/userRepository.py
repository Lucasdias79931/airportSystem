import os, json, bcrypt
from dotenv import load_dotenv
from src.user.createUserDTO import createUserDto
from src.user.database import DiskBTree

load_dotenv()

class UserRepository:
    tree : DiskBTree;

    def __init__(self):
        #self.user_db = os.path.join(os.getenv("DATABASE"), "user.json")

        self.tree = DiskBTree(path=os.getenv("DATABASE"), t=16)


    def save(self, user: createUserDto):
        user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8");
        self.tree.insert(int(user.cpf), user);

        return;
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
