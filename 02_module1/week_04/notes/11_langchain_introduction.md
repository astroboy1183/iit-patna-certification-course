# Lecture 11 · LangChain introduction (Week 4)

The first framework lecture. It starts with the problems we hit when calling LLM APIs by hand, then introduces LangChain and its building blocks at a glance. Each building block gets its own lecture next (12–18), so this note is the map, not the territory.

## Life before LangChain

Until now the flow has been: **write the prompt as a string → send it to the provider's API → get text back → parse it yourself.** That works for one call. It breaks as soon as the app grows.

| Pain point | What it looks like in practice |
|---|---|
| **Spaghetti logic** | `prompt = "..."; response = llm(prompt)` turns into nested conditionals, copy-pasted prompt strings and endless string concatenation once memory, multiple steps or tools are added |
| **Provider lock-in** | Every provider has its own client, request format and response shape, so switching models means rewriting code |
| **Messy context and memory** | Old messages are appended to a list by hand; the prompt grows until it overflows the context window, and there's no clean way to mix short-term history with long-term or vector-search recall |
| **Hard to chain steps** | Query → retrieve context → generate → summarize/store: each step is another prompt variable, another `llm()` call and more ad-hoc glue |
| **Unstructured output** | You want JSON, the model returns a paragraph, and you write fragile parsing code |
| **Poor tool integration** | Every API, database or local function is wired up by hand, with no standard way to tell the model when to use which tool |
| **No observability** | You can't see which prompt produced which answer, or the latency and token usage per step; debugging means `print()` |

The slide's example of the spaghetti problem is two chained calls glued together with f-strings: summarize a text, then generate a question from the summary. It works, but what if step 1 fails, how do you reuse it in another project, and how do you trace it? There's no standard way to orchestrate or debug it.

### My own "before" code

My Week 2 projects show these problems first-hand:

- [`02_chatbot/llm_provider.py`](../../week_02/02_chatbot/llm_provider.py) wraps OpenAI and Gemini behind one `chat()` method, but only with an `if/elif` per provider: different clients (`OpenAI` vs `genai.GenerativeModel`), different calls (`chat.completions.create` vs `generate_content`) and different response fields (`choices[0].message.content` vs `.text`). Adding a third provider means a third branch everywhere. That's **provider lock-in**.
- [`03_capstone/app.py`](../../week_02/03_capstone/app.py) keeps the whole conversation in `st.session_state["history"]` and resends all of it every turn, so the prompt grows without limit. In [`llm_providers.py`](../../week_02/03_capstone/llm_providers.py) the Gemini path has to flatten that history into a `"role: content"` string, because the two APIs expect different message formats. That's **manual memory** plus **provider lock-in**.

> **Why this pain is useful:** having built these by hand, we know *why* orchestration frameworks exist. LangChain brings **structure, reusability and observability** to LLM apps, much as Django and Flask did for web development (see [Lecture 10](10_progress_summary_and_learning_recap.md)).

## What LangChain is

**LangChain** is an open-source framework (Python and JavaScript) for building applications powered by LLMs. Think of it as a **backend framework for LLM apps**: the missing infrastructure between an idea and a production-ready app.

It does **not** give you a new model. It gives you:
- **standard interfaces**: one way to call any chat model, format any prompt or parse any output;
- **composition**: small components joined into pipelines with the `|` operator;
- **integrations**: hundreds of ready-made connectors for model providers, vector stores, document loaders and tools;
- **agents**: models that decide which tool to call, and when.

## Pain point → LangChain solution

The slide maps each pain point to a LangChain feature. I've added the current (1.x) names and where each is covered:

