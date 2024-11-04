import inquirer
from database.objects import Robot
from database.current import unload_current_data, save_current_data, set_current_data
from services.ai import generate_behaviors
from ..utils import choice_interface
from .bot_menu import bot_menu


def create_bot():
    behaviors = "inapropriate"
    while behaviors == "inapropriate":
        name = input("(Press 0 to exit) Name your Robot: ")
        if name == "0": return False
        description = input("(Press 0 to exit) Write a 100 word description of your robot: ")
        if description == "0": return False
        while len(description) < 100:
            print(f"Description only contains {len(description)} words")
            description = input("(Press 0 to exit) Write a 100 word description of your robot: ")
            if description == "0": return False
        behaviors = generate_behaviors(description)
        if behaviors == "inapropriate":
            print("Prompt is inapropriate!")
    
    current = unload_current_data()
    new_bot = Robot.create_robot(name, current["user"]["id"], behavior=behaviors)
    current["bot"] = Robot.get(new_bot)
    save_current_data(current)


def choose_bot():
    current = unload_current_data()
    robots = Robot.query(owner_id=current["user"]["id"])
    if not robots:
        print("You haven't created any robots yet!")
    else:
        choose_robots = [bot["name"] for bot in robots]
        choice_bot = [
            inquirer.List(
                'option',
                message=f"Choose one of your robots!",
                choices=choose_robots,
            ),
        ]
        chosen_robot = inquirer.prompt(choice_bot)['option']
        get_robot = Robot.query(owner_id=current["user"]["id"], name=chosen_robot)[0]
        current["bot"] = get_robot
        save_current_data(current)
        bot_menu()


def bots():
    choice_interface(
        "Manage your bots", {
            "Create New Robot": create_bot,
            "Choose Robot": choose_bot,
        }
    )
