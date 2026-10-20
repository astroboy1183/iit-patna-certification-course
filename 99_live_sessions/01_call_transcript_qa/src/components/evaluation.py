from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from src.utils.config_loader import load_config

config = load_config()
min_score, max_score = config["evaluation"]["score_range"]


class ToneEvaluationOutput(BaseModel):
    tone_empathy_score: int = Field(
        description=f"Tone and empathy score between {min_score} and {max_score}",
        ge=min_score,
        le=max_score,
    )
    justification: str = Field(description="Short reason for the score")


def get_tone_chain(llm):
    tone_parser = PydanticOutputParser(pydantic_object=ToneEvaluationOutput)

    # prompt template
    tone_prompt = PromptTemplate(
        template="""
        You are a quality assurance assistant for a customer support team.

        Evaluate the agent's tone and empathy in the following customer support transcript.
        Check whether the agent was polite, acknowledged the customer's feelings, and stayed calm and respectful.

        Score it from {min_score} (poor) to {max_score} (excellent).

        Transcript:
        {transcript}

        {format_instructions}
        """,
        input_variables=["transcript"],
        partial_variables={
            "format_instructions": tone_parser.get_format_instructions(),
            "min_score": min_score,
            "max_score": max_score,
        },
    )

    # chain

    tone_chain = tone_prompt | llm | tone_parser
    return tone_chain


class KnowledgeEvaluationOutput(BaseModel):
    knowledge_accuracy_score: int = Field(
        description=f"Knowledge accuracy score between {min_score} and {max_score}",
        ge=min_score,
        le=max_score,
    )
    justification: str = Field(description="Short reason for the score")


def get_knowledge_chain(llm):
    knowledge_parser = PydanticOutputParser(pydantic_object=KnowledgeEvaluationOutput)

    # prompt template
    knowledge_prompt = PromptTemplate(
        template="""
        You are a quality assurance assistant for an insurance customer support team.

        Evaluate the accuracy of the information the agent gave in the following customer support transcript.
        Check whether the agent's answers were correct, clear and relevant to the customer's question,
        and whether the agent avoided guessing or giving misleading information.

        Score it from {min_score} (poor) to {max_score} (excellent).

        Transcript:
        {transcript}

        {format_instructions}
        """,
        input_variables=["transcript"],
        partial_variables={
            "format_instructions": knowledge_parser.get_format_instructions(),
            "min_score": min_score,
            "max_score": max_score,
        },
    )

    # chain

    knowledge_chain = knowledge_prompt | llm | knowledge_parser
    return knowledge_chain


class ResolutionEvaluationOutput(BaseModel):
    resolution_quality_score: int = Field(
        description=f"Resolution quality score between {min_score} and {max_score}",
        ge=min_score,
        le=max_score,
    )
    issue_resolved: bool = Field(
        description="True if the customer's issue was fully resolved in the call, otherwise False"
    )
    justification: str = Field(description="Short reason for the score")


def get_resolution_chain(llm):
    resolution_parser = PydanticOutputParser(pydantic_object=ResolutionEvaluationOutput)

    # prompt template
    resolution_prompt = PromptTemplate(
        template="""
        You are a quality assurance assistant for a customer support team.

        Evaluate how well the agent resolved the customer's issue in the following customer support transcript.
        Check whether the agent understood the problem, gave a clear solution or next steps, and whether the issue was actually resolved.

        Score it from {min_score} (poor) to {max_score} (excellent).

        Transcript:
        {transcript}

        {format_instructions}
        """,
        input_variables=["transcript"],
        partial_variables={
            "format_instructions": resolution_parser.get_format_instructions(),
            "min_score": min_score,
            "max_score": max_score,
        },
    )

    # chain

    resolution_chain = resolution_prompt | llm | resolution_parser
    return resolution_chain
