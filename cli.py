import click
from auth import store_password, store_username, hash_password, check_env

@click.group()
def cli():
    """A complex web scraping tool for GISEM."""
    pass

@click.command()
@click.option("--username", prompt="Enter username", help="Your username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Your password")
def register(username, password):
    """Register or update credentials."""
    status_response = check_env()

    if status_response == 0:
        if not click.confirm("Credentials already exist. Overwrite them?"):
            click.echo("Exiting without changes.")
            return

    if status_response == 2:
        password = click.prompt("Enter password", hide_input=True, confirmation_prompt=True)
        register_password(password)
        click.echo("User registered successfully!")
    elif status_response == 1:
        username = click.prompt("Enter username")
        register_username(username)
        click.echo("User registered successfully!")
    elif status_response == -1:
        register_username(username)
        register_password(password)
        click.echo("User registered successfully!")
    
    else:
        click.echo("All credentials are set up correctly!")

def register_password(password):
    hashedPassword = hash_password(password)
    store_password(hashedPassword)

def register_username(username):
    store_username(username)

    
@click.command()
def exec():
    click.echo("Welcome to the GISEM CLI!")
    status_response = check_env()
    if status_response == 0:
        click.echo("All credentials are set up correctly!")
    else:
        click.echo("Run 'register' command to set up credentials")
        
cli.add_command(register)
cli.add_command(exec)

if __name__ == '__main__':
    cli()