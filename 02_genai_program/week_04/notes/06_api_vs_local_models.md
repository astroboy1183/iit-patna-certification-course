# Lecture 6 · APIs vs local models (Week 4)

## Why this matters

Every GenAI app starts with one decision: **where does the model run?**

- **Cloud API:** send the prompt to a provider (OpenAI, Anthropic, Google Gemini) and get the answer back.
- **Local model:** download an open model (LLaMA, Mistral) and run it on your own machine or server.

The choice affects cost, speed, quality, privacy and how you deploy.

## Paid API models

Examples: OpenAI (GPT), Anthropic (Claude), Google (Gemini).

**How they work**
1. The provider hosts the model in its cloud.
2. Your code sends a request over HTTPS and gets the model's output back.
3. Every request is authenticated with an **API key**.

| ✅ Advantages | ⚠️ Limitations |
|---|---|
| State-of-the-art quality | You pay **per token**, for as long as the app runs |
| No hardware needed: any laptop can call it | **Rate limits** cap how many requests you can make |
| Fastest way to prototype: one function call | Your data **leaves your environment** (privacy, compliance) |

> **Correction to the slide:** the slide lists GPT-3.5 and GPT-4o as OpenAI's API models. Both are now legacy: OpenAI's deprecations page shuts down `gpt-3.5-turbo` on **23 October 2026**, and the dated GPT-4o snapshots are scheduled for shutdown too. Pick a current model from the provider's model list rather than from course slides, because model names go out of date quickly.

My `openai_app.py` and `compare_models.py` still use `gpt-3.5-turbo`, so they need a model update before that date.

## Free / local models

Examples: open models on Hugging Face (Mistral, Falcon), Meta's LLaMA family, and **Ollama** as an easy way to run them.

**How they work**
1. You **download the model weights** once.
2. You run them on your own machine or server, through a library (Hugging Face `transformers`) or a runtime (Ollama).
3. Your code talks to the local model; nothing goes over the internet.

| ✅ Advantages | ⚠️ Limitations |
|---|---|
| No per-token cost: free to use after setup | Needs capable hardware (RAM, ideally a GPU with enough VRAM) |
| Full control: choose, configure or fine-tune the model | Often slower or less accurate than premium APIs |
| Better privacy: data never leaves the machine | More setup: downloads, dependencies, configuration |

"Free" means no bill per request, not zero cost: you pay for the hardware and the electricity, and you maintain the setup yourself.

> **Terminology note:** "Hugging Face" covers two different things. The **Hub** is where you download open weights to run locally. **Inference Providers** is a hosted API that runs the model for you, so it is a cloud API with per-use pricing, not a local model. My `hf_app.py` uses the second one (the `router.huggingface.co` endpoint), and it stopped working when my free credits ran out (HTTP **402 Payment Required**). That is the "paid API" trade-off, even though the model itself is open.

> **Terminology note:** LLaMA and Mistral's models are better described as **open-weight** than open-source: you can download and run the weights, but the training data and code are not released, and LLaMA has its own licence with usage conditions.

## Trade-offs at a glance

| Factor | Paid APIs (OpenAI, Anthropic, Gemini) | Local models (Hugging Face, Ollama, LLaMA, Mistral) |
|---|---|---|
| Cost | Pay per use (tokens) | Free per request; hardware costs instead |
| Speed | Usually faster (optimised servers) | Slower unless you have strong hardware |
| Accuracy | State of the art, very high | Depends on the model you choose |
| Privacy | Data leaves your environment | Data stays local |
| Control | Limited: the model is a black box | Full: you can fine-tune or modify it |
| Setup | Easy: just an API key | Downloads, dependencies, configuration |

Two nuances the table leaves out:

- **Control:** APIs are not entirely closed. OpenAI, for example, offers fine-tuning of some models through its API, but you never get the weights. Locally, you own the weights and can apply LoRA yourself, as in my [Week 4 fine-tuning project](../Finetuning-Project) (see also [Lecture 8](../../week_03/notes/08_lora_and_qlora.md)).
- **Hardware:** a GPU helps a lot, but it is not strictly required. Ollama runs **quantised** models (typically 4-bit), so a 7B model like Mistral fits in about 8 GB of RAM and can run on a CPU. My laptop has no NVIDIA GPU and still runs `mistral` through Ollama; it is just slower than the cloud APIs.

## Setting up your environment

