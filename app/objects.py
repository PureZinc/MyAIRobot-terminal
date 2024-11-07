from hashlib import sha256
from database.model import Model
from app.objects import RobotXP
import math, random, time
from services.ai import quick_ask, human_ask


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

class RobotXP:
    def __init__(self, xp: int):
        self.xp = xp
        self.level = self._get_level()
        self.level_bar = self._level_bar()
    
    def _get_level(self):
        if self.xp == 0: return 1
        return int(math.log(self.xp/10, 1.6)) + 1
    
    def _get_xp_for_level(self, level: int):
        return int(10 * (1.6 ** (level - 1)))
    
    def _level_bar(self):
        level_xp = self._get_xp_for_level(self.level)
        level_left = self.xp - level_xp
        gap = self._get_xp_for_level(self.level + 1) - level_xp
        m = (20*level_left/gap)
        main_bar = ["|" if i < m else "." for i in range(20)]
        return f"[{''.join(main_bar)}]"
    
    def __str__(self):
        return f"Level: {self.level}, XP: {self.xp}, Progress: {self.level_bar}"


class Robots(Model):
    def __init__(self):
        super().__init__("robots")

    def create_robot(self, name, owner_id, behavior=[], memory=[], xp=0):
        obj = {
            "name": name, 
            "owner_id": owner_id, 
            "behavior": behavior, 
            "memory": memory,
            "friends": {},
            "xp": xp
        }
        return self.create(obj)
    
    def create_memory(self, robot_id, convo, extra=[], save=False):
        robot = self.get(robot_id)
        down_to_255 = "Boil it down to under 255 characters"
        new_memory = quick_ask(
            f"Generate new memory for {robot} according to this conversation: {convo}", 
            extra_conditions=[down_to_255, *extra]
        )
        if save:
            robot['memory'].append(new_memory)
            self.update(robot_id, robot)
        return new_memory

    def addRobotXP(self, robot_id, xp):
        robot = self.get(robot_id)
        old_xp = RobotXP(robot["xp"])
        robot["xp"] += xp
        new_xp = RobotXP(robot["xp"])
        self.update(robot_id, robot)
        print(f"\n+{xp} XP")
        if new_xp.level > old_xp.level:
            print(f"{robot['name']} leveled up to level {new_xp.level}!!")
    
    def generate_response(self, robot_id, prompt, extra=[], save_as_mem=True):
        robot = self.get(robot_id)
        asked = human_ask(
            prompt, 
            extra_conditions=[
                robot['behavior'], 
                f"Occasionally use what's in it's memory: {robot['memory']}",
                *extra
            ]
        )
        if save_as_mem:
            in_memory = random.randint(1, 10) <= 3
            if in_memory:
                self.create_memory(robot_id, f"Prompt: {prompt}. Response: {asked}")

    
    def generate_conversation(self, robot1_id, robot2_id, rounds=5, topic=None):
        robot1, robot2 = self.get(robot1_id), self.get(robot2_id)
        template = f"""
        Imitate a conversation between {robot1} and {robot2} {f'based around {topic}' if topic else ''}lasting {rounds} rounds.

        1.) Must talk about things related to the behaviors.

        2.) Imitate as a pet, friend, or human being.

        3.) Only know what's in it's memory. Nothing outside of it should be mentioned.
        """
        convo = quick_ask(template)
        summary = quick_ask(f"Summarize this conversation between {robot1['name']} and {robot2['name']}: {convo}")

        memory = {
            robot1['name']: self.create_memory(robot1_id, convo),
            robot2['name']: self.create_memory(robot2_id, convo)
        }

        return convo, summary, memory

    
    def generate_article(self, robot_id, genre, tone, word_count=800):
        template = f"""
        Generate an {genre} article with a {tone} tone. The word count should be
        less than {word_count} words.
        """
        article = self.generate_response(robot_id, template, save_as_mem=False)
        title = quick_ask(f"Generate a title under 50 characters for this article: {article}")
        return article, title
    
    def boil_down_memory(self, robot_id):
        robot = self.get(robot_id)
        return quick_ask(f"Boil all this memory down into one sentence: {robot['memory']}")
    
    def read_article(self, robot_id, article):
        temp = f"Review or critique this story: {article}"
        review = self.generate_response(robot_id, article, extra=[temp])
        return review


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
