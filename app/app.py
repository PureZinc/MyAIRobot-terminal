from .options.auth import auth
from .options.bot_menu import bot_menu
from .options.bots import bots
from database.current import unload_current_data, save_current_data

def run():
    current = unload_current_data()

    if not current["user"]:
        auth()

    if current["user"] and not current["bot"]:
        bots()
        current = unload_current_data()

    if current["user"] and current["bot"]:
        bot_menu()

    save_current_data(current)
