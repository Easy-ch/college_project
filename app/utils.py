import json

def load_services():
    with open("data/popular_services.json", "r", encoding="utf-8") as file:
        return json.load(file)