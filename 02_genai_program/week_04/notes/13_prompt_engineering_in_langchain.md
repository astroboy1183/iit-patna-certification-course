# Lecture 13 · Prompt engineering in LangChain (Week 4)

## What prompt engineering is

Prompt engineering is more than writing clever instructions. The aim is LLM output that is **relevant, reliable and reproducible**.

The lecture's framing: treat a prompt as **API design**, where the "API" is a large neural model that reads natural language.

| Designing an API | Designing a prompt |
|---|---|
| Input parameters | Template variables (`{transcript}`, `{language}`) |
| Expected output format | Format instructions / an output schema |
| Error handling | Validation and parsing of the reply, retries |

The basics (zero-shot vs few-shot, prompting vs fine-tuning) are in [Lecture 7](../../week_03/notes/07_prompt_tuning_vs_fine_tuning.md). This lecture is about doing it **in code**, with LangChain.

## Why it matters

LLMs are general-purpose: they write code, summarise, translate and answer questions. They are also **sensitive to context and fragile under ambiguity**: a small change in wording can change the output a lot.

| Vague | Specific |
|---|---|
| "Summarise the following text." | "Summarise the following text in 3 bullet points, each under 15 words, focusing only on key facts." |

The second prompt pins down format, length and focus, so the output is easier to check and more consistent from run to run.

## The problem with ad-hoc prompting

The usual first attempt builds the prompt by string concatenation:

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
llm = FakeListChatModel(responses=["A short summary."])  # stand-in for any chat model
article_text = "LangChain is a framework for building LLM apps..."

prompt = "Summarize this article: " + article_text
response = llm.invoke(prompt)
```

> **Correction to the slide:** the slide calls the model as `llm(prompt)`. Calling a model object directly was removed in LangChain 1.x (it raises `TypeError: ... object is not callable`); use `llm.invoke(prompt)`, which returns an `AIMessage` whose text is in `.content` (see [Lecture 12](12_models_in_langchain.md)).

This works until:
- you move to another model whose API has different syntax;
- you add parameters such as tone, language or length;
- you need to know which prompt version performed better;
- several developers edit the same prompts.

Then you end up with copy-pasted strings everywhere, no structure, and no way to test or version prompts. LangChain's prompt templates address this.

## Designing prompt systems

### `PromptTemplate`: single-turn text prompts

A string template with named `{placeholders}`, filled in at run time:

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("Write a concise {language} summary about {topic}.")
template.input_variables                      # ['language', 'topic']  (detected automatically)

prompt = template.format(topic="machine learning", language="English")
# 'Write a concise English summary about machine learning.'
```

> **Correction to the slide:** the slide imports `from langchain.prompts import PromptTemplate`. That module does not exist in LangChain 1.x (`ModuleNotFoundError`); prompts live in `langchain_core.prompts`. The slide's constructor, `PromptTemplate(input_variables=[...], template="...")`, still works, but `PromptTemplate.from_template("...")` is shorter and reads the variables from the string, so the list can't drift out of sync with the text.

`.format(...)` returns a plain string. `.invoke({...})` returns a `PromptValue`, which is what a model expects when the template is piped into it (`template | llm`). A missing variable raises a `KeyError` instead of silently sending `{topic}` to the model.

### `ChatPromptTemplate`: role-based prompts for chat models

Chat models take a list of **messages with roles**:

| Role (tuple shorthand) | Becomes | Purpose |
|---|---|---|
| `"system"` | `SystemMessage` | Sets the model's behaviour or persona |
| `"human"` or `"user"` | `HumanMessage` | The user's query |
| `"ai"` or `"assistant"` | `AIMessage` | Earlier model replies, or worked examples (optional context) |

```python
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly English tutor."),
    ("human", "Translate this sentence to French: {sentence}"),
])

messages = chat_template.format_messages(sentence="I love learning.")
# [SystemMessage('You are a friendly English tutor.'),
#  HumanMessage('Translate this sentence to French: I love learning.')]
```

The slide uses `("user", ...)`; LangChain accepts both `"user"` and `"human"`. To keep a running conversation, add a `MessagesPlaceholder("history")` between the system and human messages ([Lecture 16](16_memory_in_langchain.md)).

### `SystemMessagePromptTemplate`: the persona

The system message defines **who the model is**: its persona, expertise and rules. It stays the same across queries, which is what keeps behaviour consistent. Example: *"You are a financial analyst. You answer only with factual and professional explanations."*

```python
from langchain_core.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate,
)

system = SystemMessagePromptTemplate.from_template(
    "You are a {role}. You answer only with factual and professional explanations."
)
analyst = ChatPromptTemplate.from_messages([
    system,
    HumanMessagePromptTemplate.from_template("{question}"),
])
analyst.format_messages(role="financial analyst", question="What is a bond?")
```

This builds exactly the same messages as the tuple form `("system", "You are a {role}. ...")`. The explicit classes still exist in `langchain_core.prompts`, but current docs mostly use the shorter tuples. Making the role a variable lets one template serve many personas.

### Partial variables: fill some values in advance

Some values are known when the template is built, not when it is called. `partial_variables` (or `.partial(...)`) fixes them up front, so callers supply only what changes:

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Classify into one of: {labels}\n\nTranscript:\n{transcript}",
    input_variables=["transcript"],
    partial_variables={"labels": "billing, claims, complaint, general_query"},
)
prompt.input_variables                       # ['transcript']
prompt.format(transcript="I was charged twice.")
```

### Gotcha: literal braces

Templates use f-string syntax, so every `{...}` is read as a variable. A JSON example written straight into the template breaks it:

```python
from langchain_core.prompts import PromptTemplate

