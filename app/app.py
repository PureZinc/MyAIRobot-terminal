from .options.auth import auth
from .options.intro import intro
from .options.profile import profile

def run():
    play = intro()
    while play:
        auth()
        profile()
        play = intro()

        

