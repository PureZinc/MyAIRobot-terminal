from services.ai import ask_chat, robot_convo, boil_down_memory
from app.utils import choice_interface, coming_soon
from database.current import set_current_data, unload_current_data, get_current_data
from ..objects import Robot, RobotXP
import time
import random
from functools import wraps
from .library import explore_library


def bot_stats(bot_id):
    bot = Robot.get(bot_id)
    print(
        "\n\n", 
        f"Bot Name: {bot['name']}", "\n", 
        f"Behavior: {bot['behavior']}", "\n", 
        RobotXP(bot['xp']), "\n"
    )


def requires_level(min_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            bot = get_current_data("bot")
            xp = bot['xp']
            level = RobotXP(xp).level
            if level < min_level:
                print(f"This unlocks at level {min_level}! \n")
                return False
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ask_bot():
    current = unload_current_data()

    bot = current['bot']
    username = current['user']['username']

    ask_me_anything = f"Hello, {username}! I'm {bot['name']}! Ask me anything"
    while True:
        prompt = input(f"\n \n (Press 0 to break) {ask_me_anything}: ")
        if prompt == "0":
            break

        answer, memory = Robot.generate_response(bot['id'], prompt)
        print("\n \n", answer)
        
        xp_gain = 10
        if memory:
            bot["memory"].append(memory)
            print("\nNew Memory Made! +5XP")
            Robot.update(bot["id"], bot)
            xp_gain += 5

        Robot.addRobotXP(bot["id"], xp_gain)
        new_bot = Robot.get(bot["id"])
        set_current_data("bot", new_bot)
        ask_me_anything = "Ask me something else"


def bot_settings():
    bot = get_current_data("bot")
    bot_stats(bot['id'])
    choice_interface(
        "Settings", {
            "Delete Robot": coming_soon
        }
    )


def train_memory():
    bot = get_current_data("bot")
    memory = bot['memory']

    def boil_mem():
        new_memory = Robot.boil_down_memory(bot['id'])
        bot['memory'] = [new_memory]
        Robot.update(bot['id'], bot)
        set_current_data("bot", bot)
        print("Memory boiled down!")

    def view_mem():
        for memory in bot['memory']:
            print(memory)

    choice_interface(
        f"Robot has {len(memory)} items in it's memory!", {
            "Boil Down Memory": boil_mem,
            "View Memory": view_mem
        }
    )

@requires_level(3)
def train_bot():
    choice_interface(
        "Welcome to training!", {
            "Train Memory": train_memory,
            "Train Behavior": coming_soon
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

    conversation, summary, memory = Robot.generate_conversation(current_robot['id'], robot2['id'], rounds=random.randrange(4, 8))

    print(conversation, "\n\n")
    print(f"\nSummary: {summary}\n")

    current_robot['friends'][robot2['name']] = current_robot['friends'].get(robot2['name'], 0) + 1
    robot2['friends'][current_robot['name']] = robot2['friends'].get(current_robot['name'], 0) + 1

    current_robot['memory'].append(memory[current_robot['name']])
    robot2['memory'].append(memory[robot2['name']])

    Robot.update(current_robot["id"], current_robot)
    set_current_data("bot", current_robot)
    Robot.update(robot2["id"], robot2)

    Robot.addRobotXP(current_robot["id"], 30)
    Robot.addRobotXP(robot2["id"], 50)


def playground():
    choice_interface(
        "The Playground!", {
            "Chat With Other Bots": chat_between_robots,
            "Play Games": coming_soon
        }
    )


def adventure_into_cyberspace():
    print("\n Entering Cyberspace \n")
    time.sleep(2)
    choice = choice_interface(
        "Welcome to Cyberspace! Where would you like to explore?", {
            "Playground": playground,
            "Gym": coming_soon,
            "Library": explore_library,
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
