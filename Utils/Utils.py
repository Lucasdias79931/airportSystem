from enum import Enum
import re
from functools import wraps
import json
import os
from dotenv import load_dotenv
from flask import flash, session, redirect, url_for

class Privilege(Enum):
    Normal = 1
    Adm = 2

class Status(Enum):
    Ativo = 1
    Inativo = 2
    Pendent = 3


load_dotenv()  


def validateCpf(cpf:str)->dict:
    if cpf is None:
        return {"status":False, "msg":"CPF não fornecido para validação"}

    cpf_numbers = re.sub(r"\D", "", cpf)

    if len(cpf_numbers) != 11 or cpf_numbers == cpf_numbers[0] * 11:
        return {"status":False, "msg" :"CPF inválido: formato incorreto ou repetido"}

    def calc_digito(cpf_parcial):
        soma = sum(int(cpf_parcial[i]) * (len(cpf_parcial) + 1 - i) for i in range(len(cpf_parcial)))
        resto = (soma * 10) % 11
        return resto if resto < 10 else 0

    dig1 = calc_digito(cpf_numbers[:9])
    dig2 = calc_digito(cpf_numbers[:9] + str(dig1))

    if cpf_numbers[-2:] != f"{dig1}{dig2}":
        return {"status":False, "msg":"CPF inválido: dígitos verificadores incorretos"}

    return {"status":True, "msg":"", "cpf":cpf_numbers}
    


def verifyIfCpfExist(cpf:str):
    cpf_numbers = re.sub(r"\D", "", cpf)

    db_dir = os.getenv("DATABASE")

    db_path = os.path.join(db_dir, "user.json")

    if not os.path.exists(db_path):
        return False

    try:
        with open(db_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    except Exception as e:

        raise   ValueError("Error in try opening user_db")

    for u in data:
        if str(u.get("cpf")) == cpf_numbers:
            return True

    return False
    

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash("Você precisa fazer login primeiro.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
 

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        usuario = session.get("usuario")

        if not usuario:
            flash("Você precisa estar logado.", "warning")
            return redirect(url_for("auth.login"))

        privilege = session.get("privilege")

        if privilege != 2:
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for("menu.menu"))

        return f(*args, **kwargs)
    return decorated_function
