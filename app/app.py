from .options.auth import auth
from .options.bot_menu import bot_menu
from .options.bots import bots
from database.current import unload_current_data, save_current_data

def run():
    current = unload_current_data()

    if not current["user"]:
        auth()
        current = unload_current_data()
    
    while current["user"]:
        if not current["bot"]:
            bot = bots()
            if bot:
                break
        else:
            bot_menu()
        current = unload_current_data()

    save_current_data(current)
