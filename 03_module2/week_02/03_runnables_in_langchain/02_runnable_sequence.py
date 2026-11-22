import json
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
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

# step 1: generate title
title_chain = (
    PromptTemplate.from_template(
        "Suggest a creative blog title idea related to {interest}."
    )
    | llm
    | StrOutputParser()
)

# step 2: generate blog post
outline_chain = (
    PromptTemplate.from_template("Write a blog post about {title}.")
    | llm
    | StrOutputParser()
)

# Build runnable pipeline

blog_pipeline = (
    RunnablePassthrough().assign(title=title_chain).assign(outline=outline_chain)
)

print("New-School Pipeline - Using Runnables\n\n")
print("Generates a blog topic and an outline based on your interest.\n")
user_interest = input("Enter your area of interest:").strip()
result = blog_pipeline.invoke({"interest": user_interest})

print(f"Blog Title:{result['title']}")
print(f"Blog Outline:{result['outline']}")
print("\n" + "=" * 80 + "\n")
