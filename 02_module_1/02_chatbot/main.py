import json
from json.decoder import JSONDecodeError

from dotenv import load_dotenv
from llm_provider import LLMProvider


def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file '{config_path}' not found.")
    except JSONDecodeError:
        raise JSONDecodeError(f"Invalid JSON in config file '{config_path}'.")


def run_chat():
    print(">>>>>Simple CLI Chatbot(type 'exit' to quit)<<<<<<")

    try:
        config = load_config()
        print(
            f"loaded config: {config['provider']} with model -> {config['models'][config['provider']]}"
        )
        bot = LLMProvider(config)
    except Exception as e:
        print(f"Initialization Error: {str(e)}")
        return
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye...")
            break
        if not user_input.strip():
            print("Please enter a valid question or message for the bot.")
            continue
        try:
            response = bot.chat(user_message=user_input)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"Chat Error: {str(e)}")


if __name__ == "__main__":
    load_dotenv()
    run_chat()
