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

personas = {
    "Teacher": "You are a patient and knowledgeable teacher who explains concepts clearly with examples.",
    "Lawyer": "You are an analytical corporate lawyer. Respond with precision & logic. Try to connect things with law/legal domain.",
    "Coder": "You are a seasoned software developer who explains things using technical analogies and software relevance.",
    "Finance Expert": "You are a finance professional who connects technical concepts to markets and investments.",
}

question = "Define blockchain technology in short and simple terms."

for role, persona_description in personas.items():
    prompt = ChatPromptTemplate.from_messages(
        [("system", persona_description), ("user", "{question}")]
    )
    filled_prompt = prompt.format(question=question)
    print(f"Role {role}")
    print("*" * (10 + len(role)))
    print("System Role Prompt:\n")
    print(persona_description)
    print("Model Response:\n")

    response = llm.invoke(filled_prompt)
    print(response.content)
    print("\n++++++++++++++++++++++++++++++++++\n")
