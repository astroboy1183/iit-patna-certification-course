# Module 2 · Week 1 · Models and prompts in LangChain

## Notes

| # | Lecture |
|---|---|
| 12 | [Models in LangChain](notes/12_models_in_langchain.md) |
| 13 | [Prompt engineering in LangChain](notes/13_prompt_engineering_in_langchain.md) |

The LangChain introduction (11) and structured output and output parsers (14) are in [Module 1 · Week 4](../../02_module1/week_04). Chains, memory and runnables (15–17) are in [Module 2 · Week 2](../week_02).

## Code

| Folder | Files |
|---|---|
| [01_llm_in_langchain](01_llm_in_langchain) | `llm_factory.py` builds an OpenAI or Gemini chat model from `config.json`; `app.py` sends it one prompt |
| [02_prompts-in-langchain](02_prompts-in-langchain) | Basic and chat prompt templates · few-shot · chain-of-thought · role-based · structured output · few-shot structured · saving a prompt to YAML and loading it back |

Each folder has its own `.venv` and `requirements.txt`, and reads its model settings from `config.json` and its API keys from `.env`.
