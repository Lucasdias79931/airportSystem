from faker import Faker
import pandas as pd
import os
import bcrypt
import uuid


here  = os.path.abspath(os.path.dirname(__file__))


## populate andress

andressColumns = ["id","County","state","Number","streat"]

andress  = pd.DataFrame(columns=andressColumns)



