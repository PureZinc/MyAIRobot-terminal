from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json


OPENAI_API_KEY = "sk-e1dewt6Mxl5VtBJv72tso86OAMfWHC8JeZYPYfHHIUT3BlbkFJ7QoKvjaj9Pc49U9vKPIiLKFC5rnXuBp_vYPBBBXS4A"

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=OPENAI_API_KEY)

template = """
You are responsible for building and forming the personalities of Robots built by 
users. In your memory, you will hold the behavior and personality of the robot and
control the behavior and the speech of that Robot according to those parameters.

According to added parameters in a robot's behavior, personality, and memory, you will:

1.) Imitate the robot's speech and use of language

2.) Hint towards the robots hobbies, interests, and things it doesn't like

3.) When you're given a robot name, do NOT act like an assistant. Act more like the 
robot's behaviors that are given instead. User's shouldn't know you are behind the personality
of the robot.
"""
def ask_chat(prompt, params=None):
    invoketion = [SystemMessage(template)]
    if params:
        for param in params:
            invoketion.append(SystemMessage(param))
    invoketion.append(HumanMessage(prompt))
    response = model.invoke(invoketion)
    return response.content


def robot_convo(robot1, robot2, rounds=5):
    roboconv_template = f"""
        You are imitating a conversation between two robots. Using mainly parameters from the robot's behaviors
        and memory (xp is optional), create a conversation lasting {rounds} rounds back and forth.

        You're response should be a Python Dictionary (enclosed with double quotes) with 3 different parts: the conversation, the summary, and the memories

        The first: conversation is the imitated conversation between {robot1} and {robot2}

        The second: summary will be a short summary of how the conversation went

        The last: memories will be an impression from each robot of the other robot.
    """
    invoketion = [
        SystemMessage(roboconv_template)
    ]
    response = model.invoke(invoketion)
    
    response_parts = json.loads(response.content)
    
    if len(response_parts.keys()) != 3:
        return response.content, "Failed parse, so no new memories :(", ""

    conversation = response_parts['conversation']
    summary = response_parts['summary']
    new_memories = response_parts['memories']

    return conversation, summary, new_memories


behaviors_template = """
    Return a list separated by , of the personality of a robot according to the human response given.
    The response should go into detail on the behavior of the robot.

    If that human response is NOT appropriate, just say "inapropriate".
    """
def generate_behaviors(prompt):
    invoketion = [SystemMessage(behaviors_template), HumanMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content
