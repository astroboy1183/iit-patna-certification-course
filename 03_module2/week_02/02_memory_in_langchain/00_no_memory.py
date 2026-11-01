import json
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

with open("config.json", "r") as f:
    config = json.load(f)

provider = config["provider"]
cfg = config[provider]

if provider == "openai":
    llm = ChatOpenAI(
        model=cfg.get("model"),
        temperature=cfg.get("temperature", 0.5),
        max_tokens=cfg.get("max_tokens", 250),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
else:
    llm = ChatGoogleGenerativeAI(
        model=cfg.get("model"),
        temperature=cfg.get("temperature", 0.5),
        max_output_tokens=cfg.get("max_output_tokens", 250),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_template(
    "You are a friendly and professional customer support assistant.\n"
    "User message: {user_message}\n"
    "Respond politely and helpfully."
)

chain = prompt | llm | parser

print("=======Customer support chat - no memory=======")
print("Type 'exit' or 'quit' to end")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Chat ended....\n")
        break
    if not user_input:
        print("Please enter a valid question or message for the bot.")
        continue

    response = chain.invoke({"user_message": user_input})
    print(f"Bot: {response}\n")
