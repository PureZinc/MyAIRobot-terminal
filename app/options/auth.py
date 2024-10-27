import inquirer
from database.objects import User
from database.current import set_current_data


def auth():
    auth = [
        inquirer.List(
            'auth',
            message="Login to your account!",
            choices=["register", "login", "exit"],
        ),
    ]
    logging_in = inquirer.prompt(auth)
    if logging_in['auth'] == "exit": return False

    ask_username = input("Type username here: ")
    ask_password = input("Type password: ")

    if logging_in['auth'] == "register":
        user = User().create_user(ask_username, ask_password)
    elif logging_in['auth'] == "login":
        user = User().login_user(ask_username, ask_password)

    if user:
        set_current_data("user", user)
        return True
    return False