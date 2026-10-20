# Lecture 17 · Runnables in LangChain (Week 4)

## The problem: life before runnables

Early LangChain built multi-step workflows from **chain classes**: `LLMChain`, `SequentialChain`, `RouterChain` and so on.
- Each chain needed its input and output variable names declared, and chains were linked by hand.
- Complex flows became rigid, verbose and hard to debug.
- Async execution and streaming were awkward to add.

**Example:** a "Blog → Summary → Tweet" pipeline works, but every extra step adds boilerplate and the flow feels locked in.

| Pain point | What it meant |
|---|---|
| Rigid, class-based design | A new class (and its config) for every kind of step |
| Limited flexibility | Hard to insert a custom step or reorder the flow |
| Verbose syntax | Lots of code for simple transformations |
| Poor async/streaming | Each had to be set up manually |

> **Correction to the slide:** these classes are no longer just "older": `LLMChain`, `SequentialChain` and `RouterChain` were removed from the `langchain` package in 1.0 and survive only in `langchain-classic`. On my install (langchain 1.4.3), `from langchain.chains import SequentialChain` fails with `ModuleNotFoundError: No module named 'langchain.chains'`. The pipe-based version of a chain is covered in [Lecture 15](15_chains_in_langchain.md).

## What a runnable is

A **runnable** is any LangChain component that implements one shared interface. Prompts, chat models, output parsers, retrievers, plain Python functions (wrapped) and whole chains are all runnables, so they all connect the same way.

> "If chains were step-by-step recipes, runnables are LEGO blocks: you can click them together in any order."

Why they exist:
- one consistent interface instead of many chain classes;
- composition with the `|` operator;
- async, streaming, batching and parallelism **for free** on everything.

### The shared interface

| Method | What it does |
|---|---|
| `invoke(x)` | Run on one input, return one output |
| `batch([x1, x2, ...])` | Run on many inputs, **concurrently** (a thread pool), return a list |
| `stream(x)` | Yield the output in chunks as it's produced |
| `ainvoke` / `abatch` / `astream` | Async versions of the above, for `await` in web servers |

```python
import asyncio
from langchain_core.runnables import RunnableLambda

shout = RunnableLambda(lambda text: text.upper() + "!")

print(shout.invoke("hello"))                 # 'HELLO!'
print(shout.batch(["hi", "bye"]))            # ['HI!', 'BYE!']
print(list(shout.stream("hey")))             # ['HEY!']  (one chunk: a plain function can't stream)
print(asyncio.run(shout.ainvoke("async")))   # 'ASYNC!'
```

## How they connect: the pipe

| | Flow |
|---|---|
| Old chain thinking | Input → Prompt → LLM → Output parser, each step wired by hand |
| Runnables | `chain = prompt \| llm \| parser`, then `chain.invoke(input)` |

`a | b` builds a **RunnableSequence**: the output of `a` becomes the input of `b`. The result is itself a runnable, so it has `invoke`, `batch` and `stream` too.

> **Correction to the slide:** the slide writes the flow as `input | prompt | llm | parser`. The input isn't part of the pipe: you build `prompt | llm | parser` once and pass the input to `.invoke(...)` (or `.batch`/`.stream`).

The Blog → Summary → Tweet pipeline from the problem slide, in a few lines:

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = FakeListChatModel(responses=["Runnables let you pipe LangChain parts together.",
                                   "Pipe your prompts, models and parsers like LEGO. #LangChain"])  # swap for a real model
parser = StrOutputParser()

summarize = ChatPromptTemplate.from_template("Summarize this blog in one sentence:\n{blog}") | llm | parser
tweet = ChatPromptTemplate.from_template("Write a tweet from this summary:\n{summary}") | llm | parser

pipeline = {"summary": summarize} | tweet    # the dict maps step 1's output to step 2's {summary}
print(pipeline.invoke({"blog": "A long post about LCEL..."}))
```

Adding a step means adding one more `|`, not a new class with declared variables.

## The building blocks

| Runnable | What it does | Shortcut |
|---|---|---|
| **RunnableSequence** | Runs steps one after another | `a \| b \| c` |
| **RunnableParallel** | Runs several runnables on the **same input**, returns a dict of results | A dict inside a chain: `{"x": a, "y": b}` |
| **RunnablePassthrough** | Passes the input through unchanged | Often one branch of a parallel |
| **`.assign(...)`** | Keeps the input dict and **adds** computed keys | `RunnablePassthrough.assign(k=runnable)` |
| **RunnableLambda** | Wraps a normal Python function as a runnable | Plain functions are auto-wrapped when piped |
| **RunnableBranch** | Picks one runnable based on conditions (if / elif / else) | Often simpler: a function that returns the runnable to run |

### Parallel, passthrough and assign

```python
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

word_count = RunnableLambda(lambda d: len(d["transcript"].split()))
has_refund = RunnableLambda(lambda d: "refund" in d["transcript"].lower())

checks = RunnableParallel(words=word_count, refund=has_refund, original=RunnablePassthrough())
print(checks.invoke({"transcript": "I want a refund for my claim"}))
# {'words': 7, 'refund': True, 'original': {'transcript': 'I want a refund for my claim'}}

