# Lecture 12 · Models in LangChain (Week 4)

## Why a model abstraction matters

Every provider (OpenAI, Gemini, Anthropic, Ollama, …) ships its own:
- SDK,
- request and response format (API signature),
- way of passing credentials.

Code written directly against one SDK is hard to move to another. LangChain puts a **unified interface** in front of all of them: every chat model, whatever the provider, is called the same way and returns the same kind of object. Switching provider becomes a one-line change to the constructor, and the prompts, chains and parsers around it stay as they are.

> Analogy from the slides: LangChain is a **"universal adapter"** for LLMs. Plug in any model and the rest of the app doesn't notice.

The setup (packages, the `langchain_core` / provider-package split) is in [Lecture 11](11_langchain_introduction.md).

## Types of models in LangChain

| Type | Example models | Input → output | Used for |
|---|---|---|---|
| **LLMs** (text completion) | `gpt-3.5-turbo-instruct` via `langchain_openai.OpenAI` | string → string | Legacy text completion |
| **Chat models** | GPT-4o / GPT-4o-mini, Gemini 2.5, Claude, Ollama models | list of messages → `AIMessage` | Almost everything: generation, summarisation, reasoning, multi-turn chat, tool calling |
| **Embedding models** | `text-embedding-3-small`, `all-MiniLM-L6-v2` | text → vector of floats | Semantic search, RAG, clustering ([Lecture 18](18_introduction_to_rag.md)) |
| **Multimodal** | Gemini, GPT-4o, LLaVA | messages with text + image/audio blocks → `AIMessage` | Vision and mixed-media tasks |

> **Correction to the slide:** the slide lists GPT-4o, Gemini Pro and Ollama models under **LLMs** and calls chat models a separate family for "multi-turn conversations". In LangChain those modern models are all used as **chat models** (`ChatOpenAI`, `ChatGoogleGenerativeAI`, `ChatOllama`), even for single-turn tasks. The `LLM` class (string in, string out) is the older text-completion interface and is rarely used in new code; the LangChain 1.x docs use "model" to mean chat model. "Multimodal" is not a separate class either: a chat model that supports images accepts image content blocks inside a normal message. Model names also age quickly (Gemini 1.5 has been retired), so check the provider's current model list.

The difference in return type is easy to see, using LangChain's built-in fake models (no API key, no cost):

```python
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.language_models.fake_chat_models import FakeListChatModel

llm = FakeListLLM(responses=["Paris"])
chat = FakeListChatModel(responses=["Paris"])

llm.invoke("Capital of France?")    # 'Paris'                     (a plain str)
chat.invoke("Capital of France?")   # AIMessage(content='Paris')  (a message object)
```

A chat model returns an `AIMessage`; the text is in `.content`, and the object can also carry tool calls and metadata such as token usage (from real providers). That richer return type is why chat models replaced the plain LLM interface.

## How LangChain manages a model

When you create a model object you:
1. pick the **provider class** (or let `init_chat_model` pick it, below);
2. set **generation parameters**;
3. let LangChain handle authentication and the HTTP call. Keys are read from environment variables by default (`OPENAI_API_KEY`, `GOOGLE_API_KEY`), or passed explicitly.

| Parameter | What it controls |
|---|---|
| `model` | Which model to call, e.g. `"gpt-4o-mini"`, `"gemini-2.5-flash"` |
| `temperature` | Randomness. Near 0 → focused and repeatable; higher → more varied |
| `max_tokens` | Upper limit on the length of the reply |
| `top_p` | Nucleus sampling: only sample from the most likely tokens whose probabilities add up to `p` |

```python
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, max_tokens=200, top_p=0.9)
# later, switch provider by changing one line:
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, max_tokens=200, top_p=0.9)
```

The slide's version uses `gpt-4o` and `gemini-2.5-flash` without the imports; each provider class lives in its own package (`langchain-openai`, `langchain-google-genai`), which has to be installed. Both classes accept the same parameter names here; `ChatGoogleGenerativeAI` maps `max_tokens` to Gemini's own `max_output_tokens`.

### `init_chat_model`: provider as a string

