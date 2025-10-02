from faker import Faker
import pandas as pd
import os
import bcrypt
import uuid


here  = os.path.abspath(os.path.dirname(__file__))


## populate andress


andress  = pd.DataFrame(columns=["id","County","state","Number","streat"])
Users = pd.DataFrame(columns=['id','name','cpf','id_andress','role','tell','password',''])

