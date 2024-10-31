import inquirer
from database.objects import User
from database.current import set_current_data, get_current_data


def auth():
    user = get_current_data("user")
    
    while not user:
        auth = [
            inquirer.List(
                'auth',
                message="Create User",
                choices=["Register", "Login", "Exit"],
            ),
        ]
        logging_in = inquirer.prompt(auth)
        if logging_in['auth'] == "Exit": break

        ask_username = input("Type username here: ")
        ask_password = input("Type password: ")

        if logging_in['auth'] == "Register":
            user = User().create_user(ask_username, ask_password)
            if not user:
                print("User already exists.")
        elif logging_in['auth'] == "Login":
            user = User().login_user(ask_username, ask_password)
            if not user:
                print("Incorrect credentials")

    set_current_data("user", user)
            