import json

from dotenv import load_dotenv
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
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


# few shot examples

examples = [
    {"input": "What is the capital of France?", "output": "Paris"},
    {"input": "What is the capital of Italy?", "output": "Rome"},
    {"input": "What is the capital of Germany?", "output": "Berlin"},
    {"input": "What is the capital of England?", "output": "London"},
    {"input": "What is the capital of Spain?", "output": "Madrid"},
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"], template="{input} -----> {output}\n"
)
# print(example_prompt)

few_shot = FewShotPromptTemplate(
    input_variables=["input"],
    prefix="Answer in exactly the same format as the examples: the country , "
    "then '------->', then answer. ",
    suffix="What is the capital of {input}? ",
    example_prompt=example_prompt,
    examples=examples,
)
# print(few_shot)
print(llm.invoke(few_shot.format(input="India")).content)
