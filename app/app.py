from .options.auth import auth
from .options.bot_menu import bot_menu
from .options.intro import intro
from .options.profile import profile
from database.current import get_current_data

def run():
    play = intro()
    while play:
        auth()
        profile()
        play = intro()

        

