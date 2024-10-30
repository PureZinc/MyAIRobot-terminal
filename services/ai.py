from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config.config import OPENAI_API_KEY


model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=OPENAI_API_KEY)

def quick_ask(prompt):
    invoketion = [SystemMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content

def ask_chat(bot, prompt):
    template = f"""
    Imitate how {bot} would respond to "{prompt}".

    1.) Must talk about possible interests based on the behavior

    2.) Imitate as a pet, friend, or human being.

    3.) Only know what's in it's memory. Nothing outside of it should be mentioned.
    """
    invoketion = [SystemMessage(template)]
    response = model.invoke(invoketion)
    return response.content


def robot_convo(robot1, robot2, rounds=5):
    rob1_response = ""
    rob2_response = f"Hi! I'm {robot2['name']}!"
    convo = []
    for round in range(rounds):
        if round%2==0:
            rob1_response = ask_chat(robot1, rob2_response)
            convo.append(f"{robot1['name']}: {rob1_response}")
        else:
            rob2_response = ask_chat(robot2, rob1_response)
            convo.append(f"{robot2['name']}: {rob2_response}")
    summary = quick_ask(f"Summarize this conversation between {robot1['name']} and {robot2['name']}: ")

    return convo, summary


behaviors_template = """
    Return a list separated by , of the personality of a robot according to the human response given.
    The response should go into detail on the behavior of the robot.

    If that human response is NOT appropriate, just say "inapropriate".
    """
def generate_behaviors(prompt):
    invoketion = [SystemMessage(behaviors_template), HumanMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content
