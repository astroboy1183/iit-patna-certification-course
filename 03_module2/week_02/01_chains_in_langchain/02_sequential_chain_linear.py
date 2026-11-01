import json

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
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

parser = StrOutputParser()

customer_complaint = """
I'm having a problem with your product. I've been using it for a few months and it's not working as expected."""

# Step 1 : summarize

summarize_prompt = PromptTemplate(
    input_variables=["complaint"],
    template="Summarize the following customer complaint: {complaint}",
    output_parser=parser,
)

summarize_chain = summarize_prompt | llm | parser

# step 2: Sentiment

sentiment_prompt = PromptTemplate(
    input_variables=["summary"],
    template="Determine the sentiment of the following summary in only one word - Positive, negative and neutral: {summary}\n",
    output_parser=parser,
)

sentiment_chain = sentiment_prompt | llm | parser

# Step 3 : rewrite professionally

rewrite_prompt = PromptTemplate(
    input_variables=["summary", "sentiment"],
    template=""" Rewrite the following summary in a professional tone (add sentiment tag in the end in brackets) and a {sentiment} tone:\n{summary}\n""",
    output_parser=parser,
)

rewrite_chain = rewrite_prompt | llm | parser


def process_complaint(complaint: str) -> str:
    summary = summarize_chain.invoke({"complaint": complaint})
    sentiment = sentiment_chain.invoke({"summary": summary})
    return rewrite_chain.invoke({"summary": summary, "sentiment": sentiment})


print("========Sequential chain on customer complaint workflow==========")

result = process_complaint(customer_complaint)
print(result)
print("=================================================================")
