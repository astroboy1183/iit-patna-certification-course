# LLM SDK Cheat Sheet

Quick reference for calling OpenAI, Anthropic, Gemini, Ollama and Hugging Face from Python.
The examples match the versions pinned in this folder's `requirements.txt`.

## The pattern: every SDK does the same 4 things

```
1. import   →  bring in the SDK
2. client   →  create it with your API key
3. call     →  send the model name + your messages
4. read     →  dig the text out of the response
```

| Step | OpenAI | Anthropic | Gemini | Ollama | Hugging Face |
|---|---|---|---|---|---|
| **Import** | `from openai import OpenAI` | `from anthropic import Anthropic` | `import google.generativeai as genai` | `import ollama` | `import requests` |
| **Client** | `OpenAI(api_key=...)` | `Anthropic(api_key=...)` | `genai.configure(api_key=...)` + `genai.GenerativeModel(...)` | none (runs locally) | none (plain HTTP) |
| **Call** | `client.chat.completions.create(...)` | `client.messages.create(...)` | `model.generate_content(prompt)` | `ollama.chat(...)` | `requests.post(url, ...)` |
| **Read** | `r.choices[0].message.content` | `r.content[0].text` | `r.text` | `r["message"]["content"]` | `r.json()["choices"][0]["message"]["content"]` |

The `messages` format is the same for OpenAI, Anthropic, Ollama and Hugging Face:

```python
messages = [{"role": "user", "content": "your question"}]
```

---

## Setup (same for all)

API keys live in `.env`, never in the code:

```
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
HUGGING_FACE_API_KEY=...
```

Load them at the top of every script:

```python
import os

from dotenv import load_dotenv

load_dotenv()
```

The name in `os.getenv("...")` must match `.env` exactly, or you get `None` and a `401 Unauthorized` error.

---

## 1. OpenAI

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    max_tokens=200,
)

print(response.choices[0].message.content)
```

- `max_tokens` is optional.
- Add a system prompt as the first message: `{"role": "system", "content": "You are a helpful tutor."}`

---

## 2. Anthropic (Claude)

```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=200,
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

print(response.content[0].text)
```

- `max_tokens` is **required**. Leaving it out raises an error.
- The system prompt is a separate argument, not a message: `system="You are a helpful tutor."`
- The text is in `content[0].text`, not `choices[...]`.

---

## 3. Gemini (`google-generativeai`)

```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.8-flash")
response = model.generate_content("What is the capital of France?")

print(response.text)
```

- Takes a plain string, not a `messages` list.
- The model is chosen when you create `GenerativeModel`, not in the call.
- Model names change often. Check which ones your key can use with `google_model_availability.py` in this folder.
- Google has a newer SDK, `google-genai`, with a different style (`client = genai.Client()`, then `client.models.generate_content(...)`). Newer tutorials may use it; this folder uses the older one.

---

## 4. Ollama (local models)

```python
import ollama

response = ollama.chat(
    model="mistral",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

print(response["message"]["content"])
```

- No API key: the model runs on your machine, so it's free and works offline.
- The Ollama app must be running, and the model downloaded first: `ollama pull mistral`.
- See downloaded models with `ollama list`. Installed now: `mistral`, `gemma3:270m` (tiny and fast, good for testing).
- In this SDK version the response is a **dictionary**, so use `["message"]["content"]`, not `.message.content`.

---

## 5. Hugging Face (Inference Providers)

```python
import requests

api_url = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}
payload = {
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
    "max_tokens": 200,
}

response = requests.post(api_url, headers=headers, json=payload)
response.raise_for_status()

print(response.json()["choices"][0]["message"]["content"])
```

- Use `router.huggingface.co`. The old `api-inference.huggingface.co` has been retired.
- Model IDs are always `organization/model-name`. Copy them from the model's page.
- The model must be served by a provider enabled on your account. Browse available ones at https://huggingface.co/models?inference_provider=all
- The token needs the "Make calls to Inference Providers" permission.
- See `hf_app.py` for the full list of problems we hit and how we fixed them.

---

## Shortcut: the OpenAI SDK works with the others too

Hugging Face, Gemini and Ollama all offer an OpenAI-compatible endpoint, so the OpenAI code above works with them. Change only `base_url`, `api_key` and `model`:

| Provider | `base_url` | `api_key` |
|---|---|---|
| Hugging Face | `https://router.huggingface.co/v1` | `os.getenv("HUGGING_FACE_API_KEY")` |
| Gemini | `https://generativelanguage.googleapis.com/v1beta/openai/` | `os.getenv("GEMINI_API_KEY")` |
| Ollama | `http://localhost:11434/v1` | `"ollama"` (any text; it's ignored) |

```python
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
response = client.chat.completions.create(
    model="mistral",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)
print(response.choices[0].message.content)
```

Good for basic chat. Provider-specific features (Gemini file uploads, etc.) still need the native SDK.

---

## When something goes wrong

| Error | Meaning | Check |
|---|---|---|
| `401 Unauthorized` | Key missing or wrong | `.env` name matches `os.getenv(...)`; key copied fully |
| `403 Forbidden` | Key valid, no permission | Token permissions / account access |
| `400 Bad Request` | Request is wrong | Model name, parameters. Print `response.text` for the reason |
| `404` / "model not found" | Model name doesn't exist | Copy the exact ID from the provider's docs |
| `429 Too Many Requests` | Rate limit or out of credits | Wait, or check billing / free quota |
| `NameResolutionError` | The domain doesn't exist | URL typo, or a retired endpoint |
| `ConnectionError` with `localhost:11434` | Ollama isn't running | Start the Ollama app |

Can't find the text in a response? `print(response)` shows the whole structure; follow it down to the text.
