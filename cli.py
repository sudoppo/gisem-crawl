import click
from auth import store_password, hash_password, check_env

@click.group()
def cli():
    greeting()

@click.command()
@click.option("--username", prompt="Enter username", help="Your username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Your password")
def register(username, password):
    register_username(username)
    register_password(password)
    click.echo("User registered successfully!")

def register_password(password):
    hashedPassword = hash_password(password)
    store_password(hashedPassword)

def register_username(username):
    print(f"Username: {username}")

    

def greeting():
    click.echo('Welcome to the GISEM Crawling CLI!')
    status_response = check_env()

    if status_response == 2:
        password = click.prompt("Enter password", hide_input=True, confirmation_prompt=True)
        register_password(password)
    elif status_response == 1:
        username = click.prompt("Enter username")
        register_username(username)
    elif status_response == -1:
        click.echo("Please enter your GISEM username and password!")
        register()  # Call register function to ask for both username and password
    else:
        click.echo("Username and password loaded from .env")
        

cli.add_command(register)

if __name__ == '__main__':
    cli.main(args=["register"])