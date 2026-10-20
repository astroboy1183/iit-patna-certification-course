import json
import os
import warnings

import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI

warnings.filterwarnings("ignore")

load_dotenv()

with open("config.json", "r") as f:
    config = json.load(f)

# OpenAI function


def run_openai(history):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=config["openai"].get("model", "gpt-4o-mini"),
        messages=history,
        max_tokens=config["openai"].get("max_tokens", 1000),
        temperature=config["openai"].get("temperature", 0.7),
        top_p=config["openai"].get("top_p", 0.9),
    )

    return response.choices[0].message.content.strip()


def run_gemini(message):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel(
        config["gemini"].get("model", "gemini-3.8-flash"),
        generation_config={
            "temperature": config["gemini"].get("temperature", 0.7),
            "top_p": config["gemini"].get("top_p", 0.9),
            "max_output_tokens": config["gemini"].get("max_tokens", 1000),
        },
    )
    response = model.generate_content(message)

    return response.text.strip()


# router function


def run_llm(history):
    provider = config["provider"]
    if provider == "openai":
        return run_openai(history)
    elif provider == "gemini":
        conversation_text = "\n".join(f"{m['role']}: {m['content']}" for m in history)
        return run_gemini(conversation_text)
    else:
        return "Error: Invalid provider in config.json"
