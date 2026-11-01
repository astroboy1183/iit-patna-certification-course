"""
04_token_buffer_memory.py (Modern LangChain Version)
----------------------------------------------------
Concept: Chatbot with Token-Limited Memory

Purpose:
Show how to maintain conversation memory within a token limit
using LangChain’s modern Runnable + MessageHistory architecture.

LangChain Concept:
RunnableWithMessageHistory + token counting (manual control).
"""

import json
import os
from typing import List

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from tiktoken import get_encoding

load_dotenv()

with open("config.json", "r") as f:
    config = json.load(f)

provider = config["provider"]
cfg = config[provider]

if provider == "openai":
    llm = ChatOpenAI(
        model=cfg.get("model"),
        temperature=cfg.get("temperature", 0.6),
        max_tokens=cfg.get("max_tokens", 250),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
else:
    llm = ChatGoogleGenerativeAI(
        model=cfg.get("model"),
        temperature=cfg.get("temperature", 0.6),
        max_output_tokens=cfg.get("max_output_tokens", 250),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant.\n"
    "Conversation so far (trimmed to fit token limit): {history}\n"
    "User: {input}\n"
    "Assistant:"
)

base_chain = prompt | llm | StrOutputParser()

TOKEN_LIMIT = 250
encoding = get_encoding("cl100k_base")  # for GPT-like tokenization
store = {}


def num_tokens_from_messages(messages: List[str]) -> int:
    """Roughly estimate token count from text messages."""
    return sum(len(encoding.encode(m)) for m in messages)


def get_session_history(session_id: str):
    """Return or create a session, trimming history by token budget."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    history = store[session_id]

    total_tokens = num_tokens_from_messages([m.content for m in history.messages])
    while total_tokens > TOKEN_LIMIT and len(history.messages) > 2:
        history.messages = history.messages[2:]
        total_tokens = num_tokens_from_messages([m.content for m in history.messages])

    return history


chat_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

print("\nCUSTOMER SUPPORT CHAT — TOKEN-LIMITED MEMORY (Modern API)")
print(f"(Keeps memory within ~{TOKEN_LIMIT} tokens)")
print("Type 'exit' or 'quit' to end.\n")
print("----------------------------------------")

session_id = "token_session"

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("\nChat ended. Thanks for testing!")
        break

    if not user_input:
        continue

    response = chat_chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}},
    )

    print(f"Assistant: {response}\n")

    history = get_session_history(session_id)
    total_tokens = num_tokens_from_messages([m.content for m in history.messages])
    print(f"[Approx. {total_tokens} tokens stored in memory]\n")


# Final Memory Dump
print("----------------------------------------")
print("Final Token-Limited Memory:\n")

for msg in get_session_history(session_id).messages:
    role = "USER" if msg.type == "human" else "ASSISTANT"
    print(f"{role}: {msg.content}")