# PromptTemplate.from_template('Return JSON like {"label": "billing"} for: {text}')
#   .format(text="x")  ->  KeyError: '"label"'

ok = PromptTemplate.from_template('Return JSON like {{"label": "billing"}} for: {text}')
ok.format(text="x")      # 'Return JSON like {"label": "billing"} for: x'
```

Double the braces (`{{ }}`) for literal text. Braces inside variable **values** are safe, because values are inserted, not re-parsed. That is why JSON format instructions are passed in as a variable rather than typed into the template.

## From writing prompts to designing prompt systems

| Stop thinking | Start thinking |
|---|---|
| "How do I write this prompt?" | "How do I design a reusable, testable, scalable prompt system for my app?" |

What LangChain adds:
- **Parameterised prompts:** templates with variables.
- **Reuse across LLMs:** the same template pipes into `ChatOpenAI` or `ChatGoogleGenerativeAI`.
- **Composition:** templates plug into chains, agents and RAG pipelines (`prompt | llm | parser`, [Lecture 15](15_chains_in_langchain.md)).
- **Evaluation and versioning** with LangSmith (LangChain's tracing and evaluation platform), which can store prompts with version history and compare their results on test datasets.

## Common prompt engineering patterns

| Pattern | Idea | In LangChain |
|---|---|---|
| **Few-shot** | Teach by example: show input → output pairs before the real input | `FewShotChatMessagePromptTemplate` |
| **Chain-of-thought** | Ask the model to reason step by step before answering | An instruction in the system or human message |
| **Role prompting** | Give the model a persona and context | The system message |
| **Structured output** | Ask for a fixed format (e.g. JSON) so code can parse it reliably | Format instructions + output parsers, or `with_structured_output` ([Lecture 14](14_structured_output_and_output_parsers.md)) |

Patterns stack. Role + few-shot, for example:

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [
    {"input": "I was charged twice this month.", "output": "billing"},
    {"input": "My claim has been pending for weeks.", "output": "claims"},
]
example_prompt = ChatPromptTemplate.from_messages([("human", "{input}"), ("ai", "{output}")])
few_shot = FewShotChatMessagePromptTemplate(examples=examples, example_prompt=example_prompt)

classifier_prompt = ChatPromptTemplate.from_messages([
    ("system", "You classify customer support messages as billing, claims, complaint "
               "or general_query. Reply with the label only."),   # role
    few_shot,                                                        # examples
    ("human", "{input}"),
])
classifier_prompt.format_messages(input="Your agent was rude to me.")
# System, then Human/AI pairs for each example, then the new Human message
```

Each example becomes a human → AI exchange, so the model sees the pattern as earlier turns of the conversation. Chain-of-thought combines with structured output in the same way: "think step by step, then give the final answer on its own last line as `Answer: <number>`" lets you parse the last line.

> **Note:** current "reasoning" models already work through problems internally before replying, so an explicit "think step by step" adds less there than it does with standard chat models.

The slide's point: with templates, parsers and system prompts together, the LLM becomes a **predictable module** with a defined input and output, rather than a black box.

## Developer mindset checkpoint

> "Prompts aren't instructions anymore; they're **interfaces** between you and the LLM."

The best prompt engineers think in systems, not only in wording:

| Building block | Gives you |
|---|---|
| Variables | Dynamic context |
| Templates | Reusable components |
| Patterns | Predictable reasoning |

## In my project

The call-transcript QA project ([`src/components/`](../../../03_live_sessions/01_call_transcript_qa/src/components/), first built in [`experiment.ipynb`](../../../03_live_sessions/01_call_transcript_qa/experiment.ipynb)) uses most of this lecture:
- **Templates, not concatenation:** each task (classification, tone, knowledge, resolution, final report) has its own `PromptTemplate` with a `{transcript}` or `{evaluation_outputs}` variable.
- **Role prompting:** every template opens with a persona, e.g. "You are a quality assurance assistant for a customer support team." (written inside a single `PromptTemplate`, not a separate system message).
- **Partial variables:** [`classification.py`](../../../03_live_sessions/01_call_transcript_qa/src/components/classification.py) fills `labels` from `config.json`, and [`evaluation.py`](../../../03_live_sessions/01_call_transcript_qa/src/components/evaluation.py) fills `min_score` / `max_score`, so the chain is invoked with just the transcript.
- **Structured output:** `format_instructions` comes from `PydanticOutputParser.get_format_instructions()` and is passed as a partial variable, so its JSON braces don't clash with the template syntax.
- **Reuse across models:** the same `prompt | llm | parser` chains run on OpenAI or Gemini, depending on `LLM_PROVIDER`.

Possible next steps from this lecture: add two or three labelled transcripts as few-shot examples to the classifier, and move the persona lines into system messages with `ChatPromptTemplate`.

> **Takeaway:** treat prompts like code. Parameterise them with templates, give the model a role in the system message, show examples when the format matters, and keep them in version control so they can be tested and compared.

## Check yourself

1. Give two problems with building prompts by string concatenation in a team project.
2. What is the difference between `template.format(...)` and `template.invoke(...)`? Which one does a chain use?
3. When would you use `ChatPromptTemplate` instead of `PromptTemplate`? What do the `system`, `human` and `ai` roles each do?
4. Why does `PromptTemplate.from_template('Return {"label": "x"} for {text}')` fail, and what are two ways to fix it?
5. What are `partial_variables` for? Give an example from the transcript QA project.
6. Write a few-shot chat prompt that turns product reviews into `positive` / `negative` labels, with a role in the system message.
