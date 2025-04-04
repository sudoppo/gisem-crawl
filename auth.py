import os
import bcrypt
from dotenv import load_dotenv

env_path = ".env"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode(), salt)
    return hashedPassword

def store_password(hashedPassword):
    with open(".env", "a") as f:
        f.write(f"PASSWORD={hashedPassword.decode()}\n")

def check_password(password, stored_hashed_password):
    return bcrypt.checkpw(password.encode(), stored_hashed_password)

def store_username(username):
    with open(".env", "a") as f:
        f.write(f"USERNAME={username}\n")

def check_env():
    if not os.path.exists(env_path):
        print(".env file not found! Creating .env file...")
        create_dotenv_file()
        return -1
    else:
        # Load environment variables
        load_dotenv()

        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')

        if not password:
            print("Password was not found in .env")
            if not username:
                print("Username was not found in .env")
                print("Please enter your GISEM username and password!")
                return -1
            
            print("Please enter your GISEM password!")
            return 2
        
        elif not username:
            print("Username was not found in .env")
            print("Password was found in .env")
            print("Please enter your GISEM username")
            return 1
        
        return 0
        
            
    

def create_dotenv_file():
    with open(".env", "w") as f:
        f.write("# GISEM credentials\n")
    



