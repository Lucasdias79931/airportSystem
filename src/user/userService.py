import os, sys
from Utils.Utils import validateCpf
from .createUserDTO import createUserDto
from .userRepository import UserRepository
import re

class user_service:
    userRepository : UserRepository;

    def __init__(self):
        self.userRepository = UserRepository()

    def cpfExists(self, cpf:str) -> bool:
        #cpf_numbers = re.sub(r"\D", "", cpf)
        cpf_numbers = int(cpf)

        if self.userRepository.tree.search(cpf_numbers) == None:
            return False
        else:
            return True 

    def createUser(self, user: createUserDto):
        # Validate CPF format and checksum
        cpf_validated = validateCpf(user.cpf)
        if not cpf_validated['status']:
            raise ValueError("Invalid CPF")

        # Check duplicate
        if self.cpfExists(user.cpf):
            raise ValueError("CPF already exists in the system")

        # Use normalized CPF
        user.cpf = cpf_validated['cpf']

        # Persist user
        self.userRepository.save(user)
        return {"message": "User created successfully!"}
