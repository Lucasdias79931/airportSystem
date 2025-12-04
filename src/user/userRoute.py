from flask import Blueprint, request, render_template, redirect, url_for, flash
from .userService import user_service
from .createUserDTO import createUserDto
from Utils.Utils import Status, Privileg

user_bp = Blueprint("user", __name__, url_prefix='/user')
user_service = user_service()

adm = createUserDto(
    cpf="62971312011",
    name="lucas dos santos dias",
    password="123",
    privilege=Privileg.Adm,
    status=Status.Ativo
)

try:
    user_service.createUser(adm);
except:
    pass;

@user_bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    try:
        data = request.form.to_dict() if request.form else request.get_json()
        user = createUserDto(
            cpf=data["cpf"],
            name=data["name"],
            password=data["password"]
        )
        response = user_service.createUser(user)
        flash("User created successfully!", "success")
    except KeyError as e:
        flash(f"Missing field: {e}", "warning")
        return render_template("register.html")
    except ValueError as e:
        flash(str(e), "danger")
        return render_template("register.html")
    except Exception as e:
        print("Erro inesperado:", e)
        flash("Internal server error", "danger")
        return render_template("register.html")

    return redirect(url_for("home.index"))
