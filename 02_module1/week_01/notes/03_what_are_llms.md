# Lecture 3 · What are LLMs? (Evolution of LLMs)

## Definition

A **Large Language Model (LLM)** is a neural network trained on massive amounts of text to understand and generate human-like language.

- **Key idea:** it doesn't "know" facts; it learns **patterns of language**.
- **Mental model:** "a super-charged autocomplete engine that can reason, summarize and generate."

## Why "large"?

- **Billions of parameters**, trained on **trillions of words (tokens)**.
- **Parameters** are the learned weights, the "knobs" that capture relationships in text.
- More scale generally gives better generalization, reasoning and creativity, but **bigger isn't always better** for a given task (cost, speed, hardware).
- Examples: GPT-3 has 175B parameters; GPT-4's size is undisclosed; LLaMA 2 goes up to 70B.

## How an LLM works (simplified pipeline)

```
text ──► 1. tokenization ──► 2. embeddings ──► 3. transformer (self-attention) ──► 4. predict next token ──┐
                                                                                                        │
            ◄──────────────────────── append the token and repeat until done ◄──────────────────────────┘
```

### 1. Tokenization
- Text is split into **tokens**: whole words, parts of words or characters.
- Illustration from the lecture: `"ChatGPT rocks!"` → `["Chat", "G", "PT", "rocks", "!"]`. The exact split depends on each model's tokenizer.
- The model never sees words, only **token IDs** (numbers).
- Practical consequence: API **pricing and context limits are counted in tokens**, not words.

### 2. Embeddings
- Each token becomes a **vector** (a list of numbers) that represents its meaning.
- Similar meanings end up close together in this "meaning space". The classic illustration: `king − man + woman ≈ queen`.
- Text embeddings are also what power **semantic search and RAG** (Module 5).

### 3. Encoding, decoding and self-attention
- **Encoder:** reads the input tokens and builds internal representations.
- **Decoder:** predicts the next token from the context.
- Note: GPT-style chat models are **decoder-only** transformers; encoder-decoder designs are used in models like T5.
- **Self-attention** lets the model weigh **every token in the context** when predicting the next one, not just the last word. This is what makes transformers good with long, connected text.

### 4. The prediction loop
- The model predicts one token, appends it to the text, and repeats until it's done.
- This is how it writes essays, answers questions and generates code, one token at a time.
- That's also why responses can **stream** word by word in chat apps.

## How LLMs are trained

| Phase | What happens | Who does it |
|---|---|---|
| **1. Pre-training** | Learn to predict the next token on huge datasets (books, Wikipedia, the web, code). Picks up grammar, facts and reasoning patterns | Big labs; extremely expensive in compute, done once per model |
| **2. Fine-tuning** | Adapt the pre-trained model to a domain or task (e.g. legal contracts, medical Q&A such as Med-PaLM) | Labs or companies with domain data |
| **3. Instruction tuning and RLHF** | Teach it to follow instructions; **RLHF** (reinforcement learning from human feedback) aligns it with human preferences: helpful, harmless, honest | Labs |

## Key concepts every developer needs

| Concept | Meaning | Why it matters to you |
|---|---|---|
| **Parameters** | Number of learned weights | Bigger models cost more and are slower; pick the smallest that does the job |
| **Context window** | Maximum tokens the model can "see" at once (prompt + history + answer) | Long chats or documents must fit, or be trimmed or retrieved (RAG). Example from the lecture: 128K tokens for GPT-4 Turbo |
| **Checkpoints** | Saved states of a model during training | Different versions or sizes of the same model family |
| **Prompting** | Zero-shot (just ask) or few-shot (show examples in the prompt) | Changes behaviour **without** changing the model; fast and cheap |
| **Fine-tuning** | Permanently changes the model's weights | Costs time and data; use when prompting isn't enough |
| **Embeddings API** | Returns vectors for text | Semantic search, clustering, recommendations, RAG |

## Types of LLMs

| | Closed-source APIs | Open-source / open-weight models |
|---|---|---|
| Examples | OpenAI GPT, Anthropic Claude, Google Gemini | LLaMA, Mistral, Mixtral, Falcon, GPT4All |
| How you use them | Call a hosted API | Run locally (e.g. Ollama) or on your own cloud |
| Pros | Easy to use, top performance | Control, privacy, lower running cost, customization |
| Cons | Cost per token, less control, data-privacy concerns | Need hardware (GPU/RAM), more setup |

I compared both kinds hands-on in `../../week_02/01_API_VS_local/compare_models.py`: OpenAI and Gemini APIs vs a local Mistral model through Ollama.

## Why LLMs are popular with developers

- **General purpose:** summarization, translation, coding, tutoring and more with one model.
- **Zero-shot / few-shot learning:** works on new tasks without retraining.
- **APIs:** any Python developer can build AI apps without an ML background.
- **Ecosystem:** LangChain, LangGraph and Hugging Face make prototyping fast.

## Where LLMs are heading

- **Efficiency:** smaller, faster models that run on edge devices.
- **Multimodality:** text + images + speech + video.
- **Agentic AI:** LLMs that plan, act and use tools (Modules 6–7).
- **Customization:** domain-specific fine-tuned models for enterprises.

## Key takeaways

- LLMs are the foundation of generative AI applications.
- They work by **tokenization → embeddings → attention → prediction loop**.
- **Pre-training, fine-tuning and instruction tuning** make them capable.
- Developers don't need to train them; they **orchestrate** them.

## Check yourself

1. Why does an LLM "hallucinate" if it's just predicting the next token?
2. Your chatbot forgets the start of a long conversation. Which concept explains this, and what are two fixes?
3. When would you choose a local open model over a closed API?
4. What's the difference between few-shot prompting and fine-tuning?
