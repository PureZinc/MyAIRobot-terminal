import json
from .files import currentfile

def unload_current_data():
    with open(currentfile, "r") as f:
        data = json.load(f)  
    return data

def save_current_data(current):
    with open(currentfile, "w") as f:
        json.dump(current, f, indent=4)

