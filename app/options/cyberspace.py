import time
from app.utils import choice_interface, coming_soon
from database.objects import User, Robot
from database.current import set_current_data, get_current_data
from pprint import pprint


def all_robots():
    robots = [bot["name"] for bot in Robot().query()]
    total_bots = len(robots)

    pprint(f"{robots}")
    choice_interface(
        f"\nTotal Robots: {total_bots}", {
            "Search Bots": coming_soon
        }
    )


def observe_cyberspace():
    user = get_current_data("user")
    print("\n Entering Cyberspace as a Human \n")
    time.sleep(2)
    choice = choice_interface(
        f"You are currently observing Cyberspace, {user['username']}!", {
            "Robots": all_robots,
            "Leaderboard": coming_soon,
            "Library": coming_soon,
        }
    )
    if choice == "exited":
        print("\n Exiting Cyberspace \n")
        time.sleep(2)
