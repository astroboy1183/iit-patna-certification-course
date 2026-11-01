import json
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
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


def clean_text(raw_text):
    text = raw_text.strip()
    text = re.sub(r"\s+", " ", text)
    text.replace("pls", "please").replace("u", "you").replace("thx", "thanks")
    return text


preprocess = RunnableLambda(clean_text)

prompt = PromptTemplate(
    input_variables=["cleaned_text"],
    template=(
        "You are a friendly customer support assistant.\n"
        "Given the cleaned message below, write a polite, clear, and helpful reply.\n\n"
        "Customer Message:\n{cleaned_text}"
    ),
)
core_chain = prompt | llm | parser


def postprocess(response, original_text):
    clean_response = response.strip().replace("\n\n", "\n")
    meta = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_message": original_text,
        "response": response,
        "word_count": len(clean_response.split()),
    }
    return json.dumps(meta, indent=2)


postprocess_chain = RunnableLambda(
    lambda output: postprocess(output["response"], output["input"])
)


def process_email(email_text):
    cleaned = preprocess.invoke(email_text)
    response = core_chain.invoke({"cleaned_text": cleaned})
    final_result = postprocess_chain.invoke({"response": response, "input": email_text})
    return final_result


emails = [
    "Hey, i orderd a phone last week but not yet arrived. pls help!",
    "thx for the update but can u speed up the refund?",
    "hi i recieved wrong color shoes what can i do?",
]

for e in emails:
    print("Original email:\n", e)
    print("*" * 50)
    output = process_email(e)
    print(output)
    print("*" * 50)
