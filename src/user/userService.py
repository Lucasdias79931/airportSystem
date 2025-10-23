import os, sys
from Utils.Utils import validateCpf, verifyIfCpfExist
from .userDTO.createUserDTO import createUserDto
from .userDTO.userRepository import UserRepository

class userService:
    def __init__(self):
        self.userRepository = UserRepository()

    def createUser(self, user: createUserDto):
        # Validate CPF format and checksum
        cpf_validated = validateCpf(user.cpf)
        if not cpf_validated['status']:
            raise ValueError("Invalid CPF")

        # Check duplicate
        if verifyIfCpfExist(user.cpf):
            raise ValueError("CPF already exists in the system")

        # Use normalized CPF
        user.cpf = cpf_validated['cpf']

        # Persist user
        self.userRepository.save(user)
        return {"message": "User created successfully!"}