enrich = RunnablePassthrough.assign(words=word_count)    # keep the input keys, add one more
print(enrich.invoke({"transcript": "I want a refund for my claim"}))
# {'transcript': 'I want a refund for my claim', 'words': 7}
```

With model calls inside, the parallel branches run **at the same time**, so three 2-second LLM calls take about 2 seconds, not 6. `.assign` is the usual way to carry the original question along while adding, say, retrieved context (Lecture 18).

### Branching

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

route = RunnableBranch(
    (lambda d: d["call_type"] in {"billing", "claims"}, RunnableLambda(lambda d: ["knowledge_accuracy", "resolution_quality"])),
    (lambda d: d["call_type"] == "complaint",           RunnableLambda(lambda d: ["tone_empathy", "resolution_quality"])),
    RunnableLambda(lambda d: ["knowledge_accuracy"]),   # default: the last item has no condition
)
print(route.invoke({"call_type": "complaint"}))      # ['tone_empathy', 'resolution_quality']
print(route.invoke({"call_type": "general_query"}))  # ['knowledge_accuracy']
```

This is the same logic as `route_call` in my project's [router.py](../../../03_live_sessions/01_call_transcript_qa/src/components/router.py). The docs now prefer a plain `RunnableLambda` whose function returns the runnable to run; anything beyond simple routing (loops, retries, state) belongs in LangGraph.

## Chains vs runnables

| Aspect | Legacy chains | Runnables |
|---|---|---|
| Syntax | Class-based, verbose | Functional, minimal (`\|`) |
| Composability | Limited | Pipe any component into any other |
| Streaming / async | Manual setup | Built in on every runnable |
| Parallel execution | Difficult | `RunnableParallel`, `.batch()` |
| Debuggability | Opaque | Each step is a visible, traceable run |
| Future | Removed in 1.0 (`langchain-classic`) | Foundation of LangGraph |

Two caveats the slides skip:
- **Pipes don't make code faster by themselves.** Speed comes from `batch`, `RunnableParallel`, async and streaming (which improves *perceived* speed).
- **Streaming needs every step to support it.** A model and `StrOutputParser` stream token by token; a plain `RunnableLambda` waits for its whole input, so it turns the stream back into one chunk (use a generator function to keep streaming).

## In my project: the call-transcript QA pipeline

My live-session project ([experiment.ipynb](../../../03_live_sessions/01_call_transcript_qa/experiment.ipynb), [src/](../../../03_live_sessions/01_call_transcript_qa/src)) already builds runnables: `classification_chain = prompt | llm | parser`, and the same shape for tone, knowledge, resolution and the final report. But [pipeline.py](../../../03_live_sessions/01_call_transcript_qa/src/pipeline/pipeline.py) uses them one call at a time:

| What it does now | Runnable feature that fits |
|---|---|
| `for ... in df.iterrows(): chain.invoke(row["transcript"])` with a `try/except` per row | `chain.batch(transcripts, return_exceptions=True)`: rows run concurrently, a failed row returns its exception instead of crashing the run |
| Tone, knowledge and resolution chains invoked one after another per transcript | A `RunnableParallel` of only the chains in `eval_plan`, so they run at once |
| `route_call` picks the evaluations with `if/elif` | Fine as is; could become a branch inside the chain |

`batch` with per-row error handling, in miniature:

```python
from langchain_core.runnables import RunnableLambda

def classify(transcript: str) -> str:
    if not transcript:
        raise ValueError("empty transcript")
    return "complaint" if "angry" in transcript else "general_query"

chain = RunnableLambda(classify)   # stands in for prompt | llm | parser
rows = ["I am angry about my bill", "", "What are your hours?"]
results = chain.batch(rows, config={"max_concurrency": 5}, return_exceptions=True)
print(results)   # ['complaint', ValueError('empty transcript'), 'general_query']
```

`max_concurrency` caps simultaneous calls, which matters for API rate limits.

## Best practices

> **Correction to the slide:** the "Best Practices" slide in this deck is a copy of the memory lecture's slide (memory type, token window, RAG). Those belong to [Lecture 16](16_memory_in_langchain.md). Practices that actually apply to runnables:

| Practice | Why |
|---|---|
| Build small chains and compose them | Each piece can be tested with `.invoke` on its own |
| Use `.batch()` instead of loops over `.invoke()` | Concurrency for free; set `max_concurrency` for rate limits |
| Use `RunnableParallel` for independent steps | Total time ≈ slowest branch, not the sum |
| Use `RunnablePassthrough.assign` to carry inputs forward | Later steps still see the original question |
| Use `.stream()` in user-facing apps | The first words appear immediately |
| Keep `RunnableLambda` functions pure and small | Easier to debug, and keeps the pipe readable |
| Move to LangGraph for loops, state and agents | Pipes are for straight-line and branching flows |

## Why it matters and what's next

- Runnables are the **standard** way to build in LangChain: prompts, models and parsers ([Lectures 12–14](12_models_in_langchain.md)) all speak this interface.
- They're the base of **LangGraph** and agents: a compiled LangGraph graph is itself a runnable (I checked: `isinstance(graph, Runnable)` is `True`), so it has `invoke`, `batch` and `stream` as well.
- They make apps more **modular** and easier to maintain, and faster where you use batching, parallelism or streaming.

> **Takeaway:** a runnable is anything with `invoke`/`batch`/`stream`. Snap them together with `|`, fan out with a dict, carry inputs with `.assign`, and you get concurrency and streaming without writing it yourself.

## Check yourself

1. Name the four core runnable methods and when you'd use each one.
2. What does `{"summary": summarize} | tweet` turn into, and why is the dict needed?
3. What's the difference between `RunnablePassthrough()` and `RunnablePassthrough.assign(...)`? Give an example of each.
4. Rewrite the per-row loop in my `run_classification` using `.batch()`. How do you keep one bad transcript from stopping the run?
5. Why can putting a plain `RunnableLambda` in the middle of a chain break token streaming?
6. The tone, knowledge and resolution evaluations are independent. How would `RunnableParallel` change the time per transcript?
