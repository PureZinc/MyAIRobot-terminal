import os

base_dir = os.path.dirname(__file__)

datafile = os.path.join(base_dir, "../database/db/data.json") # The path to the database
currentfile = os.path.join(base_dir, "../database/db/current.json") # Holds your current data 

OPENAI_API_KEY = "<YOUR_OPENAI_API_KEY>"