The slide's switch still means editing an import and a class name. LangChain 1.x has a factory that takes the provider as data, so the choice can come from config or an environment variable:

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini", temperature=0.3)            # -> ChatOpenAI
llm = init_chat_model("google_genai:gemini-2.5-flash", temperature=0.3) # -> ChatGoogleGenerativeAI
llm = init_chat_model("gpt-4o-mini", model_provider="openai")           # same, provider as its own argument
```

It still needs the provider package installed; it just imports the right class for you. There is a matching `init_embeddings("openai:text-embedding-3-small")` in `langchain.embeddings`.

## One interface for every model

Every chat model is a **Runnable** ([Lecture 17](17_runnables_in_langchain.md)), so they all share the same methods:

| Method | Does |
|---|---|
| `.invoke(input)` | One call, returns one `AIMessage` |
| `.batch([in1, in2, …])` | Several inputs, run concurrently, returns a list |
| `.stream(input)` | Yields the reply in chunks as it is generated (for chat UIs) |
| `.ainvoke` / `.abatch` / `.astream` | Async versions |

The input can be a plain string or a list of messages with roles:

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import SystemMessage, HumanMessage

model = FakeListChatModel(responses=["Bonjour", "Merci", "Bonne nuit"])  # stand-in for any chat model

reply = model.invoke([SystemMessage("You translate English to French."), HumanMessage("Hello")])
print(reply.content)                                 # Bonjour
print([m.content for m in model.batch(["Thank you", "Good night"])])   # ['Merci', 'Bonne nuit']

for chunk in model.stream("Hello"):
    print(chunk.content, end="")
```

Swap `FakeListChatModel(...)` for `ChatOpenAI(...)` or `init_chat_model(...)` and nothing else changes: that is the abstraction the lecture is about. The fake models are also handy for unit-testing chains offline.

> **Correction (older tutorials):** LangChain 0.x code often calls a model directly, `llm("...")`, or uses `llm.predict(...)` / `llm.predict_messages(...)`. These were removed in 1.x: calling a model object raises `TypeError: ... object is not callable`. Use `.invoke()`. Likewise, imports such as `from langchain.llms import OpenAI` or `from langchain.chat_models import ChatOpenAI` no longer work; provider classes come from their own packages (`from langchain_openai import ChatOpenAI`).

### Embeddings and multimodal input, briefly

```python
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage

emb = OpenAIEmbeddings(model="text-embedding-3-small")
# emb.embed_query("refund policy") -> list[float];  emb.embed_documents([...]) -> list[list[float]]

msg = HumanMessage(content=[
    {"type": "text", "text": "What is in this image?"},
    {"type": "image", "url": "https://example.com/cat.png"},
])
# vision_model.invoke([msg])   # any chat model that supports images
```

Embedding models have a different interface (`embed_query`, `embed_documents`) because they return vectors, not messages. They come back in the RAG lectures.

## In my project

My call-transcript QA project ([`llm_loader.py`](../../../03_live_sessions/01_call_transcript_qa/src/utils/llm_loader.py), first built in [`experiment.ipynb`](../../../03_live_sessions/01_call_transcript_qa/experiment.ipynb)) is this lecture in practice:
- it reads `LLM_PROVIDER` from the environment and builds either `ChatOpenAI` or `ChatGoogleGenerativeAI`;
- model names and `temperature` (0.3, for steadier scoring) come from [`config/config.json`](../../../03_live_sessions/01_call_transcript_qa/config/config.json), not from code;
- everything downstream (`prompt | llm | parser` in `src/components/`) works with either model without changes.

Two things the lecture suggests improving:
- With `init_chat_model`, the `if/elif` becomes a lookup: map `"openai"` → `"openai"` and `"gemini"` → `"google_genai"`, then call `init_chat_model(config["llm"][key], model_provider=..., temperature=...)`. Adding a provider is then a config change.
- The config's default Gemini model is `gemini-1.5-flash`, which Google has retired; `gemini-2.5-flash` is a current replacement.

> **Takeaway:** in LangChain you code against the *chat model interface*, not a provider. Pick the provider and parameters at construction time (ideally from config), then use `.invoke()` / `.batch()` / `.stream()` everywhere.

## Check yourself

1. What does a chat model's `.invoke()` return, and how is it different from what a legacy `LLM` returns?
2. Which three things differ between provider SDKs that LangChain hides from you?
3. Rewrite `ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)` using `init_chat_model`. Why is the string form useful in a config-driven app?
4. What do `temperature`, `max_tokens` and `top_p` each control? Which would you lower for a classifier that must give the same label every run?
5. A 0.x tutorial calls `llm("Tell me a joke")`. What happens in LangChain 1.x, and what is the fix?
6. How can you unit-test a chain that uses `ChatOpenAI` without an API key or network access?
