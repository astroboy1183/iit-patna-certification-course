import json
import os

from dotenv import load_dotenv


def load_config(config_path: str = "config/config.json"):
    load_dotenv()
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file '{config_path}' not found.")
    with open("config/config.json", "r") as f:
        config = json.load(f)

    return config
