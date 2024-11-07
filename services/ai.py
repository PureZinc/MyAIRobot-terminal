from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config.config import OPENAI_API_KEY


model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=OPENAI_API_KEY)

def quick_ask(*prompts):
    invoketion = [*[SystemMessage(prompt) for prompt in prompts]]
    response = model.invoke(invoketion)
    return response.content

def human_ask(prompt, extra_conditions=[]):
    invoketion = [*[SystemMessage(extra) for extra in extra_conditions], HumanMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content

behaviors_template = """
    Return a summary of the robot described in the prompt, including it's behaviors, speech, and
    way of communicating. Boil it down to less than 255 characters.

    If that human response is NOT appropriate, just say "inapropriate".
    """
def generate_behaviors(prompt):
    invoketion = [SystemMessage(behaviors_template), HumanMessage(prompt)]
    response = model.invoke(invoketion)
    return response.content
