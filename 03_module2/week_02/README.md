# Module 2 · Week 2 · Chains, memory and runnables in LangChain

## Notes

| # | Lecture |
|---|---|
| 15 | [Chains in LangChain](notes/15_chains_in_langchain.md) |
| 16 | [Memory in LangChain](notes/16_memory_in_langchain.md) |
| 17 | [Runnables in LangChain](notes/17_runnables_in_langchain.md) |

The slides use LangChain 0.x classes (`LLMChain`, `SequentialChain`, `ConversationBufferMemory`) that are not in LangChain 1.x. The notes mark each one with a "Correction to the slide" and show the current LCEL and `RunnableWithMessageHistory` versions. Lectures 12–13 (models, prompts) are in [Module 2 · Week 1](../week_01); the LangChain introduction (11) and structured output (14) are in [Module 1 · Week 4](../../02_module1/week_04).

## Code

| Folder | Files |
|---|---|
| [01_chains_in_langchain](01_chains_in_langchain) | No chain vs a simple chain · linear sequential chain · parallel (non-linear) chain · router chain · custom hybrid chain · pre- and post-processing chain |
| [02_memory_in_langchain](02_memory_in_langchain) | No memory · basic message history · summary memory · buffer window memory · token buffer memory |

Each folder has its own `.venv` and `requirements.txt`, and reads its model settings from `config.json` and its API keys from `.env`.
