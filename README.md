# Certificate Program in Generative AI & Agentic AI for Developers (IIT Patna)

My code, notes, and practice assignments from the **Certificate Program in Generative AI & Agentic AI for Developers**, a 6-month program offered by IIT Patna jointly with USDC Projects India Pvt Ltd.

- [Course page](https://certifications.iitpatna.com/generative-ai-for-developers)
- [Brochure (PDF)](https://cep.iitp.ac.in/GenAi_for_Developers_Brochure-.pdf)

## Repository layout

| Folder | Contents |
|---|---|
| [01_Python_Programming](01_Python_Programming) | Python foundations: numbered lessons and practice assignments |
| [02_genai_program](02_genai_program) | The GenAI program week by week: pre-recorded lecture notes and hands-on projects |
| [03_live_sessions](03_live_sessions) | Projects built in the Sunday live sessions |

Each project folder has its own `requirements.txt` and its own virtual environment. See [Setup](#setup).

---

## 01 · Python Programming

Files are numbered in the order they were covered. Lesson files contain code written while following the course. Practice files (`*_practice.py`) contain assignments: the questions are in the docstring at the top of each file, followed by my solutions.

| # | File | Type | Topics covered |
|---|------|------|----------------|
| 1 | [1_print_and_escape_sequences.py](01_Python_Programming/1_print_and_escape_sequences.py) | Lesson | `print()`, `sep` and `end`, f-strings, escape sequences, comments |
| 2 | [2_print_and_escape_sequences_practice.py](01_Python_Programming/2_print_and_escape_sequences_practice.py) | Practice | Commenting code, formatting output with escape sequences, `sep`/`end` in one `print()` |
| 3 | [3_variables_and_data_types.py](01_Python_Programming/3_variables_and_data_types.py) | Lesson | Variables, `str`/`int`/`float`/`bool`, `type()`, Python keywords |
| 4 | [4_variables_and_data_types_practice.py](01_Python_Programming/4_variables_and_data_types_practice.py) | Practice | Predicting types, string-to-`int` conversion, invalid variable names, dynamic typing |
| 5 | [5_user_input.py](01_Python_Programming/5_user_input.py) | Lesson | `input()`, converting input with `int()` |
| 6 | [6_user_input_and_type_casting_practice.py](01_Python_Programming/6_user_input_and_type_casting_practice.py) | Practice | Calculating age with `datetime`, arithmetic on input, casting between `float`, `int`, and `str` |
| 7 | [7_operators.py](01_Python_Programming/7_operators.py) | Lesson | Arithmetic, comparison, and logical operators |
| 8 | [8_operators_practice.py](01_Python_Programming/8_operators_practice.py) | Practice | Conditions with comparison and logical operators, conditional expressions, divisibility checks |
| 9 | [9_strings.py](01_Python_Programming/9_strings.py) | Lesson | Indexing, slicing, concatenation, `in`, `len()`, string methods |
| 10 | [10_strings_practice.py](01_Python_Programming/10_strings_practice.py) | Practice | Slicing and reversing, `split()`, `count()`, `replace()`, `endswith()` |
| 11 | [11_debugging.py](01_Python_Programming/11_debugging.py) | Lesson | A recap program combining output, input, casting, operators, and strings |
| 12 | [12_debugging_practice.py](01_Python_Programming/12_debugging_practice.py) | Practice | Finding and fixing type errors with type casting |
| 13 | [13_lists.py](01_Python_Programming/13_lists.py) | Lesson | Creating and indexing lists, `append`, `insert`, `remove`, `pop`, `sort`, `reverse`, `extend`, slicing, nested lists |
| 14 | [14_lists_practice.py](01_Python_Programming/14_lists_practice.py) | Practice | List methods, building lists from user input, reverse slicing, membership checks, nested lists |
| 15 | [15_loops_if_else_.py](01_Python_Programming/15_loops_if_else_.py) | Lesson | `if`/`elif`/`else`, `for` loops over lists, type checks inside loops |
| 16 | [16_loops_if_else_practice.py](01_Python_Programming/16_loops_if_else_practice.py) | Practice | Even/odd checks, `continue`, `while` with `break`, sums with loops, counting vowels, a 3-attempt login with `getpass` |
| 17 | [17_docstrings_practice.py](01_Python_Programming/17_docstrings_practice.py) | Practice | Functions with docstrings, f-string formatting, a report card |
| 18 | [18_functions_practice.py](01_Python_Programming/18_functions_practice.py) | Practice | Functions, default arguments, `*args`, `**kwargs`, a multi-operation `calculate()` |
| 19 | [19_tuples_practice.py](01_Python_Programming/19_tuples_practice.py) | Practice | Tuple indexing and slicing, `count()`, `index()`, unpacking, immutability |
| 20 | [20_dictionaries_practice.py](01_Python_Programming/20_dictionaries_practice.py) | Practice | Looping over key-value pairs, adding keys, `.get()`, character frequency counts, nested dictionaries |
| 21 | [21_sets_practice.py](01_Python_Programming/21_sets_practice.py) | Practice | Removing duplicates, intersection, difference, fast membership checks |

---

## 02 · GenAI program, week by week

Full index with lecture notes and key ideas: [02_genai_program/README.md](02_genai_program/README.md).

| Week | Theory notes | Hands-on |
|---|---|---|
| [Week 1](02_genai_program/week_01) | [Lectures 0–4](02_genai_program/week_01/notes): roadmap, what GenAI is, ML vs GenAI, how LLMs work, Responsible AI | — |
| [Week 2](02_genai_program/week_02) | [Lecture 5](02_genai_program/week_02/notes): the developer mindset | Cloud APIs vs local models · CLI chatbot · Streamlit chat assistant (below) |
| [Week 3](02_genai_program/week_03) | [Lectures 7–8](02_genai_program/week_03/notes): prompt tuning vs fine-tuning, LoRA and QLoRA | — |

### Week 2 · [01_API_VS_local](02_genai_program/week_02/01_API_VS_local): calling LLMs through cloud APIs and locally

| File | What it does |
|---|---|
| [openai_app.py](02_genai_program/week_02/01_API_VS_local/openai_app.py) | Chat completion with the OpenAI SDK |
| [gemini_app.py](02_genai_program/week_02/01_API_VS_local/gemini_app.py) | Text generation with the Gemini SDK (`google-generativeai`) |
| [google_model_availability.py](02_genai_program/week_02/01_API_VS_local/google_model_availability.py) | Lists the Gemini models available to an API key that support `generateContent` |
| [ollama_app.py](02_genai_program/week_02/01_API_VS_local/ollama_app.py) | Runs a local model (Mistral) through Ollama |
| [hf_app.py](02_genai_program/week_02/01_API_VS_local/hf_app.py) | Calls an open model through Hugging Face Inference Providers, with notes on every error hit along the way and how it was fixed |
| [compare_models.py](02_genai_program/week_02/01_API_VS_local/compare_models.py) | Sends the same prompt to OpenAI, Gemini, Ollama, and Hugging Face to compare their answers |
| [SDK_CHEATSHEET.md](02_genai_program/week_02/01_API_VS_local/SDK_CHEATSHEET.md) | Side-by-side reference for the OpenAI, Anthropic, Gemini, Ollama, and Hugging Face SDKs, plus common errors |

### Week 2 · [02_chatbot](02_genai_program/week_02/02_chatbot): a CLI chatbot with switchable providers

A command-line chatbot that reads the provider and model from [config.json](02_genai_program/week_02/02_chatbot/config.json), so it can switch between OpenAI and Gemini without code changes.

- [main.py](02_genai_program/week_02/02_chatbot/main.py): loads the config and `.env`, and runs the chat loop
- [llm_provider.py](02_genai_program/week_02/02_chatbot/llm_provider.py): an `LLMProvider` class that wraps both SDKs behind one `chat()` method

### Week 2 · [03_capstone](02_genai_program/week_02/03_capstone): a Streamlit chat assistant

A web chat UI with conversation memory, routing to OpenAI or Gemini from [config.json](02_genai_program/week_02/03_capstone/config.json).

- [app.py](02_genai_program/week_02/03_capstone/app.py): the Streamlit chat interface and session history
- [llm_providers.py](02_genai_program/week_02/03_capstone/llm_providers.py): OpenAI and Gemini calls behind one `run_llm()` router

---

## 03 · Live sessions

Projects built during the program's Sunday live sessions.

### Live session 01 · [Call-transcript classification and QA](03_live_sessions/01_call_transcript_qa)

Built in the Sunday live session: a LangChain pipeline that classifies customer-support calls (`billing`, `claims`, `complaint`, `general_query`) and scores tone, resolution quality and knowledge accuracy with Pydantic-validated outputs.

- [experiment.ipynb](03_live_sessions/01_call_transcript_qa/experiment.ipynb): the pipeline, built step by step
- [config/config.json](03_live_sessions/01_call_transcript_qa/config/config.json): models, temperature, evaluation criteria and labels
- [data/](03_live_sessions/01_call_transcript_qa/data): sample call transcripts

---

## Setup

Each project folder has its own virtual environment, built from its own `requirements.txt` with Python 3.13:

```bash
cd 02_genai_program/week_02/02_chatbot
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The GenAI projects read API keys from a `.env` file in the project folder, which is not committed:

```
OPENAI_API_KEY=...
GEMINI_API_KEY=...
HUGGING_FACE_API_KEY=...
```

Local models need [Ollama](https://ollama.com) installed and the model downloaded, e.g. `ollama pull mistral`.

## Running the code

```bash
# Python practice (each file runs on its own; practice files ask for input)
cd 01_Python_Programming
python 8_operators_practice.py

# CLI chatbot
cd 02_genai_program/week_02/02_chatbot
python main.py
```
