from services.ai import ask_chat
from app.utils import choice_interface, coming_soon


def ask_bot():
    ask_me_anything = f"Hello! Ask me anything"
    while True:
        prompt = input(f"(press 0 to break) {ask_me_anything}: ")
        if prompt == "0":
            break
        answer = ask_chat(prompt)
        print(answer)
        ask_me_anything = "Ask me something else"


def bot_menu():
    choice_interface(
        "Hello! What do we plan on doing today?", {
            "chat": ask_bot,
            "train": coming_soon,
            "adventure": coming_soon,
            "settings": coming_soon
        }
    )