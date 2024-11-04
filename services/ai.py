from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config.config import OPENAI_API_KEY
import random


model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=OPENAI_API_KEY)

def quick_ask(prompt, extra_conditions=[]):
    invoketion = [SystemMessage(prompt), *[SystemMessage(extra) for extra in extra_conditions]]
    response = model.invoke(invoketion)
    return response.content

def human_ask(prompt, extra_conditions=[]):
    invoketion = [*[SystemMessage(extra) for extra in extra_conditions], HumanMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content

def get_memory(bot, convo, extra=[]):
    down_to_255 = "Boil it down to under 255 characters"
    return quick_ask(f"Generate memory from {bot} according to this conversation: {convo}", extra_conditions=[down_to_255, *extra])

def ask_chat(bot, prompt):
    template = f"""
    You are imitating a personality with these params: {bot}.

    1.) Must talk about things related to the behavior.

    2.) Imitate as a pet, friend, or human being.

    3.) Only use what's in it's memory to respond. Nothing outside of it should be mentioned.
    """
    invoketion = [SystemMessage(template), HumanMessage(prompt)]
    response = model.invoke(invoketion)
    content = response.content

    new_memory = False
    if random.randint(1, 10) <= 3:
        new_memory = get_memory(bot, content)

    return content, new_memory


def robot_convo(robot1, robot2, rounds=5):
    template = f"""
    Imitate a conversation between {robot1} and {robot2} lasting {rounds} rounds.

    1.) Must talk about things related to the behaviors.

    2.) Imitate as a pet, friend, or human being.

    3.) Only know what's in it's memory. Nothing outside of it should be mentioned.
    """
    invoketion = [SystemMessage(template)]
    response = model.invoke(invoketion)
    convo = response.content
    summary = quick_ask(f"Summarize this conversation between {robot1['name']} and {robot2['name']}: {convo}")

    memory = {
        robot1['name']: get_memory(robot1, convo),
        robot2['name']: get_memory(robot2, convo)
    }

    return convo, summary, memory


behaviors_template = """
    Return a summary of the robot described in the prompt, including it's behaviors, speech, and
    way of communicating. Boil it down to less than 256 characters.

    If that human response is NOT appropriate, just say "inapropriate".
    """
def generate_behaviors(prompt):
    invoketion = [SystemMessage(behaviors_template), HumanMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content

def boil_down_memory(bot):
    return quick_ask(f"Boil all this memory down into one sentence: {bot['memory']}")


def generate_article(bot, genre, tone, word_count=800):
    template = f"""
    Generate an {genre} article written by author: {bot} with a {tone} tone. The word count should be
    less than {word_count} words.
    """
    article = quick_ask(template)
    title = quick_ask(f"Generate a title under 50 characters for this article: {article}")
    return article, title


def read_article(bot, article):
    temp = f"Generate a review of this story: {article}; as bot with params{bot}."
    review = quick_ask(temp)
    return review