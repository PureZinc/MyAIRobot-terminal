from services.ai import ask_chat, robot_convo
from app.utils import choice_interface, coming_soon
from database.current import set_current_data, unload_current_data, get_current_data
from services.robot_xp import RobotXP
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

        behaviors = ' '.join(bot['behavior'])
        answer = ask_chat(prompt, params=[f"Robot name: {bot['name']}", f"Imitate these behaviors: {behaviors}"])
        print("\n \n", answer)
        ask_me_anything = "Ask me something else"


def bot_settings():
    bot = get_current_data("bot")
    print(
        "\n \n", 
        f"Bot Name: {bot['name']}", "\n", 
        f"Behavior: {bot['behavior']}", "\n", 
        RobotXP(bot['xp']), "\n"
    )

    while True:
        choice = choice_interface(
            "Settings", {
                "rename": coming_soon,
                "delete": coming_soon
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
    
    choice = choice_interface(
        "Welcome to training!", {
            "choices": coming_soon
        }
    )

def chat_between_robots():
    current_robot = get_current_data("bot")
    robots = Robot().query()
    all_robots = [bot for bot in robots if bot != current_robot]
    robot2 = random.choice(all_robots)

    current_id, robot2_id = Robot().get_id(current_robot), Robot().get_id(robot2)

    print("Finding bot to talk to...")
    time.sleep(2)
    print(f"{current_robot['name']} is currently speaking to {robot2['name']}")
    conversation, summary, memories = robot_convo(current_robot, robot2, rounds=random.randrange(2, 6))
    print("\n", conversation, "\n")
    print(summary, "\n")
    

    curr_memory, rob2_memory = memories[current_robot['name']], memories[robot2['name']]

    current_robot['memory'].append(curr_memory)
    robot2['memory'].append(rob2_memory)

    Robot().update(current_id, current_robot)
    set_current_data("bot", current_robot)
    Robot().update(robot2_id, robot2)
    


def playground():
    while True:
        choice = choice_interface(
            "The Playground!", {
                "chat with other bots": chat_between_robots,
                "play games": coming_soon
            }
        )
        if choice == "exited":
            break

def adventure_into_cyberspace():
    print("\n Entering Cyberspace \n")
    time.sleep(2)
    choice = choice_interface(
        "Welcome to Cyberspace! Where would you like to explore?", {
            "playground": playground,
            "gym": coming_soon,
            "library": coming_soon,
        }
    )
    if choice == "exited":
        print("\n Exiting Cyberspace \n")
        time.sleep(2)


def bot_menu():
    choice = choice_interface(
        "Hello! What do we plan on doing today?", {
            "chat": ask_bot,
            "train": train_bot,
            "enter cyberspace": adventure_into_cyberspace,
            "settings": bot_settings
        }
    )
    if choice == "exited":
        set_current_data("bot", None)