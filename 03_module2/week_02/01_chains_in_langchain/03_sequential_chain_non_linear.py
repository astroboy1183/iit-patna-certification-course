import json

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
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

product_description = """
Introducing the new EcoBrew Smart Coffee Maker — an energy-efficient device
that brews coffee via a smartphone app. It supports WiFi connectivity,
custom brew settings, and eco-friendly pods made from biodegradable materials.
Ideal for modern homes and sustainable coffee lovers.
"""

feature_prompt = PromptTemplate(
    input_variables=["description"],
    template=(
        "Extract the 5 key product features from the following description:\n\n"
        "{description}\n\nReturn as a bullet list."
    ),
)
feature_chain = feature_prompt | llm | parser

ad_prompt = PromptTemplate(
    input_variables=["description"],
    template=(
        "Write a short, catchy advertisement for this product (max 3 sentences). "
        "Highlight its unique qualities:\n\n{description}"
    ),
)
ad_chain = ad_prompt | llm | parser

seo_prompt = PromptTemplate(
    input_variables=["description"],
    template=(
        "Generate 10 SEO-friendly keywords or hashtags for this product. "
        "Return as a comma-separated list.\n\n{description}"
    ),
)
seo_chain = seo_prompt | llm | parser

multi_chain = RunnableParallel(
    {
        "features": feature_chain,
        "ad_copy": ad_chain,
        "seo_tags": seo_chain,
        "original_input": RunnablePassthrough(),  # rint(printspecial LangChain utility that simply "passes through" the input it receives, without any processing.
    }
)


def combine_results(results: dict) -> str:
    """Combine all outputs into a structured final summary."""
    final_report = f"""
 PRODUCT INTELLIGENCE REPORT
-------------------------------
Original Input:
{results["original_input"]}

Key Features:
{results["features"]}

Ad Copy:
{results["ad_copy"]}

SEO Keywords:
{results["seo_tags"]}
"""
    return final_report.strip()


print("Non-Linear Sequential Chain — Product Intelligence System\n")

results = multi_chain.invoke({"description": product_description})
final_output = combine_results(results)
print(results)
print(final_output)
print("\nNon-linear sequential chain executed successfully!\n")

print("📘 PROCESS OVERVIEW")
print("""
Parallel branches:
  - Extracts structured product features
  - Generates creative ad copy
  - Produces SEO keywords
Then merges results into a unified marketing intelligence report.
""")
