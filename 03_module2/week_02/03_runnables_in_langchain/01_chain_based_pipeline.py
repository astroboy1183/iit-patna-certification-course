import json
import os

from dotenv import load_dotenv
from langchain.chains import LLMChain, SequentialChain
from langchain_core.prompts import PromptTemplate
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

# step 1

topic_prompt = PromptTemplate(
    input_variables=["interest"],
    template="Suggest a creative blog title idea related to the topic: {interest}",
)
topic_chain = LLMChain(llm=llm, prompt=topic_prompt, output_key="title")

# step 2

outline_prompt = PromptTemplate(
    input_variables=["title"],
    template="Write a short outline for the blog titled: {title}",
)

outline_chain = LLMChain(llm=llm, prompt=outline_prompt, output_key="outline")

# combine with sequential chain

blog_pipeline = SequentialChain(
    chains=[topic_chain, outline_chain],
    input_variables=["interest"],
    output_variables=["title", "outline"],
    verbose=True,
)

print("Old-School Pipeline - Without using Runnables\n\n")
print("Generates a blog topic and an outline based on your interest.\n")
user_interest = input("Enter your area of interest:").strip()
result = blog_pipeline.invoke({"interest": user_interest})

print(f"Blog Title:{result['title']}")
print(f"Blog Outline:{result['outline']}")
print("\n" + "=" * 80 + "\n")
