from app.utils import choice_interface, coming_soon


def intro():
    choice = choice_interface(
        f"What would you like to do?", {
            "Play": lambda: None,
            "About": coming_soon
        }, self_returns=["Play"]
    )
    if choice == "exited":
        return False
    elif choice == "Play":
        return True
