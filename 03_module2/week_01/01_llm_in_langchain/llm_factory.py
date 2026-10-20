import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

with open("config.json", "r") as f:
    config = json.load(f)

provider = config["provider"]


def get_llm():
    if provider == "openai":
        llm = ChatOpenAI(
            model=config["openai"]["model"],
            temperature=config["openai"]["temperature"],
            top_p=config["openai"]["top_p"],
            max_tokens=config["openai"]["max_tokens"],
        )
        return llm
    elif provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=config["gemini"]["model"],
            temperature=config["gemini"]["temperature"],
            top_p=config["gemini"]["top_p"],
            max_tokens=config["gemini"]["max_tokens"],
        )
        return llm
    else:
        raise ValueError("Invalid provider in config.json")
