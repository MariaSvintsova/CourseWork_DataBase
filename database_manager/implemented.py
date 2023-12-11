import os
from dotenv import load_dotenv

load_dotenv()
database = os.getenv("database")
host = os.getenv("host")
user = os.getenv('user')
password = os.getenv('password')