| Pain point | Slide's answer | What it is in LangChain 1.x | Covered in |
|---|---|---|---|
| Provider lock-in | (lecture write-up) one model interface | Chat model classes (`ChatOpenAI`, `ChatGoogleGenerativeAI`, …), `init_chat_model` | [12_models_in_langchain.md](12_models_in_langchain.md) |
| Messy prompt logic | Chains, prompt templates | `PromptTemplate`, `ChatPromptTemplate` | [13_prompt_engineering_in_langchain.md](13_prompt_engineering_in_langchain.md) |
| Unstructured output | (lecture write-up) output parsers | Output parsers, `with_structured_output` | [14_structured_output_and_output_parsers.md](14_structured_output_and_output_parsers.md) |
| Multi-step tasks | Sequential / parallel chains | Pipelines built with `\|` (LCEL), `RunnableParallel` | [15_chains_in_langchain.md](15_chains_in_langchain.md), [17_runnables_in_langchain.md](17_runnables_in_langchain.md) |
| Manual context handling | Memory (ConversationBuffer, VectorStore, …) | Message history, or a LangGraph checkpointer for agents | [16_memory_in_langchain.md](16_memory_in_langchain.md) |
| Bringing in your own data | Embedding models | Embeddings, vector stores, retrievers | [18_introduction_to_rag.md](18_introduction_to_rag.md) |
| No API/DB integration | Tools & agents | `@tool` + `create_agent` | Later module |
| Debugging nightmare | LangSmith | LangSmith tracing | Below |

The common thread: every piece has **clear input and output boundaries**, so pieces can be swapped and reused instead of rewritten.

## The ecosystem today

LangChain is no longer one big package. It's a family of packages, so you install only what you use:

| Package | What's in it |
|---|---|
| `langchain-core` | The base abstractions: messages, prompt templates, output parsers, the Runnable interface and `\|`. Small, with few dependencies |
| `langchain` | The high-level layer: `create_agent`, `init_chat_model`, middleware. Built on `langchain-core` and LangGraph |
| `langchain-openai`, `langchain-google-genai`, `langchain-anthropic`, `langchain-ollama`, … | One **integration package per provider**, e.g. `ChatOpenAI`, `ChatGoogleGenerativeAI`, `OpenAIEmbeddings` |
| `langchain-community` | Community-maintained integrations that have no dedicated package |
| `langchain-text-splitters` | Splitting documents into chunks (used in RAG) |
| `langchain-classic` | Legacy pre-1.0 code (`LLMChain`, `ConversationBufferMemory`, old agents), kept for backwards compatibility |
| **LangGraph** (`langgraph`) | Lower-level orchestration for stateful, multi-step agents (loops, branching, persistence) |
| **LangSmith** (`langsmith`) | Tracing, debugging and evaluation (a hosted service with a free tier, plus an open-source SDK) |

My live-session project uses `langchain` 1.4, `langchain-core` 1.6, `langchain-openai` 1.6 and `langchain-google-genai` 4.4.

> **Correction to the slide:** the slides (and many online tutorials) are written for LangChain 0.x. The project moved fast: **0.1** (Jan 2024) split out `langchain-core` and `langchain-community`, **0.2** (May 2024) moved integrations into partner packages, **0.3** (Sep 2024) moved to Pydantic 2, and **1.0** (Oct 2025) slimmed `langchain` down to agents and models and moved the legacy chains and memory classes into `langchain-classic`. In my 1.x environment, old imports such as `from langchain.chains import LLMChain` and `from langchain.memory import ConversationBufferMemory` fail with `ModuleNotFoundError`. When a tutorial's import fails, check its version first.

## The core building blocks at a glance

| # | Block | Mental model | Example | Deep dive |
|---|---|---|---|---|
| 1 | **Models** | A black-box function: messages in, message out | `ChatOpenAI`, `OpenAIEmbeddings` | [12](12_models_in_langchain.md) |
| 2 | **Prompts** | A parameterized template: `f(topic) → prompt` | `PromptTemplate.from_template(...)` | [13](13_prompt_engineering_in_langchain.md) |
| 3 | **Structured output** | Text → schema → clean object | `PydanticOutputParser` | [14](14_structured_output_and_output_parsers.md) |
| 4 | **Runnables** | One pipeline step with a standard interface | anything with `.invoke()` | [17](17_runnables_in_langchain.md) |
| 5 | **Chains** | A sequence of runnables: step 1 → step 2 → step 3 | `prompt \| model \| parser` | [15](15_chains_in_langchain.md) |
| 6 | **Memory** | A context store: current input + past history | message history | [16](16_memory_in_langchain.md) |
| 7 | **Tools & agents** | Tools are the hands; the agent is the mind deciding when to use them | `@tool`, `create_agent` | Later module |
| 8 | **LangSmith** | A flight recorder for every run | tracing via environment variables | Below |

