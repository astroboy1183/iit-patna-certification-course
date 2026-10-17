# Lecture 15 · Chains in LangChain (Week 4)

## Why chains exist

Most people start with plain calls glued together by hand:

```python
prompt = f"Summarize this article:\n\n{article_text}"
summary = llm.invoke(prompt).content
tweet = llm.invoke(f"Write a tweet based on: {summary}")
```

This works until you need error handling, a different model per step, memory, structured output, or a way to see what happened between steps. Then the script turns into spaghetti: hard to debug and hard to reuse in another project.

Chains fix this. They let you:
- **compose** several LLM calls into one workflow;
- **reuse** small, testable pieces (one for summarising, one for rewriting);
- slot in **memory, output parsing, routing or plain Python** between the LLM calls;
- **debug each link** on its own.

The slide's analogy: chains are **LEGO blocks for LLM logic**. Each block does one thing well, and blocks connect in many ways.

## What is a chain?

A chain is a sequence of calls (to an LLM, a tool or an ordinary function) linked together to do one task.

| Part | Example |
|---|---|
| **Inputs** | `{"topic": "AI"}` |
| **Intermediate steps** | build the prompt, call the LLM, transform the result |
| **Outputs** | `{"summary": "AI is transforming the world"}` |

The chain takes care of passing data between steps, lets one chain be used inside another, and hides the plumbing so you can think about the logic.

## The architecture of a chain

```
Inputs → Prompt template → LLM / Tool → Output parser → Outputs
e.g.  article text → "Summarise this article…" → GPT-4o → parser → summary
```

| Component | Role |
|---|---|
| **Prompt template** | Shapes the input into the message the model sees (Lecture 13) |
| **LLM or tool** | Does the work (Lecture 12) |
| **Output parser** | Turns raw text into a string or structured data (Lecture 14) |
| **Memory** (optional) | Carries context across runs (Lecture 16) |

Chains can also include **pre-processing** (clean the input), **post-processing** (format or validate the output) and **caching** of intermediate results.

The slide's example puts a "JSON parser" before "summary text". A JSON parser returns a dict; for plain text you'd use `StrOutputParser`.

## Core chain types (from the slide)

| Slide's chain type | What it does | Example | Modern LCEL equivalent |
|---|---|---|---|
| `LLMChain` | Prompt template + LLM | Summarisation | `prompt \| llm \| StrOutputParser()` |
| `SimpleSequentialChain` | One chain's single output becomes the next one's input | Blog → summary → tweet | `{"summary": chain_a} \| prompt_b \| llm \| parser` |
| `SequentialChain` | Like the above, but with several named inputs and outputs | Multi-document summaries | `RunnablePassthrough.assign(...)` |
| `RouterChain` | Sends each input to the right sub-chain | Routing customer queries | `RunnableBranch` or a routing function in `RunnableLambda` |
| Custom chains | Your own functions, parsing or API calls | Mixing structured and free-text tasks | `RunnableLambda` |

> **Correction to the slide:** `LLMChain`, `SimpleSequentialChain`, `SequentialChain` and the `RouterChain` family are legacy classes, superseded by LCEL from LangChain 0.1 onwards (`LLMChain` was formally deprecated in 0.1.17), and they are **not in `langchain` 1.x** at all. On my installed `langchain` 1.4.3, `from langchain.chains import LLMChain` raises `ImportError: No module named 'langchain.chains'`. The old classes now live in the separate `langchain-classic` package, for legacy code only. New code uses **LCEL** (the LangChain Expression Language): every prompt, model, parser and function is a *Runnable*, and the `|` operator joins them. The slide's point still holds (each piece is composable, and a chain can contain other chains); the LCEL versions are below.

## Building chains with LCEL

All snippets below run offline with a fake model (checked on langchain-core 1.6.6). Shared setup:

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# Offline stand-in that returns these replies in turn.
# For real calls: from langchain_openai import ChatOpenAI; llm = ChatOpenAI(model="gpt-4o-mini")
llm = FakeListChatModel(responses=["AI tools now draft, test and review code.",
                                   "AI now drafts, tests and reviews code. Are you ready? #AI"])
```

### Linear chain (replaces `LLMChain` and `SimpleSequentialChain`)

```python
summary_prompt = PromptTemplate.from_template("Summarise this article in two sentences:\n\n{article}")
tweet_prompt = PromptTemplate.from_template("Write a tweet based on this summary:\n\n{summary}")

summary_chain = summary_prompt | llm | StrOutputParser()                          # the old LLMChain
tweet_chain = {"summary": summary_chain} | tweet_prompt | llm | StrOutputParser()  # blog → summary → tweet

print(tweet_chain.invoke({"article": "Long article text..."}))
```

The dict `{"summary": summary_chain}` is shorthand for a `RunnableParallel`: it runs `summary_chain` and puts the result under the key the next prompt expects. `tweet_chain` is also a **nested chain**, since `summary_chain` sits inside it.

### Keeping every intermediate value (replaces `SequentialChain`)

```python
from langchain_core.runnables import RunnablePassthrough

blog_chain = (
    RunnablePassthrough.assign(summary=summary_chain)
    .assign(tweet=tweet_prompt | llm | StrOutputParser())
)
out = blog_chain.invoke({"article": "Long article text..."})
print(sorted(out))   # ['article', 'summary', 'tweet']
```

`assign` keeps the input keys and adds new ones, so the final dict has the article, the summary *and* the tweet.

### Branching: run chains in parallel

```python
from langchain_core.runnables import RunnableParallel

title_chain = PromptTemplate.from_template("Suggest a title for:\n{article}") | llm | StrOutputParser()
keyword_chain = PromptTemplate.from_template("List 5 keywords for:\n{article}") | llm | StrOutputParser()

