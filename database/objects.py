from hashlib import sha256
from .model import Model
import time
from app.objects import RobotXP


hasher = lambda pw: sha256(pw.encode()).hexdigest()

default_profile = {
    "membership": "Free",
    "cybercoins": 100,
    "joined on": "Today"
}

class Users(Model):
    def __init__(self):
        super().__init__("users")
    
    def create_user(self, username, password):
        hashed_password = hasher(password)
        obj = {"username": username, "password": hashed_password}
        available_users = self.query(**obj)
        if len(available_users) > 0:
            return None
        return self.create({**obj, "profile": default_profile})
    
    def login_user(self, username, password):
        hashed_password = hasher(password)
        obj = {"username": username, "password": hashed_password}
        available_users = self.query(**obj)
        if len(available_users) == 1:
            return available_users[0]
        return None


class Robots(Model):
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

    def addRobotXP(self, robot_id, xp):
        robot = self.get(robot_id)
        old_xp = RobotXP(robot["xp"])
        robot["xp"] += xp
        new_xp = RobotXP(robot["xp"])
        self.update(robot_id, robot)
        print(f"\n+{xp} XP")
        if new_xp.level > old_xp.level:
            print(f"{robot['name']} leveled up to level {new_xp.level}!!")


class Articles(Model):
    def __init__(self):
        super().__init__("articles")
    
    def create_article(self, author_id, title, content):
        obj = {
            "author_id": author_id,
            "title": title,
            "content": content,
            "written_date": time.localtime()
        }
        return self.create(obj)
    
User = Users()
Robot = Robots()
Article = Articles()