### 1 · Models

LangChain wraps every provider behind the same interface, so you can **switch models without rewriting the core logic**. The slide lists three kinds: LLMs, chat models and embedding models (which turn text into vectors for similarity search in RAG).

> **Correction to the slide:** the slide files GPT, Claude and Gemini under "LLMs (text-based models)" and chat models separately. In LangChain, **"LLM" classes are the older text-in, text-out completion interface**; GPT, Claude and Gemini are all used through **chat models** (messages in, an `AIMessage` out), which is what `ChatOpenAI` and `ChatGoogleGenerativeAI` are. New code should use chat models; the plain LLM classes are mostly legacy.

### 2 · Prompt templates

Prompts define *how the model should think*. A template turns a hard-coded f-string into a reusable object with named variables.

> **Correction to the slide:** the slide writes `PromptTemplate("Translate {text} to French")`. In current LangChain that raises `TypeError`, because `PromptTemplate` only takes keyword arguments. Use:
> ```python
> from langchain_core.prompts import PromptTemplate
>
> prompt = PromptTemplate.from_template("Translate {text} to French")
> print(prompt.format(text="I love learning"))   # Translate I love learning to French
> ```

### 3 · Structured output

LLMs return free text, and automation needs data. An **output parser** adds format instructions to the prompt and turns the reply into a Python object (or raises an error if the shape is wrong). My live-session project uses `PydanticOutputParser` so that every classification comes back as an object with `call_type` and `confidence`.

### 4 and 5 · Runnables and chains

Every component (prompt, model, parser) is a **Runnable**: it has `.invoke()`, `.batch()` and `.stream()`. Because they share one interface, they snap together with `|`, like Unix pipes. The result is a **chain**: one reusable object you can call, test and trace as a unit. Chains create structured workflows instead of one-off API calls, e.g. input → summarizer → translator → output.

> **Correction to the slide:** the slide's "Sequential / Parallel Chains" refers to old classes such as `LLMChain` and `SequentialChain`. Those now live only in `langchain-classic`. Current LangChain builds the same pipelines with the `|` operator (the LangChain Expression Language, LCEL) and `RunnableParallel`.

### 6 · Memory

LLMs are **stateless**: each call knows only what's in that request. Memory adds past conversation to the next prompt, so the chat feels continuous. The slide lists buffer memory (recent turns), summary memory (older turns compressed into a summary) and vector-store memory (relevant past turns found by semantic search); the lecture write-up adds window memory (only the last *k* turns).

> **Correction to the slide:** `ConversationBufferMemory`, `ConversationSummaryMemory` and the vector-store one (whose real name is `VectorStoreRetrieverMemory`, not `VectorStoreMemory`) are **legacy classes**, deprecated and moved to `langchain-classic`. In LangChain 1.x, chat history is kept as a list of messages (optionally wrapped with `RunnableWithMessageHistory` from `langchain-core`), and agents persist it with a LangGraph **checkpointer** such as `InMemorySaver`. The ideas (buffer, window, summary, vector recall) are unchanged; only the classes are different.

### 7 · Tools and agents

Real apps need actions, not just text: searching, querying a database, calling an API. A **tool** is a function the model is allowed to call; an **agent** is a model in a loop that decides which tool to call, reads the result and repeats until it can answer. Example: user query → decide to search → summarize the results → reply. Together they turn a static chatbot into a problem-solver.

> **Correction to the slide:** older LangChain built agents with `initialize_agent` / `AgentExecutor`. In LangChain 1.x those are gone from `langchain`; the standard way is `from langchain.agents import create_agent`, called as `create_agent(model, tools=[...], system_prompt=...)`, which runs on LangGraph under the hood.

