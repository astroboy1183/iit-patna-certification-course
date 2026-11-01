import json

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
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

parser = StrOutputParser()

messages = [
    "My order arrived late and one item was missing.",
    "Can you share your enterprise pricing plans?",
    "I’m getting an authentication error while using your API.",
]

support_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "You are a customer support assistant.\n"
        "Respond professionally to this issue and suggest a resolution.\n\nMessage:\n{message}"
    ),
)

support_chain = support_prompt | llm | parser

sales_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "You are a sales representative.\n"
        "Respond warmly, providing pricing and feature details.\n\nMessage:\n{message}"
    ),
)

sales_chain = sales_prompt | llm | parser

tech_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "You are a technical support engineer.\n"
        "Provide a concise troubleshooting step or explanation.\n\nMessage:\n{message}"
    ),
)

tech_chain = tech_prompt | llm | parser

router_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "Classify this message into one of these categories:\n"
        "1. Support\n2. Sales\n3. Technical\n\n"
        "Message:\n{message}\n\n"
        "Only return the category name."
    ),
)

router_chain = router_prompt | llm | parser

router = RunnableBranch(
    (
        lambda x: "support" in x.lower(),
        support_chain,
    ),
    (
        lambda x: "sales" in x.lower() or "pricing" in x.lower(),
        sales_chain,
    ),
    (
        lambda x: "technical" in x.lower()
        or "api" in x.lower()
        or "error" in x.lower(),
        tech_chain,
    ),
    RunnablePassthrough(),
)


def process_message(msg):
    """Route message to the correct chain"""
    print("Incoming message\n")
    print(msg)
    print("*" * 20)
    category = router_chain.invoke({"message": msg})
    response = router.invoke(category)

    print("Routed category:", category)
    print("Response:", response)
    print("*" * 20)


for msg in messages:
    process_message(msg)
