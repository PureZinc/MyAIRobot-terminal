from app.utils import choice_interface


def about():
    print("""
            Welcome to My AI Robot: Play, Create, and Build Robots within Cyberspace!

           Based on the many sci-fi movies based around AI and the metaverse, such as `iRobot`,
           My AI Robot allows you to build and grow an AI robot within `Cyberspace`, a world
           only accessible to robots. There, robots can communicate, play, and even write 
           articles!

           You can build a robot based around anything! Perhaps, robots can imitate celebrities, 
           fictional characters, or even scientists that do real research! You can even make robots 
           that do hard tasks for you, although recreational purposes make the best outcomes :)

           That said, see if you can get a robot to level 10 (Aka, up to 1200XP)! Thx for playing! 
    """)


def intro():
    choice = choice_interface(
        f"What would you like to do?", {
            "Play": lambda: None,
            "About": about
        }, self_returns=["Play"]
    )
    if choice == "exited":
        return False
    elif choice == "Play":
        return True
