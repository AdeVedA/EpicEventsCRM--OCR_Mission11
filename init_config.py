import getpass
import os

from validator.inputs import Input
from views.view import View


def menu():
    header = "SOFTWARE INITIAL CONFIG"
    menu_options = [
        "1. Setup the environnement (run it first)",
        "",
        "2. Initialize the databas tables (run it second)",
        "",
        "3. Define your first Manager (run it last)",
        "",
        "0. Exit",
    ]
    View.menu(header, menu_options)
    choice = input("\x1B[93m")
    return choice


def main_ctrl():
    """Management menu function"""
    while True:
        choice = menu()
        match choice:
            case "1":
                config()
            case "2":
                db_tables_creation()
            case "3":
                db_populate()
            case "0":
                break
            case _:
                View.input_return_prints("choice_error")


def db_populate():
    """3. manager creation"""
    View.menu("First Manager Creation", [])
    View.space(15)
    View.prt_info_blue("Please enter the manager informations")
    manager_username = Input.string_name("\x1B[94mManager name : \x1B[93m")
    is_valid = False
    while not is_valid:
        manager_password = getpass.getpass("\x1B[94mEnter Manager password : ")
        confirm_password = getpass.getpass("\x1B[94mConfirm password : ")
        if manager_password != confirm_password:
            View.input_return_prints("passwords_not_match")
            View.erase_line(2)
        else:
            is_valid = True
    role = "MANAGEMENT"
    user_to_create = [{"username": manager_username, "password": manager_password, "role": role}]

    import populate_manager

    populate_manager.populate_users(user_to_create)

    View.space(17)
    View.prt_info_blue(f"The manager {manager_username} has been created")
    View.space(17)
    View.press_key()


def db_tables_creation():
    """2. database tables creation"""
    View.menu("INITIAL DATABASE TABLES CREATION", [])
    if os.path.exists(".env"):
        with open(".env", "r") as file:
            content = file.read()
            View.prt_green(content)
        View.prt_info_blue("Your environment variable should be properly defined before continuing.")
    else:
        View.prt_warn_yred("you should first run 1. Setup the environnement")
        return

    import database

    database.init_db()
    View.space(17)
    View.prt_info_blue("The tables have properly been created")
    View.space(17)
    View.press_key()


def config():
    """1. Database/Sentry environment setup"""
    View.menu("DATABASE & SENTRY ENVIRONMENT CONFIG", [])
    if os.path.exists(".env"):
        View.space(10)
        View.prt_warn_yred("Your environment variable file already exists.")
        View.space(12)
        View.prt_warn_yred("You can quit by pressing ctrl+C or continue")
        with open(".env", "r") as file:
            content = file.read()
            View.prt_cyan(content)
    else:
        pass
    View.space(13)
    View.prt_info_blue("\x1B[94mPlease enter your environment informations")
    user = input("\x1B[94mPlease enter your Database user : \x1B[93m")
    password = input("\x1B[94mPlease enter your Database password : \x1B[93m")
    host = input("\x1B[94mPlease enter your Database host (default is localhost) : \x1B[93m")
    port = input("\x1B[94mPlease enter your Database port (default is 5432) : \x1B[93m")
    name = input("\x1B[94mPlease enter your Database name : \x1B[93m")
    sentry = input("\x1B[94mPlease enter your Sentry DSN : \x1B[93m")

    data = (
        f"DATABASE_USER='{user}'\nDATABASE_PASSWORD='{password}'\nDB_HOST='{host}'\n"
        f"DB_PORT='{port}'\nDB_NAME='{name}'\nSENTRY_DSN='{sentry}'"
    )

    with open(".env", "w") as file:
        file.write(data)

    View.space(17)
    View.prt_info_blue(f"The database {name} has been setup as your environment")
    View.space(17)
    View.press_key()


if __name__ == "__main__":
    try:
        main_ctrl()
    except KeyboardInterrupt:
        print("\n\x1B[37mStopped by 'service-ordered' user interruption...")
