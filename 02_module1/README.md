# GenAI program: week by week

My work in IIT Patna's *Certificate Program in Generative AI & Agentic AI for Developers*, organized by course week. Theory weeks have lecture notes; hands-on weeks also have the code I built. Projects from the Sunday live sessions are kept separately in [`03_live_sessions/`](../03_live_sessions) at the repo root, because everything here is pre-recorded.

| Week | Theory notes | Hands-on |
|---|---|---|
| [Week 1](week_01) | [Lectures 0–4](week_01/notes): roadmap, what GenAI is, ML vs GenAI, how LLMs work, Responsible AI | — |
| [Week 2](week_02) | [Lecture 5](week_02/notes): the developer mindset | [Cloud APIs vs local models](week_02/01_API_VS_local) · [CLI chatbot](week_02/02_chatbot) · [Streamlit chat assistant](week_02/03_capstone) |
| [Week 3](week_03) | [Lectures 7–8](week_03/notes): prompt tuning vs fine-tuning, LoRA and QLoRA | — |
| [Week 4](week_04) | [Lectures 6, 10–18](week_04/notes): APIs vs local models, recap, LangChain (models, prompts, structured output, chains, memory, runnables), intro to RAG | [LoRA fine-tuning of phi-1.5 on CPU](week_04/Finetuning-Project) |


## Lecture notes

| # | Lecture | Week |
|---|---|---|
| 0 | [GenAI development roadmap](week_01/notes/00_genai_development_roadmap.md) | 1 |
| 1 | [What is Generative AI?](week_01/notes/01_what_is_generative_ai.md) | 1 |
| 2 | [Traditional ML vs Generative AI](week_01/notes/02_traditional_ml_vs_generative_ai.md) | 1 |
| 3 | [What are LLMs?](week_01/notes/03_what_are_llms.md) | 1 |
| 4 | [Responsible AI](week_01/notes/04_responsible_ai.md) | 1 |
| 5 | [The developer mindset in GenAI](week_02/notes/05_developer_mindset_in_genai.md) | 2 |
| 6 | [APIs vs local models](week_04/notes/06_api_vs_local_models.md) | 4 |
| 7 | [Prompt tuning vs fine-tuning](week_03/notes/07_prompt_tuning_vs_fine_tuning.md) | 3 |
| 8 | [LoRA and QLoRA](week_03/notes/08_lora_and_qlora.md) | 3 |
| 10 | [Progress summary and learning recap](week_04/notes/10_progress_summary_and_learning_recap.md) | 4 |
| 11 | [LangChain introduction](week_04/notes/11_langchain_introduction.md) | 4 |
| 12 | [Models in LangChain](week_04/notes/12_models_in_langchain.md) | 4 |
| 13 | [Prompt engineering in LangChain](week_04/notes/13_prompt_engineering_in_langchain.md) | 4 |
| 14 | [Structured output and output parsers](week_04/notes/14_structured_output_and_output_parsers.md) | 4 |
| 15 | [Chains in LangChain](week_04/notes/15_chains_in_langchain.md) | 4 |
| 16 | [Memory in LangChain](week_04/notes/16_memory_in_langchain.md) | 4 |
| 17 | [Runnables in LangChain](week_04/notes/17_runnables_in_langchain.md) | 4 |
| 18 | [Introduction to RAG](week_04/notes/18_introduction_to_rag.md) | 4 |

Notes are numbered like the course slides. Week 4 also has [study resources](week_04/notes/study_resources.md) (frameworks map, terminal cheat sheet, Copilot and Claude API setup).

## How the lectures fit together

1. **Roadmap**: the developer's job in GenAI is to *orchestrate* models (APIs, prompts, pipelines, RAG, agents), not to train them.
2. **What is GenAI**: the new capability is generating content.
3. **Traditional ML vs GenAI**: GenAI doesn't replace classic ML; each fits different problems, and they often work best together.
4. **LLMs**: the engine behind text GenAI, and the concepts you'll meet in every API call (tokens, context window, temperature, embeddings).
5. **Responsible AI**: because these systems generate content that people act on, building in safeguards is part of the job.
6. **Developer mindset** (Week 2): put it all together. Your job is to orchestrate pre-trained models into modular input → process → output workflows, stay tool-agnostic, and design responsibly.
7. **Adapting models** (Week 3): start with prompting; fine-tune when you need consistent, domain-specific behaviour; and use LoRA/QLoRA to make fine-tuning affordable.
8. **Recap** (Week 4): a checkpoint before frameworks. Knowing the building blocks by hand (tokens, embeddings, APIs, prompts, fine-tuning) means LangChain, LangGraph and CrewAI become upgrades, not mysteries.
9. **LangChain** (Week 4): the same building blocks as standard components: one interface for every model, reusable prompt templates, structured output, and runnables piped into chains with `|`. Memory has moved to LangGraph.
10. **RAG** (Week 4): when the model needs your data, retrieve the relevant chunks from a vector store and put them in the prompt, instead of retraining.

## Key ideas so far

1. Generative AI **creates** new content (text, images, code, audio, video); traditional AI **predicts, classifies and detects**.
2. GenAI works on **unstructured** data (text, images); classic ML shines on **structured, tabular** data.
3. An LLM is a neural network trained on huge amounts of text to **predict the next token**; it learns patterns of language, it doesn't "know" facts.
4. Models see **tokens** (numbers), not words; cost and context limits are measured in tokens.
5. **Embeddings** turn tokens or text into vectors so that similar meanings sit close together; they power semantic search and RAG.
6. **Self-attention** in transformers lets the model weigh every token in the context, not just the last word.
7. LLMs are built in stages: **pre-training → fine-tuning → instruction tuning and RLHF**.
8. **Prompting** changes behaviour without changing the model; **fine-tuning** permanently changes its weights.
9. **Closed APIs** (OpenAI, Anthropic, Gemini) are easy and powerful; **open models** (LLaMA, Mistral) give control and privacy but need hardware.
10. GenAI can **hallucinate and be biased**, so production apps need guardrails, monitoring and human review for high-stakes decisions.
11. **We don't train, we orchestrate:** GenAI apps are prompts + pipelines + integrations around pre-trained models; think in **input → process → output** workflows and stay **tool-agnostic**.
12. **Prompting before fine-tuning:** prompting is cheap and flexible but can be inconsistent; fine-tuning gives consistent domain behaviour but needs data and compute. For changing facts, prefer RAG.
13. **LoRA** freezes the model and trains small adapters (ΔW = A × B, rank r ≪ d, k); **QLoRA** does the same on a 4-bit base model, so a 65B model fits on one 48 GB GPU.
14. **Foundations before frameworks:** understand the flow data → tokens → embeddings → response, so you know what a framework is doing under the hood.
15. **Every LangChain component is a runnable** (`invoke`, `batch`, `stream`), so prompts, models, parsers and retrievers compose with `|` (LCEL); the legacy `LLMChain`/`SequentialChain` classes are gone in 1.x.
16. **Structured output:** prefer `with_structured_output()` on chat models; use parsers like `PydanticOutputParser` otherwise, and make schemas strict (`Literal`, `list[str]`) so bad output fails loudly.
17. **RAG pipeline:** load → split → embed → store (once), then retrieve → augment the prompt → generate (per question). It grounds answers and reduces hallucinations, but doesn't eliminate them.

## Running the code

Each project folder has its own `requirements.txt` and virtual environment (Python 3.13):

```bash
cd week_02/02_chatbot
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

API keys go in a `.env` file in the project folder (never committed): `OPENAI_API_KEY`, `GEMINI_API_KEY`, `HUGGING_FACE_API_KEY`.