### 8 · LangSmith

A tracing and debugging platform. It records every run of a chain or agent: each step's inputs and outputs, the exact prompt sent, latency and token usage. That makes it easy to find the weak step or the prompt that needs work. It's switched on with environment variables (`LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY`), with no code changes, and it also works for apps that don't use LangChain.

## How it all fits together

The lecture write-up ends with the complete pipeline:

```
User input → Prompt template → Chat model → Output parser → (Memory update) → answer
                  ↑                                               │
                  └──────────── past history fed back in ─────────┘
```

Here's the slide's spaghetti example (summarize, then generate a question) rewritten as a chain:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# To try it offline, with no API key:
# from langchain_core.language_models.fake_chat_models import FakeListChatModel
# model = FakeListChatModel(responses=["<a summary>", "<a question>"])

summarize = (
    ChatPromptTemplate.from_template("Summarize this text in two sentences:\n{text}")
    | model
    | StrOutputParser()
)
ask = (
    ChatPromptTemplate.from_template("Write one quiz question about this summary:\n{summary}")
    | model
    | StrOutputParser()
)

# The dict runs `summarize` and passes its output on as "summary".
chain = {"summary": summarize} | ask
print(chain.invoke({"text": "LangChain is an open-source framework for building LLM apps..."}))
```

Compared with the f-string version: each step is a named, reusable object; swapping `ChatOpenAI` for `ChatGoogleGenerativeAI` changes one line; `chain.batch([...])` runs many inputs; and with LangSmith on, every step is traced.

### Before and after in my own code

My [call-transcript QA project](../../../03_live_sessions/01_call_transcript_qa) is the "after" picture:

| Problem in my Week 2 code | How the live-session project solves it with LangChain |
|---|---|
| `if/elif` per provider in `llm_provider.py`, with different calls and response fields | [`src/utils/llm_loader.py`](../../../03_live_sessions/01_call_transcript_qa/src/utils/llm_loader.py) still picks the provider, but returns `ChatOpenAI` or `ChatGoogleGenerativeAI`, and everything downstream treats them the same |
| Prompts as f-strings | [`src/components/classification.py`](../../../03_live_sessions/01_call_transcript_qa/src/components/classification.py) uses `PromptTemplate` with `partial_variables` for the labels and format instructions |
| Reading `.text` or `choices[0].message.content` and hoping it's the right shape | `PydanticOutputParser` returns a validated `ClassificationOutput` object |
| Glue code between steps | `prompt \| llm \| parser`, then a router and separate evaluation and report chains |

One thing I learnt along the way: in [`experiment.ipynb`](../../../03_live_sessions/01_call_transcript_qa/experiment.ipynb) I rebuilt `prompt | llm | parser` inside the loop for every transcript. In `src/pipeline/inference.py` the chains are built **once** (`build_chains`) and reused. A chain is a reusable object, not a function call, so build it once and invoke it many times.

What's still missing is memory: the project is single-turn, and the capstone's hand-rolled history is what [Lecture 16](16_memory_in_langchain.md) replaces.

> **Takeaway:** LangChain doesn't make the model smarter. It standardizes everything *around* the model (models, prompts, outputs, steps, memory, tools, tracing) so LLM apps are built from small, swappable parts instead of one-off glue code.

## Check yourself

1. Name four problems you hit when calling LLM APIs directly, and point to where at least one shows up in your Week 2 code.
2. What is the difference between `langchain-core`, `langchain` and `langchain-openai`? Why was the library split into separate packages?
3. In LangChain, what's the difference between an "LLM" class and a chat model? Which kind is `ChatOpenAI`?
4. Why does `prompt | model | parser` work? What do all three objects have in common?
5. A tutorial uses `from langchain.memory import ConversationBufferMemory` and it fails on your machine. Why, and what are your options?
6. What does LangSmith show you that `print()` debugging doesn't?
