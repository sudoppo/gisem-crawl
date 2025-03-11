import os
import bcrypt
from dotenv import load_dotenv

env_path = ".env"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode(), salt)
    return hashedPassword

def store_password(hashedPassword):
    with open("password.txt", "wb") as f:
        f.write(hashedPassword)

def check_password(password, stored_hashed_password):
    return bcrypt.checkpw(password.encode(), stored_hashed_password)

def check_env():
    
    if not os.path.exists(env_path):
        print(".env file not found! Creating .env file...")
        create_dotenv_file()
    else:
        # Load environment variables
        load_dotenv()

        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        if password and username:
            print("Username and password loaded from .env")
        elif username:
            print("Username loaded from .env")
            print("Password was not found in .env")
            print("Please enter your GISEM password!")
            return 2
        elif password:
            print("Password loaded from .env")
            print("Username was not found in .env")
            print("Please enter your GISEM username!")
            return 1
        
        else:
            print("Username and password were not found in .env")
            print("Please enter your GISEM username and password!")
            return -1
            
    

def create_dotenv_file():
    with open(".env", "w") as f:
        f.write("PASSWORD=")


