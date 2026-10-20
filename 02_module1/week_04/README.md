# Week 4 · LangChain, RAG and fine-tuning in practice

Notes from the Week 4 lectures:

| # | Lecture |
|---|---|
| 6 | [APIs vs local models](notes/06_api_vs_local_models.md) |
| 10 | [Progress summary and learning recap](notes/10_progress_summary_and_learning_recap.md) |
| 11 | [LangChain introduction](notes/11_langchain_introduction.md) |
| 12 | [Models in LangChain](notes/12_models_in_langchain.md) |
| 13 | [Prompt engineering in LangChain](notes/13_prompt_engineering_in_langchain.md) |
| 14 | [Structured output and output parsers](notes/14_structured_output_and_output_parsers.md) |
| 15 | [Chains in LangChain](notes/15_chains_in_langchain.md) |
| 16 | [Memory in LangChain](notes/16_memory_in_langchain.md) |
| 17 | [Runnables in LangChain](notes/17_runnables_in_langchain.md) |
| 18 | [Introduction to RAG](notes/18_introduction_to_rag.md) |

Plus [study resources](notes/study_resources.md): a map of ML and GenAI frameworks, Windows vs macOS/Linux terminal commands, and getting GitHub Copilot and Claude API access.

The LangChain slides were written for LangChain 0.x. The notes use the current 1.x APIs, and mark each outdated slide with a "Correction to the slide". The code snippets were run against langchain 1.4.3 / langchain-core 1.6.6 using fake models (no API calls); the few that need a real API key or extra packages are marked as such.

## Hands-on

| Folder | What I built |
|---|---|
| [Finetuning-Project](Finetuning-Project) | LoRA fine-tuning of `microsoft/phi-1_5` on a CPU: a baseline chat, the LoRA training script and a chat with the trained adapter. [ISSUES_AND_FIXES.md](Finetuning-Project/ISSUES_AND_FIXES.md) logs every setup and code issue hit along the way |