seo_chain = RunnableParallel(title=title_chain, keywords=keyword_chain)
print(seo_chain.invoke({"article": "Long article text..."}))   # {'title': ..., 'keywords': ...}
```

Both branches get the same input and run concurrently.

### Router chain (replaces `RouterChain`)

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

tone_chain = PromptTemplate.from_template("Rate the agent's empathy:\n{transcript}") | llm | StrOutputParser()
knowledge_chain = PromptTemplate.from_template("Check the agent's facts:\n{transcript}") | llm | StrOutputParser()

router = RunnableBranch(
    (lambda x: x["call_type"] == "complaint", tone_chain),
    knowledge_chain,                                   # default branch
)
print(router.invoke({"call_type": "complaint", "transcript": "..."}))

# Equivalent: a plain function that returns the chain to run.
def pick_chain(x):
    return tone_chain if x["call_type"] == "complaint" else knowledge_chain

router2 = RunnableLambda(pick_chain)
```

When a `RunnableLambda` returns a Runnable, LangChain runs it with the same input. LangChain's docs now prefer this routing-function style over `RunnableBranch`.

### Hybrid chain: plain Python inside the chain

```python
clean = RunnableLambda(lambda x: {"article": " ".join(x["article"].split())})
hybrid = clean | summary_chain        # deterministic clean-up, then the LLM
print(hybrid.invoke({"article": "  lots   of\n\n  whitespace  "}))
```

## Common chain patterns

| Pattern | Idea | Example | LCEL building block |
|---|---|---|---|
| **Linear** | Each step's output feeds the next | Blog → summary → tweet | `\|` |
| **Branching** | Several chains in parallel | Title + keywords together | `RunnableParallel` |
| **Router** | Pick a sub-chain per input | FAQ bot vs escalation bot | `RunnableBranch` / routing `RunnableLambda` |
| **Nested** | A chain that calls other chains | Rewriter → translator → formatter | Any chain used as a step |
| **Hybrid** | LLM + Python + external API | AI → validate → API call → summarise | `RunnableLambda` |

## Debugging and observability

Once a script becomes a multi-step pipeline, you need to see what each step received and returned.

- Log every step's input and output, especially when several LLMs are chained.
- Put **structured output parsers between steps**, so a bad shape fails at the step that produced it rather than three steps later.

> **Correction to the slide:** the slide says to pass `verbose=True` to your chain constructors. That was the legacy `LLMChain(..., verbose=True)` style; LCEL chains built with `|` have no such constructor. The current options are:
> - `from langchain_core.globals import set_debug; set_debug(True)` prints every step's inputs and outputs (`set_verbose(True)` is a lighter version);
> - per call: `chain.invoke(inputs, config={"callbacks": [ConsoleCallbackHandler()]})`, with `ConsoleCallbackHandler` from `langchain_core.tracers`;
> - **LangSmith** tracing: set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` in the environment to get a browsable trace of every run.

## Best practices for chain design

| Principle | Meaning |
|---|---|
| Keep it modular | One chain does one job; build complexity by composing |
| Validate between steps | Structured output or Pydantic parsers at each hand-off |
| Don't chain too deep | Beyond about 5–6 links debugging gets messy. For loops, retries or shared state, move to **LangGraph** |
| Mix logic and LLM sensibly | Deterministic code for what must be reliable; LLMs for language and judgement |
| Log everything | Needed for debugging and auditing |
| Design for reuse | Small chains become plug-ins for bigger projects |

The slide says "consider Runnables" for deep chains, but LCEL chains already *are* Runnables (Lecture 17, [`17_runnables_in_langchain.md`](17_runnables_in_langchain.md)). The real step up for complex control flow is LangGraph.

### How my call-transcript QA project fits

My live-session project ([`src/pipeline/pipeline.py`](../../../03_live_sessions/01_call_transcript_qa/src/pipeline/pipeline.py)) is a **classification → routing → evaluation → report** pipeline:
- each LLM step is a small `prompt | llm | parser` chain with a Pydantic parser (modular, validated between steps);
- the router ([`src/components/router.py`](../../../03_live_sessions/01_call_transcript_qa/src/components/router.py)) is plain Python that maps `call_type` to an evaluation plan (logic where reliability matters);
- each step catches exceptions per call, so one bad reply doesn't stop the whole run.

Two things I could improve with this lecture's tools:
- `route_call` could be wrapped in a `RunnableLambda`, making the whole pipeline one composable chain.
- The `iterrows()` loops call chains one row at a time. `batch` runs them concurrently and still collects errors:

```python
results = summary_chain.batch(
    [{"article": "a"}, {"article": "b"}, {"article": "c"}],
    config={"max_concurrency": 4},
    return_exceptions=True,     # failed items come back as exception objects instead of raising
)
```

> **Takeaway:** a chain is a pipeline of small, testable steps: prompt → model → parser, plus any Python you need. Build chains with LCEL (`|`, `RunnableParallel`, `RunnableBranch`, `RunnableLambda`) rather than the legacy `LLMChain` family, validate at every hand-off, and trace the run when something goes wrong.

## Check yourself

1. What problems appear when you chain LLM calls with plain f-strings and `llm.invoke`, and how do chains address them?
2. Rewrite `SimpleSequentialChain(chains=[summary_chain, tweet_chain])` in LCEL. How would you also keep the intermediate summary in the output?
3. What's the difference between `RunnableParallel` and `RunnableBranch`? Give a use case for each.
4. Why does placing a Pydantic parser between two steps make a pipeline easier to debug?
5. `verbose=True` does nothing on your `prompt | llm | parser` chain. Name two ways to see every step's inputs and outputs.
6. In a classification → routing → evaluation pipeline, which steps should be LLM calls and which plain code? Why?
