import json
import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
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
    "You are a concise and helpful assistant.\n"
    "Here’s a summary of the chat so far: {history}\n"
    "Now respond to the user message: {input}\n"
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

print("\nCUSTOMER SUPPORT CHAT — SUMMARY MEMORY (Modern API)")
print("Type 'exit' or 'quit' to end.\n")
print("----------------------------------------")

session_id = "summary_session"

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("\nChat ended. Thanks for testing!")
        break

    if not user_input:
        continue

    response = chain_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}},
    )

    print(f"Assistant: {response}\n")

    history = get_session_history(session_id)
    if len(history.messages) >= 8:
        summarizer = (
            ChatPromptTemplate.from_template(
                "Summarize the following conversation in 2-3 concise sentences:\n{conversation}"
            )
            | llm
            | StrOutputParser()
        )
        convo_text = "\n".join(
            [f"{m.type.upper()}: {m.content}" for m in history.messages]
        )
        summary = summarizer.invoke({"conversation": convo_text})
        store[session_id] = InMemoryChatMessageHistory()
        store[session_id].add_ai_message(f"Conversation Summary: {summary}")
        print("\nConversation summarized to maintain concise memory.\n")

history = get_session_history(session_id)
for msg in history.messages:
    role = "USER" if msg.type == "human" else "ASSISTANT"
    print(f"{role}: {msg.content}")
