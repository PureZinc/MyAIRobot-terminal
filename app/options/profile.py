from database.current import get_current_data, set_current_data
from app.utils import choice_interface, coming_soon
from .bots import bots


def profile():
    user = get_current_data("user")

    choice = choice_interface(
        f"Welcome Back, {user['username']}!", {
            "Profile": coming_soon,
            "My Bots": bots,
            "Settings": coming_soon
        }
    )
    if choice == "exited":
        if choice == "exited":
            print("Would you also like to log out?")
            yes_no = input("0: YES | 1: NO  ")
            if yes_no == "0":
                set_current_data("user", None)
            return True
