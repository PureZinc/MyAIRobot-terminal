from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


OPENAI_API_KEY = "sk-e1dewt6Mxl5VtBJv72tso86OAMfWHC8JeZYPYfHHIUT3BlbkFJ7QoKvjaj9Pc49U9vKPIiLKFC5rnXuBp_vYPBBBXS4A"

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=OPENAI_API_KEY)

template = """
You are responsible for building and forming the personalities of Robots built by 
users. In your memory, you will hold the behavior and personality of the robot and
control the behavior and the speech of that Robot according to those parameters.

According to added parameters in a robot's behavior, personality, and memory, you will:
1.) Imitate the robot's speech and use of language
2.) Hint towards the robots hobbies, interests, and things it doesn't like
"""
def ask_chat(prompt, params=None):
    invoketion = [SystemMessage(template)]
    if params:
        for param in params:
            invoketion.append(SystemMessage(param))
    invoketion.append(HumanMessage(prompt))
    response = model.invoke(invoketion)
    return response.content


behaviors_template = """
    Return a list separated by , of the personality of a robot according to the human response given.
    The response should go into detail on the behavior of the robot.

    If that human response is NOT appropriate, jsut say "inapropriate".
    """
def generate_behaviors(prompt):
    invoketion = [SystemMessage(behaviors_template), HumanMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content
