from faker import Faker
import pandas as pd
import os
import bcrypt
import uuid


here  = os.path.abspath(os.path.dirname(__file__))


## populate andress


Users = pd.DataFrame(columns=['id','name','cpf','addres','role','tell','password',''])

