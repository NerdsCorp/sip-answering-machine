import json
import os

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/config.json"))

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=4)