| Route | What to install | Authentication |
|---|---|---|
| **Cloud APIs** | The provider SDKs: `openai`, `anthropic`, and Google's `google-genai` | API key in `.env` (loaded with `python-dotenv`) or a secrets manager; never hard-coded |
| **Hugging Face (local)** | `transformers` + `huggingface_hub` | A Hugging Face token, needed for gated models (e.g. LLaMA) and for Inference Providers; public models download without one |
| **Ollama** | The Ollama app (macOS, Linux, Windows) | None: it runs on `localhost` |

Ollama workflow: install it, run `ollama pull mistral` to download a model, then query it from the terminal (`ollama run mistral`) or from Python.

> **Correction to the slide:** the slide says to install `google-generativeai`. Google has deprecated that package; its replacement is **`google-genai`** (`from google import genai`, then `client = genai.Client()` and `client.models.generate_content(...)`). My Week 2 code still uses the old package, which my [SDK cheat sheet](../../week_02/01_API_VS_local/SDK_CHEATSHEET.md) notes.

> **Correction to the slide:** Ollama on Windows is no longer a "preview". It is now a regular native Windows app, alongside macOS and Linux.

## Same code, two worlds

Ollama exposes an **OpenAI-compatible endpoint**, so the same OpenAI SDK code can talk to a cloud model or a local one. Only the client settings change:

```python
from openai import OpenAI

# Local: Ollama must be running and the model pulled (ollama pull mistral)
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # key is ignored locally

response = client.chat.completions.create(
    model="mistral",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)
print(response.choices[0].message.content)

# Cloud: OpenAI(api_key=os.getenv("OPENAI_API_KEY")) and a current OpenAI model name
```

This makes "API vs local" a configuration choice rather than a rewrite, which is the tool-agnostic habit from [Lecture 5](../../week_02/notes/05_developer_mindset_in_genai.md).

## My hands-on (Week 2)

I built this lecture's demo in [`week_02/01_API_VS_local`](../../week_02/01_API_VS_local):

| File | What it shows |
|---|---|
| [openai_app.py](../../week_02/01_API_VS_local/openai_app.py) | Cloud API: chat completion with the OpenAI SDK |
| [gemini_app.py](../../week_02/01_API_VS_local/gemini_app.py) | Cloud API: Gemini through `google-generativeai` |
| [ollama_app.py](../../week_02/01_API_VS_local/ollama_app.py) | Local model: `mistral` through Ollama, no API key |
| [hf_app.py](../../week_02/01_API_VS_local/hf_app.py) | Hosted open model (Llama 3.1 8B) through Hugging Face Inference Providers, with every error I hit and how I fixed it |
| [compare_models.py](../../week_02/01_API_VS_local/compare_models.py) | One function per provider (OpenAI, Gemini, Ollama, Hugging Face), each sent the same prompt for comparison |
| [SDK_CHEATSHEET.md](../../week_02/01_API_VS_local/SDK_CHEATSHEET.md) | The same four steps (import, client, call, read) across five SDKs, plus common errors |

What the hands-on taught me beyond the slides:
- **Cloud APIs fail on keys and billing:** 401 for a wrong key, 429 for rate limits, 402 when free credits run out.
- **Local models fail in hardware ways:** the model must be downloaded first, the Ollama app must be running, and speed depends on your RAM and CPU/GPU.

## When to use what

**Cloud API if…**
- you need the best quality, or you are prototyping and want results today;
- you have no suitable hardware;
- traffic is low or unpredictable, so paying per token is cheaper than owning servers.

**Local model if…**
- the data is sensitive and must not leave your machine or network (health, legal, internal documents);
- usage is high and steady, so per-token bills would outgrow the hardware cost;
- you need offline use, or full control to fine-tune and pin a model version.

Many real systems are **hybrid**: a local model for private or cheap, simple tasks, and a cloud API for the hardest requests.

> **Takeaway:** an API rents someone else's state-of-the-art model by the token; a local model is one you own and run yourself. Decide on cost, quality, privacy and control, and write code that lets you switch.

## Check yourself

1. Name three reasons a hospital might choose a local model over a cloud API, and one reason it might not.
2. Why is a local model "free" per request but not free overall?
3. My `hf_app.py` uses an open Llama model but returned HTTP 402. Is it a local model? Explain.
4. How can a 7B model run on a laptop with no NVIDIA GPU? What is the cost?
5. What two settings change when you point the OpenAI SDK at Ollama instead of OpenAI?
6. Which Python package should new Gemini code use today, and why not the one on the slide?
