import json
from .files import currentfile

def unload_current_data():
    with open(currentfile, "r") as f:
        data = json.load(f)  
    return data

def save_current_data(current):
    with open(currentfile, "w") as f:
        json.dump(current, f, indent=4)

def set_current_data(key, value):
    current = unload_current_data()
    current[key] = value
    save_current_data(current)

def get_current_data(key):
    current = unload_current_data()
    return current[key]
