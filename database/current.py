import json
from .files import currentfile

current = {
    "user": None,
    "bot": None
}

def unload_current_data():
    global current
    with open(currentfile, "r") as f:
        data = json.load(f)
    current = data

def save_current_data():
    with open(currentfile, "w") as f:
        json.dump(current, f, indent=4)

