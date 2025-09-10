import os;
import json

config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
webhookURL = None

with open(config_path, "r") as f:
    json_config  = json.load(f)