# Lecture 10 · Progress summary and learning recap (Week 4)

A checkpoint lecture: no new concepts, just a look back at what the first weeks covered and why it matters before moving on to frameworks like LangChain.

## Where we started

At the start of the program, most of us had questions like:

- *What exactly is Generative AI?*
- *How is it different from traditional AI or ML?*
- *Do I need to train models from scratch to build GenAI apps?*

The short answers, now:

| Question | Answer |
|---|---|
| What is GenAI? | AI that **creates** new content (text, images, code, audio) instead of only predicting or classifying |
| How is it different from ML? | Traditional ML is **predictive**, usually on structured data; GenAI is **creative**, usually on unstructured data. They complement each other |
| Do I need to train models from scratch? | **No.** Developers orchestrate pre-trained models through APIs, prompts and pipelines; when behaviour must change, lightweight fine-tuning (LoRA/QLoRA) adapts an existing model |

The journey so far: **curiosity → confidence**, with an understanding of the building blocks of modern GenAI systems, both conceptual and hands-on.

## What we've learned so far

| Stage | Topic | Core skill or insight | My notes / code |
|---|---|---|---|
| 1 | What is Generative AI? | What GenAI is, why it matters, and its real-world impact | [Lecture 1](../../week_01/notes/01_what_is_generative_ai.md) |
| 2 | Traditional AI vs GenAI | *Predictive* AI (ML) vs *creative* AI (GenAI) | [Lecture 2](../../week_01/notes/02_traditional_ml_vs_generative_ai.md) |
| 3 | Responsible AI | An ethical foundation: fairness, safety and responsible model use | [Lecture 4](../../week_01/notes/04_responsible_ai.md) |
| 4 | Transformers basics | The "Attention Is All You Need" revolution: why transformers changed everything | [Lecture 3](../../week_01/notes/03_what_are_llms.md) (self-attention) |
| 5 | What are LLMs? | Tokenization, embeddings, pre-training and fine-tuning, intuitively | [Lecture 3](../../week_01/notes/03_what_are_llms.md) |
| 6 | Developer mindset in GenAI | From "model trainer" to "AI system orchestrator" | [Lecture 5](../../week_02/notes/05_developer_mindset_in_genai.md) |
| 7 | APIs vs local models | Connecting both cloud APIs (OpenAI, Gemini) and local models (Ollama, Hugging Face) | [01_API_VS_local](../../week_02/01_API_VS_local) |
| 8 | Prompt tuning vs fine-tuning | Controlling model behaviour, either with prompts or with lightweight training | [Lecture 7](../../week_03/notes/07_prompt_tuning_vs_fine_tuning.md) |
| 9 | LoRA and QLoRA | Modern efficiency tricks to fine-tune huge models affordably | [Lecture 8](../../week_03/notes/08_lora_and_qlora.md) · [Finetuning-Project](../Finetuning-Project) |
| 10 | Your first simple chatbot | The first working GenAI app: the moment theory turned into reality | [02_chatbot](../../week_02/02_chatbot) |
| 11 | Capstone: chatbot with memory + UI | Persistence and a UI: connecting GenAI logic with user experience | [03_capstone](../../week_02/03_capstone) |

## Why this foundation matters

- 🧩 **Conceptual clarity.** We know how **data → tokens → embeddings → responses** flows through a model. When LangChain abstracts these details away later, we'll still know what's happening under the hood.
- ⚙️ **Practical grounding.** We built things **without "magic" libraries**: handling APIs, cost, model configs and local setups. That's the real engineering layer.
- 🚀 **Confidence through creation.** The first chatbot wasn't fancy, and that's the point: it proved we can build working GenAI systems from scratch.

> **Takeaway:** every new tool from here on (LangChain, LangGraph, CrewAI, …) should feel like an **upgrade, not a mystery**, because we've already done by hand what those tools automate.

## What I'd add from building it myself

The hands-on work taught a few things the slides don't:

- **Most of the work is engineering around the model:** environments, versions, config files, retries and error handling, more than the model call itself.
- **The environment matters as much as the code.** The fine-tuning project only ran after fixing Python-version and library-version mismatches and switching from GPU settings to CPU ones (see [ISSUES_AND_FIXES.md](../Finetuning-Project/ISSUES_AND_FIXES.md)).
- **Validate model output.** Structured outputs (Pydantic schemas) catch the cases where the model returns the wrong shape, which happened in my [live-session project](../../../03_live_sessions/01_call_transcript_qa).

## Check yourself

1. Explain the path **data → tokens → embeddings → response** in your own words.
2. Why don't most GenAI developers train models from scratch? What do they do instead?
3. When would you choose a local model (Ollama, Hugging Face) over a cloud API, and vice versa?
4. What's the difference between controlling a model with prompts and with fine-tuning? Which would you try first, and why?
5. Why learn to build a chatbot "by hand" before using a framework like LangChain?
