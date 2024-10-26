from hashlib import sha256
from .model import Model


hasher = lambda pw: sha256(pw.encode()).hexdigest()

class User(Model):
    def __init__(self):
        super().__init__("users")
    
    def create_user(self, username, password):
        hashed_password = hasher(password)
        obj = {"username": username, "password": hashed_password}
        return self.create(obj)
    
    def login_user(self, username, password):
        hashed_password = hasher(password)
        obj = {"username": username, "password": hashed_password}
        available_users = self.query(**obj)
        if len(available_users) == 1:
            return available_users[0]
        else:
            return None


class Robot(Model):
    def __init__(self):
        super().__init__("robots")

    def create_robot(self, name, owner_id, behavior=[], memory=[], xp=0):
        obj = {
            "name": name, 
            "owner_id": owner_id, 
            "behavior": behavior, 
            "memory": memory,
            "xp": xp
        }
        return self.create(obj)