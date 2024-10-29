from .options.auth import auth
from .options.bot_menu import bot_menu
from .options.intro import intro
from .options.profile import profile
from database.current import get_current_data

def run():
    play = intro()
    if play:
        user = get_current_data("user")
        if not user:
            auth()
            user = get_current_data("user")
        
        while user:
            bot = get_current_data("bot")
            while not bot:
                profile()
                bot = get_current_data("bot")
            bot_menu()
