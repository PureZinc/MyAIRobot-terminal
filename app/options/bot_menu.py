from services.ai import ask_chat
from app.utils import choice_interface, coming_soon
from database.current import set_current_data, unload_current_data, get_current_data
from services.robot_xp import RobotXP


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
    
    choice = choice_interface(
        "Hello! What do we plan on doing today?", {
            "chat": ask_bot,
            "train": coming_soon,
            "adventure": coming_soon,
            "settings": bot_settings
        }
    )


def bot_menu():
    choice = choice_interface(
        "Hello! What do we plan on doing today?", {
            "chat": ask_bot,
            "train": train_bot,
            "adventure": coming_soon,
            "settings": bot_settings
        }
    )
    if choice == "exited":
        set_current_data("bot", None)