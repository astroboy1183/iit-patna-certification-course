# Lecture 5 · The developer mindset in GenAI (Week 2)

## Why mindset matters

| | Traditional ML developer | GenAI developer |
|---|---|---|
| Main work | Data cleaning, feature engineering, model training, hyperparameter tuning | Building **workflows and apps around pre-trained models** |
| Starting point | Your own data → your own model | A powerful model that already exists |

**Analogy:** instead of **baking the bread** (training a model), you're **running a sandwich shop** (orchestrating models, data and tools into a product).

## Core philosophy: we don't train, we orchestrate

Pre-trained models already hold vast general knowledge. The developer's job is to put that to work:

| Lever | What it means | Example |
|---|---|---|
| **Prompting** | Shaping the model's behaviour with instructions and examples | A system prompt that sets tone and rules |
| **Pipelines** | Chaining several steps or tools | Classify → evaluate → summarize |
| **Integration** | Connecting APIs, databases and cloud services | Look up an order in the CRM, then answer |

**Example:** a customer-support bot is not a model you train. It's **LLM + vector database (your help articles) + CRM API (customer data)**, connected by your code.

## Developers as API composers

- GenAI capabilities arrive as **APIs** (OpenAI, Anthropic, Gemini, …).
- You "compose" an app like music: **the APIs are the instruments, your code is the conductor.**
- **Skills shift:**
  - less about model internals;
  - more about **modular API integration, monitoring and optimization**.

**Example:** a summarizer app is really **API call + cost logging + output formatting**, and the last two are where most of the engineering goes.

```python
# Illustrative sketch of the summarizer: the API call is one line; the rest is engineering around it.
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment


def summarize(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize in 3 bullet points."},
            {"role": "user", "content": text},
        ],
        max_tokens=200,
    )
    usage = response.usage
    print(f"tokens in={usage.prompt_tokens} out={usage.completion_tokens}")  # cost logging
    return response.choices[0].message.content.strip()                     # output formatting
```

## Modular thinking: input → process → output

Every GenAI solution can be broken into three stages:

| Stage | In the lecture's example |
|---|---|
| **Input** | The user's query |
| **Process** | LLM generates → apply filters → enrich with external data |
| **Output** | A polished response, or an action |

This makes solutions **debuggable** (you can test each step), **reusable** (swap one step without touching the others) and **scalable**.

> Think like a **workflow designer**, not a model tuner.

My live-session notebook follows this shape: **input** = call transcripts (CSV) → **process** = classify each call, route it to the right evaluations, score tone / resolution / knowledge → **output** = one results table (`../../live_sessions/01_call_transcript_qa/experiment.ipynb`).

## Key developer skills for the GenAI era

| Skill | What it means | Where it comes up in the program |
|---|---|---|
| **Prompt engineering** | Guiding model responses | Modules 3–4 |
| **Evaluation and testing** | Measuring response quality, not just "it looks right" | Throughout; my notebook's scoring chains |
| **RAG** | Grounding answers in private data | Module 5 |
| **Cost and performance awareness** | Tokens, latency, scaling | Module 2 (e.g. free-tier limits, `max_tokens`) |
| **Responsible AI** | Bias, fairness, safe outputs | Lecture 4 |

## A future-proof developer mindset

- **The role is evolving:** coder → orchestrator → **AI system designer**.
- **Competitive advantage:** the ability to **prototype and ship GenAI apps quickly**.
- **The best GenAI developers:**
  - **stay tool-agnostic**: they can switch APIs and models easily;
  - **think in workflows**, not isolated API calls;
  - **balance creativity with responsibility**.

Being tool-agnostic is what my `../02_chatbot` and `../03_capstone` projects practise: the provider and model come from `config.json`, so switching between OpenAI and Gemini needs no code change. The SDK cheat sheet in `../01_API_VS_local/SDK_CHEATSHEET.md` shows the same idea across five providers.

## Key takeaways

- You're not training GPT-4 from scratch; **you're building applications around it**.
- Shift your identity **from model builder to system orchestrator**.
- Success in GenAI = **modular thinking + API fluency + responsible design**.

## Check yourself

1. Explain the bread vs sandwich-shop analogy in your own words.
2. Break a "chat with your PDF" app into input → process → output.
3. Why is staying tool-agnostic valuable? How would you design an app so the LLM provider can be switched?
4. In the summarizer example, which parts are "the model" and which are "the engineering"?
