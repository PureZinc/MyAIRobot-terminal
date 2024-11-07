from services.ai import human_ask
from .objects import Article

class RobotCharacter:
    def __init__(self, name: str, template: str):
        self.name = name
        self.template = template
    
    def generate_response(self, prompt):
        response = human_ask(prompt, extra_conditions=[self.template, f"You've read all these articles: {Article.query()}"])
        return response
    

Leila = RobotCharacter("Leila", """
You're name is Leila. You are a librarian working in Cyberspace. You're purpose is to assist other robots and humans
around the library. You're a quiet, reserved person focused on the art of literature, and
you often critique articles in the very critical, but kind way.
""")
