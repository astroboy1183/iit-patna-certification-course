# Live session 01 · Call-transcript classification and QA evaluation

Built during the program's Sunday live session. A LangChain pipeline over customer-support call transcripts:

1. **Classify** each call as `billing`, `claims`, `complaint` or `general_query` (Pydantic-validated output with a confidence score).
2. **Route** each call to the evaluations that matter for its type.
3. **Score** tone and empathy, resolution quality and knowledge accuracy (1–5, with a justification), each with its own prompt and parser.

| File | Purpose |
|---|---|
| [experiment.ipynb](experiment.ipynb) | The pipeline, built step by step |
| [config/config.json](config/config.json) | Models, temperature, evaluation criteria, classification labels |
| [data/](data) | Sample call transcripts |

Run it with the venv in this folder (`pip install -r requirements.txt`) and `OPENAI_API_KEY` or `GEMINI_API_KEY` plus `LLM_PROVIDER` in a `.env` file.
