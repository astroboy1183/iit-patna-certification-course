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

direct_template = PromptTemplate(
    input_variables=["question"],
    template="Question: {question}",
)
cot_template = PromptTemplate(
    input_variables=["question"],
    template="Let's think step by step before answering.\n{question}\n"
    "Now give the final answer concise.",
)
questions = [
    "If a bat and ball costs $1.10 in total and the bat costs $1 more than the ball, how much does the ball cost?",
    "if 5 machines take 5 minutes to make 5 widgets, how long will it take for 100 machines to make 100 widgets?",
]


def run_and_print(formatted_prompt: str):
    try:
        response = llm.invoke(formatted_prompt)
        if hasattr(response, "content"):
            return response.content
        else:
            return str(response)
    except Exception as e:
        return "Invocation error:", e


for i, q in enumerate(questions):
    print(f"\n==========Question {i + 1}=========: {q}")
    formatted_direct_prompt = direct_template.format(question=q)
    direct_answer = run_and_print(formatted_direct_prompt)
    print(f"Direct Answer: {direct_answer}")
    print("\nCOT answer: ")
    formatted_cot_prompt = cot_template.format(question=q, answer=direct_answer)
    cot_answer = run_and_print(formatted_cot_prompt)
    print(f"COT Answer: {cot_answer}")
