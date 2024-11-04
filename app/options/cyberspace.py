import time
from app.utils import choice_interface, search_interface, coming_soon
from database.objects import User, Robot, Article
from .library import observe_library
from ..objects import RobotXP
from database.current import set_current_data, get_current_data
from pprint import pprint


def robot_stats(bot_id):
    bot = Robot.get(bot_id)
    owner = User.get(bot['owner_id'])
    xp = RobotXP(bot['xp'])
    articles = len(Article.query(author_id=str(bot_id)))
    print(
        f"Name: {bot['name']}\n",
        f"Owner: {owner['username']}\n",
        f"Total Friends: {len(bot['friends'])}\n",
        f"Articles written: {articles}\n",
        f"Status: {xp}\n"
    )
    input("Press enter to exit...")

def all_robots():
    robots = Robot.query()
    total_bots = len(robots)
    choice_filter = lambda bot: bot['name']

    search_interface(
        f"Total Bots: {total_bots}", robots, 
        retrieve_func=robot_stats, choice_filter=choice_filter, query_num=10
    )

def leaderboard():
    choice_interface(
        "Leaderboard:", {
            "Top Players": lambda: None,
            "Top Robots": lambda: None
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
            "Library": observe_library,
        }
    )
    if choice == "exited":
        print("\n Exiting Cyberspace \n")
        time.sleep(2)
