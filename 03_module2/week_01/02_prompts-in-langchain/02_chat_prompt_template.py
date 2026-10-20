import json

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

with open("config.json", "r") as f:
    config = json.load(f)

provider = config["provider"]

if provider == "openai":
    llm = ChatOpenAI(
        model=config["openai"]["model"],
        temperature=config["openai"]["temperature"],
        top_p=config["openai"]["top_p"],
        max_tokens=config["openai"]["max_tokens"],
    )
elif provider == "gemini":
    llm = ChatGoogleGenerativeAI(
        model=config["gemini"]["model"],
        temperature=config["gemini"]["temperature"],
        top_p=config["gemini"]["top_p"],
        max_tokens=config["gemini"]["max_tokens"],
    )
else:
    raise ValueError("Invalid provider in config.json")

# create chat prompt template

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that translates English to Hindi."),
        ("human", "{input}"),
        ("ai", "{ai_response}"),
    ]
)

final_chat_prompt = chat_prompt.format(input="I love programming", ai_response="")

response = llm.invoke(final_chat_prompt)
print(response.content)
