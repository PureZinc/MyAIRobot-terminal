from services.ai import ask_chat, robot_convo
from app.utils import choice_interface, coming_soon
from database.current import set_current_data, unload_current_data, get_current_data
from ..objects import RobotXP
from database.objects import Robot
import time
import random


def ask_bot():
    current = unload_current_data()

    bot = current['bot']
    username = current['user']['username']

    ask_me_anything = f"Hello, {username}! I'm {bot['name']}! Ask me anything"
    while True:
        prompt = input(f"\n \n (Press 0 to break) {ask_me_anything}: ")
        if prompt == "0":
            break

        answer = ask_chat(bot, prompt)
        print("\n \n", answer)



        ask_me_anything = "Ask me something else"


def bot_settings():
    bot = get_current_data("bot")
    print(
        "\n\n", 
        f"Bot Name: {bot['name']}", "\n", 
        f"Behavior: {bot['behavior']}", "\n", 
        RobotXP(bot['xp']), "\n"
    )

    while True:
        choice = choice_interface(
            "Settings", {
                "Delete Robot": coming_soon
            }
        )
        if choice == "exited":
            break


def train_bot():
    bot = get_current_data("bot")
    xp = bot['xp']
    level = RobotXP(xp).level
    if level < 3:
        print("This unlocks at level 3! \n")
        return False
    
    choice_interface(
        "Welcome to training!", {
            "choices": coming_soon
        }
    )

def chat_between_robots():
    current_robot = get_current_data("bot")
    robots = Robot.query()
    all_robots = [bot for bot in robots if bot != current_robot]
    robot2 = random.choice(all_robots)

    print("Finding bot to talk to...")
    time.sleep(2)
    print(f"{current_robot['name']} is currently speaking to {robot2['name']}")
    conversation, summary = robot_convo(current_robot, robot2, rounds=random.randrange(4, 8))
    for convo in conversation:
        print(convo, "\n\n")
        time.sleep(2)
    print(f"\nSummary: {summary}\n")

    # if f"Spoke to {robot2['name']}" not in current_robot['memory']:
    #     current_robot['memory'].append(f"Spoke to {robot2['name']}")
    # if f"Spoke to {current_robot['name']}" not in robot2['memory']:
    #     robot2['memory'].append(f"Spoke to {current_robot['name']}")

    # Robot().update(current_id, current_robot)
    # set_current_data("bot", current_robot)
    # Robot().update(robot2_id, robot2)


def playground():
    while True:
        choice = choice_interface(
            "The Playground!", {
                "Chat With Other Bots": chat_between_robots,
                "Play Games": coming_soon
            }
        )
        if choice == "exited":
            break

def adventure_into_cyberspace():
    print("\n Entering Cyberspace \n")
    time.sleep(2)
    choice = choice_interface(
        "Welcome to Cyberspace! Where would you like to explore?", {
            "Playground": playground,
            "Gym": coming_soon,
            "Library": coming_soon,
        }
    )
    if choice == "exited":
        print("\n Exiting Cyberspace \n")
        time.sleep(2)


def bot_menu():
    user, bot = get_current_data("user"), get_current_data("bot")
    user_name, bot_name = user['username'], bot['name']

    if bot:
        choice_interface(
            f"Hello, {user_name}, I'm {bot_name}! What do we plan on doing today?", {
                "Chat": ask_bot,
                "Train": train_bot,
                "Enter Cyberspace": adventure_into_cyberspace,
                "Settings": bot_settings
            }
        )
        set_current_data("bot", None)