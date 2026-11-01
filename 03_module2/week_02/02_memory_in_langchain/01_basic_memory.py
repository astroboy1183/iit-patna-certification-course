import json
import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory  # line 47
from langchain_core.output_parsers import StrOutputParser  # line 31
from langchain_core.prompts import ChatPromptTemplate  # line 33
from langchain_core.runnables.history import RunnableWithMessageHistory  # line 51
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
    "You are a friendly customer support assistant.\n"
    "Previous messages: {history}\n"
    "User: {input}\n"
    "Assistant:"
)

base_chain = prompt | llm | parser

store = {}


def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chain_with_memory = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

print("=======Customer support chat - with modern memory=======")
print("Type 'exit' or 'quit' to end")

session_id = "demo_session"

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Chat ended....\n")
        break
    if not user_input:
        print("Please enter a valid question or message for the bot.")
        continue

    response = chain_with_memory.invoke(
        {"input": user_input}, config={"configurable": {"session_id": session_id}}
    )

    print(f"Assistant: {response}\n")

print("**********************************")
print("Chat memory contents(Modern API)")

history = get_session_history(session_id)
for msg in history.messages:
    role = "USER" if msg.type == "human" else "ASSISTANT"
    print(f"{role}: {msg.content}")
