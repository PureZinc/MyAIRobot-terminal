from database.current import get_current_data, set_current_data
from app.utils import choice_interface, coming_soon
from .bots import bots
from pprint import pprint


def log_out(are_you_sure):
    print(are_you_sure)
    yes_no = input("0: YES | 1: NO  ")
    if yes_no == "0":
        print("User successfully logged out!")
        set_current_data("user", None)

def my_profile():
    user = get_current_data("user")
    profile = user["profile"]

    print("My Profile: \n")
    for type, value in profile.items():
        print(f"{type}: {value}\n")

    choice_interface(
        f"", {
            "Edit Profile": coming_soon,
            "Upgrade Membership": coming_soon
        }
    )

def settings():
    choice_interface(
        f"What would you like to do?", {
            "View Profile": my_profile,
            "Log Out": lambda: log_out("Are you sure you want to log out?"),
            "Delete": coming_soon,
        }
    )


def profile():
    user = get_current_data("user")

    choice = choice_interface(
        f"Welcome Back, {user['username']}!", {
            "Profile": my_profile,
            "My Bots": bots,
            "Settings": settings
        }
    )
    log_out("Would you also like to log out?")
