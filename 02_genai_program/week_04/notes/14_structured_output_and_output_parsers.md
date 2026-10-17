# Lecture 14 · Structured output and output parsers (Week 4)

## The problem: free text doesn't plug into code

An LLM answers in prose by default. That's fine for a human reader, but a program can't reliably pull fields out of a sentence.

| | Example | Can code use it directly? |
|---|---|---|
| **Unstructured** (human-readable) | `The customer is happy and recommends the product. Rating: 5/5.` | ❌ No: you'd need fragile string matching |
| **Structured** (machine-readable) | `{"sentiment": "positive", "rating": 5, "recommendation": true}` | ✅ Yes: parse, store in a database, pass to the next step |

Unstructured text breaks automation pipelines because it can't be parsed, stored or handed to other systems with any confidence.

## Where it matters

| Use case | Fields to extract |
|---|---|
| Resume parsing | name, skills, `experience_years` |
| Customer support | intent, urgency, category |
| Finance | transaction details from invoice text |
| Agents | state that must survive across steps (needed for multi-step reasoning) |

The slide's key idea: structured output turns an LLM from a **chatbot** into a **data engine**.

## Two ways to get structured output

| Approach | How it works | When |
|---|---|---|
| **Native, model-side**: `.with_structured_output(schema)` | LangChain sends the schema to the provider's API (JSON-schema response format or tool calling), so the model is constrained or steered **while generating** | The model/provider supports it (most current chat models do) |
| **LangChain output parsers** | The schema is described in the **prompt text** (format instructions); the model's text reply is parsed and validated **afterwards** | The model has no native support, or you want the prompt-only route |

## Which models support native structured output

The slide's table says: OpenAI `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` ✅; legacy `gpt-3.5-turbo` ❌ (use parsers); Gemini `gemini-1.5-pro`/`-flash` ✅ (JSON mode); legacy `gemini-pro` partial.

> **Correction to the slide:** the table mixes up two different OpenAI features and is now out of date.
> - **Tool (function) calling** is supported by `gpt-3.5-turbo` and `gpt-4-turbo`, so `with_structured_output(Schema, method="function_calling")` works with them. They are not limited to parsers.
> - **Strict JSON-schema "Structured Outputs"** only exists on `gpt-4o-mini`, `gpt-4o-2024-08-06` and later models. In `langchain-openai` 1.x the default method is `"json_schema"` (I checked the signature on my installed 1.6.7), so with older models pass `method="function_calling"`.
> - `gemini-pro` and the Gemini 1.5 models have been retired by Google. Current Gemini models support structured output through `ChatGoogleGenerativeAI(...).with_structured_output(...)`. (My own QA project config still defaults to `gemini-1.5-flash`, so that needs updating.)
> - More generally, `with_structured_output()` works on any LangChain chat model that supports tool calling (Anthropic, Mistral, many Ollama models), not only OpenAI and Gemini.

## Native structuring: `with_structured_output()`

You hand the model a schema; it returns data in that shape instead of an `AIMessage`.

| Schema format | You get back | Validated? | Best for |
|---|---|---|---|
| **TypedDict** (standard library) | a `dict` | ❌ No | Lightweight, simple cases |
| **Pydantic model** | a Pydantic object | ✅ Yes (types, `Literal`, `ge`/`le`…) | Most production code |
| **JSON Schema** (a plain dict) | a `dict` | ❌ No | Sharing one schema with web services or other languages |

```python
from typing import Literal
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class Classification(BaseModel):
    """Classify a customer support call."""
    call_type: Literal["billing", "claims", "complaint", "general_query"]
    confidence: float = Field(ge=0, le=1, description="Confidence between 0 and 1")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(Classification)

result = structured_llm.invoke("Classify this call: 'I was charged twice this month.'")
# result is a Classification object, e.g. Classification(call_type='billing', confidence=0.93)
```

(I built this offline on my installed versions; the `invoke` itself needs an API key.)

Useful options:
- `include_raw=True` returns `{"raw": AIMessage, "parsed": ..., "parsing_error": ...}`, so a bad reply doesn't raise and you can log it.
- `method=` picks the mechanism: `"json_schema"` (strict, OpenAI default), `"function_calling"`, or `"json_mode"`.
- The docstring and `Field(description=...)` are sent to the model, so write them as instructions.

## LangChain output parsers

Used when the model can't enforce a schema itself. A parser does two jobs: `get_format_instructions()` produces text to paste into the prompt, and `parse()` turns the reply back into Python data.

| Parser | Returns | Validates types? | Use when |
|---|---|---|---|
| `StrOutputParser` | plain `str` (the message content) | n/a | You only need clean text (e.g. a summary) |
| `JsonOutputParser` | `dict` / `list` | ❌ No | You need JSON-like data quickly, no strict validation |
| `StructuredOutputParser` + `ResponseSchema` | `dict` of strings | ❌ No | Legacy: named fields with descriptions |
| `PydanticOutputParser` | Pydantic object | ✅ Yes | Strongly typed pipelines with validation logic |

> **Correction to the slide:** the class is `JsonOutputParser` (not `JSONOutputParser`), and it doesn't *enforce* strict JSON: it extracts and parses JSON from the reply (tolerating ```` ```json ```` fences, and partial JSON while streaming). Nothing checks the fields unless you validate them yourself. Also, `StructuredOutputParser` / `ResponseSchema` are no longer in `langchain` 1.x: along with other legacy code they moved to the separate `langchain-classic` package. Every field it describes is a string, so prefer `PydanticOutputParser` (or `with_structured_output`) for new code. All the parsers in the table above except `StructuredOutputParser` import from `langchain_core.output_parsers`.

### PydanticOutputParser in a chain

