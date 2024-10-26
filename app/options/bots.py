import inquirer
from database.objects import Robot
from database.current import unload_current_data, save_current_data
from services.ai import generate_behaviors
from ..utils import choice_interface


def create_bot():
    behaviors = "inapropriate"
    while behaviors == "inapropriate":
        name = input("Name your Robot: ")
        description = input("Write a 100 word description of your robot: ")
        while len(description) < 100:
            print(f"Description only contains {len(description)} words")
            description = input("Write a 100 word description of your robot: ")
        behaviors = generate_behaviors(description)
    
    current = unload_current_data()
    Robot().create_robot(name, current["user"], behavior=behaviors.split(', '))
    current["robot"] = Robot().query(name=name, user_id=current["user"])[0].id
    save_current_data(current)

def choose_bot():
    current = unload_current_data()
    robots = Robot().query(owner_id=current["user"])
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
        chosen_robot = inquirer.prompt(choice_bot)
        current["bot"] = chosen_robot
        save_current_data(current)
        return True


def bots():
    choice_interface(
        "Manage your bots", {
            "create new robot": create_bot,
            "choose robot": choose_bot,
        }
    )