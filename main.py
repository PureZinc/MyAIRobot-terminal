import inquirer
from services.ai import ask_chat, generate_behaviors
from database.objects import User, Robot
from database.current import current, unload_current_data, save_current_data


title = "Welcome to My AI Robot!"
subtitle = "Build your very own AI and venture him off into Cyberspace!"

def start_authorize():
    auth = [
        inquirer.List(
            'auth',
            message="Login to your account!",
            choices=["register", "login", "exit"],
        ),
    ]
    logging_in = inquirer.prompt(auth)
    if logging_in['auth'] == "exit": return False

    ask_username = input("Type username here: ")
    ask_password = input("Type password: ")

    if logging_in['auth'] == "register":
        user = User().create_user(ask_username, ask_password)
    elif logging_in['auth'] == "login":
        user = User().login_user(ask_username, ask_password)

    if user:
        current["user"] = user
        return True
    return False

def ask_bot():
    ask_me_anything = f"Hello! Ask me anything"
    while True:
        prompt = input(f"(press 0 to break) {ask_me_anything}: ")
        if prompt == "0":
            break
        answer = ask_chat(prompt)
        print(answer)
        ask_me_anything = "Ask me something else"

def bot_making_menu():
    main_menu = [
        inquirer.List(
            'option',
            message=f"Choose one of your robots!",
            choices=["choose bot", "create new bot", "exit"],
        ),
    ]
    choice = inquirer.prompt(main_menu)
    while True:
        if choice['option'] == "create new bot":

            behaviors = "inapropriate"
            while behaviors == "inapropriate":
                name = input("Name your Robot: ")
                description = input("Write a 100 word description of your robot: ")
                while len(description) < 100:
                    print(f"Description only contains {len(description)} words")
                    description = input("Write a 100 word description of your robot: ")
                behaviors = generate_behaviors(description)
            
            robot = Robot().create_robot(name, current["user"], behavior=behaviors.split(', '))
            current["robot"] = robot.query(name=name, user_id=current["user"])[0].id

        elif choice['option'] == "choose bot":
            robots = Robot().query(owner_id=current["user"])
            if not robots:
                print("You haven't created any robots yet!")
                continue
            else:
                choice_bot = [
                    inquirer.List(
                        'option',
                        message=f"Choose one of your robots!",
                        choices=robots,
                    ),
                ]
                chosen_robot = inquirer.prompt(choice_bot)
                current["bot"] = chosen_robot
        elif choice['option'] == "exit":
            break

def play():
    bot_menu = [
        inquirer.List(
            'option',
            message=f"Hello! What do we plan on doing today?",
            choices=["chat", "train", "adventure", "settings", "exit"],
        ),
    ]
    while True:
        answers = inquirer.prompt(bot_menu)
        if answers['option'] == "chat":
            ask_bot()
        elif answers['option'] == "exit":
            break

if __name__ == "__main__":
    print("\n \n \n" + title)
    print(subtitle + "\n")

    # unload_current_data()

    # if not current["user"]:
    #     start_authorize() 

    # if not current["bot"]:
    #     bot_making_menu()

    play()

    # save_current_data()

    print("Thanks for playing :). I'll see you back soon!")
