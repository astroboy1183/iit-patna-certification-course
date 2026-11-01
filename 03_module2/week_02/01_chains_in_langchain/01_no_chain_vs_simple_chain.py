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

customer_feedback = """
I recently bought the new Galaxy X smartphone, and I'm genuinely impressed!
The camera quality is stunning, and the battery lasts all day.
However, the phone feels a bit bulky and slippery.
Still, overall, it's one of the best Android phones I've used in years.
"""
manual_prompt = """Summarize the following feedback in 2-3 sentences.
Highlight the positives and negatives clearly

Feedback: 
{customer_feedback}
"""

print("=========")

print("Manual LLM call without chain")

manual_response = llm.invoke(manual_prompt.format(customer_feedback=customer_feedback))
print(manual_response.content.strip())

print("=========================")


print("Chain based LLM call")

prompt_template = PromptTemplate(
    input_variables=["customer_feedback"],
    template="Summarize the following feedback in 2-3 sentences.\n"
    "Highlight the positives and negatives clearly\n"
    "Feedback:\n"
    "{customer_feedback}",
)

chain = prompt_template | llm
response = chain.invoke({"customer_feedback": customer_feedback})
print(response.content.strip())
print("=========================")
