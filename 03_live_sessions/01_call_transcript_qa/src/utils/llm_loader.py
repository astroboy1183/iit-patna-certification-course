import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from src.utils.config_loader import load_config

config = load_config()


def load_llm(llm):
    provider = os.getenv("LLM_PROVIDER")
    if provider is None:
        raise ValueError("LLM_PROVIDER not in environment")

    provider = provider.lower()

    if provider == "openai":
        llm = ChatOpenAI(
            model=config["llm"].get("openai_model", "gpt-4o-mini"),
            temperature=config["llm"].get("temperature", 0.3),
        )
    elif provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=config["llm"].get("gemini_model", "gemini-1.5-flash"),
            temperature=config["llm"].get("temperature", 0.3),
        )
    else:
        raise ValueError("LLM_PROVIDER")
    return llm
