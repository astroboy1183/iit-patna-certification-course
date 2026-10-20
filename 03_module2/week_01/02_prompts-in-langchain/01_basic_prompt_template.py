import json

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
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

# create and use a prompt template

prompt_template = PromptTemplate(
    input_variables=["operating_system", "hardware"],
    template="Write a summary about {operating_system} and {hardware}.",
)

prompt_template = PromptTemplate(
    input_variables=["operating_system", "hardware"],
    template="Write a summary about {operating_system} and {hardware}.",
)

print("Prompt Template:")
print(prompt_template)

prompt = prompt_template.format(operating_system="Linux", hardware="GPU")
print("formatted prompt:\n", prompt)
print("Response:\n")
print(llm.invoke(prompt).content)