The pattern from my live-session project ([`src/components/classification.py`](../../../03_live_sessions/01_call_transcript_qa/src/components/classification.py)), runnable offline with a fake model:

```python
from typing import Literal
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

class Classification(BaseModel):
    call_type: Literal["billing", "claims", "complaint", "general_query"]
    confidence: float = Field(ge=0, le=1, description="Confidence between 0 and 1")

parser = PydanticOutputParser(pydantic_object=Classification)
prompt = PromptTemplate(
    template="Classify this support call.\n\n{transcript}\n\n{format_instructions}",
    input_variables=["transcript"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Fake model returning a canned reply; swap in ChatOpenAI(model="gpt-4o-mini") for real use.
llm = FakeListChatModel(responses=['{"call_type": "billing", "confidence": 0.92}'])

chain = prompt | llm | parser
print(chain.invoke({"transcript": "I was charged twice this month."}))
# call_type='billing' confidence=0.92
```

`get_format_instructions()` inserts the model's JSON schema plus an example into the prompt. If the reply isn't valid JSON, or fails Pydantic validation, `parse()` raises `OutputParserException`.

### Lessons from my call-transcript QA project

Two real bugs from [`experiment.ipynb`](../../../03_live_sessions/01_call_transcript_qa/experiment.ipynb) show why the schema's types matter:

| Bug | Cause | Fix |
|---|---|---|
| `OutputParserException` on the final report | The model returned `"recommendation": ["…", "…"]` (a JSON list) but the field was typed `str` | Type the field as `list[str]` ([`src/components/reporting.py`](../../../03_live_sessions/01_call_transcript_qa/src/components/reporting.py)) |
| Off-list labels slip through | `call_type: str` accepts any string, e.g. `"refund"`; my router's `else` branch then quietly treats it as a general query | Use `Literal["billing", "claims", "complaint", "general_query"]` so a wrong label fails at parse time |

```python
from langchain_core.exceptions import OutputParserException

try:
    parser.parse('{"call_type": "refund", "confidence": 0.8}')
except OutputParserException as e:
    print("rejected:", type(e).__name__)   # Literal catches the off-list label
```

The rule: make the schema as strict as the downstream code expects. Bounds like `Field(ge=1, le=5)` (as in [`src/components/evaluation.py`](../../../03_live_sessions/01_call_transcript_qa/src/components/evaluation.py)) do the same job for scores.

## Repairing broken output: `OutputFixingParser`

- Even with format instructions, models sometimes return malformed JSON or the wrong shape.
- `OutputFixingParser` wraps another parser. When parsing fails, it sends the bad output, the error and the format instructions back to an LLM and asks for a corrected version.
- This matters in production, where one schema-breaking reply can stop a whole batch.

> **Correction to the slide:** in LangChain 1.x, `OutputFixingParser` (and `RetryOutputParser`) are no longer importable from `langchain`; they live in the `langchain-classic` package, which isn't installed in my project. The same idea can be built with `langchain-core` alone, by giving the parser a fallback that re-prompts the model:

```python
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables import RunnableLambda

# (continues from the PydanticOutputParser example above: reuses Classification, parser, prompt)
fix_prompt = PromptTemplate.from_template(
    "This output does not match the required format:\n\n{bad_output}\n\n"
    "{format_instructions}\nReturn only the corrected JSON."
)
llm = FakeListChatModel(responses=[
    "Sure! call_type: billing, confidence 0.9",         # first reply: not JSON
    '{"call_type": "billing", "confidence": 0.9}',       # repaired reply
])
repair = (
    RunnableLambda(lambda msg: {"bad_output": msg.content,
                                "format_instructions": parser.get_format_instructions()})
    | fix_prompt | llm | parser
)
safe_parser = parser.with_fallbacks([repair], exceptions_to_handle=(OutputParserException,))

chain = prompt | llm | safe_parser
print(chain.invoke({"transcript": "I was charged twice."}))   # call_type='billing' confidence=0.9
```

Simpler options: `chain.with_retry(stop_after_attempt=3)` just re-runs the call (often enough at temperature > 0), and `with_structured_output(..., include_raw=True)` lets you inspect failures without an exception.

## Which to use

| You want | Use |
|---|---|
| Schema-valid output from a modern chat model | `.with_structured_output(PydanticModel)` |
| Schema control for a model without native support | `PydanticOutputParser` (or `JsonOutputParser` if loose dicts are fine) |
| Validation plus automatic repair | `PydanticOutputParser` + a repair fallback (`OutputFixingParser` in `langchain-classic`) |
| Just text | `StrOutputParser` |

The slide calls `with_structured_output()` "clean, deterministic JSON". The **shape** is reliable; the **content** still depends on the model, so keep validating values that matter.

> **Takeaway:** prompts shape what the model says; schemas and parsers make it safe for code to use. Prefer `with_structured_output()` with a strict Pydantic model, and fall back to output parsers when the model can't do it natively.

Related: prompt templates and partial variables (Lecture 13, [`13_prompt_engineering_in_langchain.md`](13_prompt_engineering_in_langchain.md)); parsers as links in a chain (Lecture 15, [`15_chains_in_langchain.md`](15_chains_in_langchain.md)).

## Check yourself

1. Why does unstructured LLM output break an automation pipeline? Give one example from the use-case table.
2. How does `with_structured_output()` differ from `PydanticOutputParser` in *where* the schema is applied?
3. You call `with_structured_output()` on `gpt-4-turbo` and the request fails. What would you change?
4. Which parser would you choose for (a) a summary, (b) a quick loose dict, (c) a typed record written to a database? Why?
5. A field typed `str` received a JSON list and parsing failed. What are two ways to fix it, and which is better?
6. What does `OutputFixingParser` do, and how can you get the same behaviour with only `langchain-core`?
