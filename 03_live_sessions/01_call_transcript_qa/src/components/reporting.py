from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from src.utils.config_loader import load_config

config = load_config()


class FinalReport(BaseModel):
    summary: str = Field(description="Summary of the call")
    recommendation: list[str] = Field(description="List of actionable improvements")


def get_final_report_chain(llm):
    final_parser = PydanticOutputParser(pydantic_object=FinalReport)

    final_prompt = PromptTemplate(
        template="""
        You are a QA Manager reviewing customer support calls.

        Based on the evaluation results below, generate:
        1. A concise summary of the agent's performance.
        2. A list of actionable recommendations for improvement. 
    
        Evaluation Data:
        {evaluation_outputs}

        Important: 
        1. Be specific and Practical
        2. Focus on the most important points
        3. Do not repeat scores
        4. Focus on improvement

        {format_instructions}   
        """,
        input_variables=["evaluation_outputs"],
        partial_variables={
            "format_instructions": final_parser.get_format_instructions(),
            "labels": config["classification"]["labels"],
        },
    )

    final_chain = final_prompt | llm | final_parser
    return final_chain
