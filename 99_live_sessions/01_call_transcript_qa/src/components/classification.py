from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


class ClassificationOutput(BaseModel):
    call_type: str = Field(description="Type of customer call")
    confidence: float = Field(description="Confidence score between 0 and 1")


def get_classification_prompt(llm, config):
    parser = PydanticOutputParser(pydantic_object=ClassificationOutput)

    # prompt template
    prompt = PromptTemplate(
        template="""
        You are called classification assistant. 

        classify the following customer support transcript into one of the categories:
        {labels}

        Transcript:
        {transcript}

        {format_instructions}   
        """,
        input_variables=["transcript"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "labels": config["classification"]["labels"],
        },
    )
    classification_chain = prompt | llm | parser
    return classification_chain
