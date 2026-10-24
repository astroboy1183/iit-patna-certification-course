import json

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

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


# Define output schema using pydantic
class ReviewAnalysis(BaseModel):
    title: str = Field(
        description="A short description title summarizing the review content."
    )
    summary: str = Field(
        description="A concise 2-3 sentence summary of the customer's opinion."
    )
    sentiment: str = Field(
        description="The sentiment of the review (positive, negative, or neutral)."
    )


parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)
format_instructions = parser.get_format_instructions()
# print(format_instructions)

# Define review input and prompt
customer_review = """
I recently bought the new Galaxy X smartphone, and I'm genuinely impressed!
The camera quality is stunning, and the battery lasts all day.
However, the phone feels a bit bulky and slippery.
Still, overall, it's one of the best Android phones I've used in years.
"""

prompt_template = PromptTemplate(
    input_variables=["review"],
    template=(
        "Extract the key information from the following customer review.\n"
        "Follow the structure below exactly:\n"
        "{format_instructions}\n"
        "Customer Review: {review}\n"
    ),
    partial_variables={"format_instructions": format_instructions},
)

formatted_prompt = prompt_template.format(review=customer_review)
response = llm.invoke(formatted_prompt)
print(f"Raw output: \n {response.content}")

print("clean output:")
try:
    parsed_output = parser.parse(response.content)
    print(json.dumps(parsed_output.model_dump(), indent=4))
except Exception as e:
    print(f"Parsing error: {e}")
