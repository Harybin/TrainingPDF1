import json

def load_data(filepath: str):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(filepath: str, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
