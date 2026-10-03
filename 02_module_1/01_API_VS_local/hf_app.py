"""
Call an LLM hosted on Hugging Face through the Inference Providers API.

Problems faced while getting this working, and how each was fixed
====================================================================

1. ConnectionError / NameResolutionError: "Failed to resolve 'api-inference.huggingface.co'"
   - Cause: the original code used the old serverless Inference API at
     https://api-inference.huggingface.co/models/<model_id>. Hugging Face has
     retired that service, so the domain no longer exists in DNS. The
     computer could not turn the name into an IP address, so no connection
     was ever made.
   - How we confirmed it: other domains (huggingface.co, google.com,
     router.huggingface.co) resolved fine. Only the old domain failed, so it
     was not an internet problem.
   - Fix: use the new Inference Providers router at
     https://router.huggingface.co/v1/chat/completions

2. Wrong model ID: "gpt3.5"
   - Cause: GPT-3.5 is an OpenAI model and is not hosted on Hugging Face.
   - Fix: use an open model that Hugging Face serves, written as
     "organization/model-name".

3. 401 Unauthorized
   - Cause: the environment variable name in the code did not match the name
     in .env (HUGGING_FACE_API_KEY vs HUGGINGFACE_API_KEY). os.getenv()
     returned None, so the request was sent with "Authorization: Bearer None".
   - Fix: use exactly the same name in the code and in .env.
     The name used now is HUGGING_FACE_API_KEY.

4. 400 Bad Request: "...is not supported by any provider you have enabled."
   - Cause: Qwen/Qwen2.5-7B-Instruct exists, but none of the inference
     providers enabled on this account host it. The router only accepts
     models that an enabled provider serves.
   - Fix: switch to a model that is served (meta-llama/Llama-3.1-8B-Instruct).
     Available models are listed at
     https://huggingface.co/models?inference_provider=all

5. 400 Bad Request: "The requested model 'Llama-3.1-8B-Instruct' does not exist."
   - Cause: the organization prefix was missing. Hugging Face model IDs are
     always "organization/model-name".
   - Fix: "meta-llama/Llama-3.1-8B-Instruct". Copy model IDs from the model's
     page on huggingface.co instead of typing them.

6. Response format changed
   - Cause: the old API returned [{"generated_text": "..."}]. The router
     returns the OpenAI-style chat format instead.
   - Fix: read the answer from response.json()["choices"][0]["message"]["content"].

Debugging lessons
-----------------
- Read a traceback from the bottom up. Each "The above exception was the
  direct cause of..." line links an error to the one that caused it.
- raise_for_status() shows only the status code (400, 401...). Print
  response.text to see the server's message, which says exactly what is wrong.
- 401 = the API key is missing or invalid. 403 = the key is valid but lacks
  permission (the token needs "Make calls to Inference Providers").
  400 = the request itself is wrong (model name, parameters...).
- The router uses the same format as OpenAI's API, so the openai Python
  package also works here by setting base_url="https://router.huggingface.co/v1".
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

prompt = "What is the currency of india?"

model_id = "meta-llama/Llama-3.1-8B-Instruct"
api_url = "https://router.huggingface.co/v1/chat/completions"

header = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}

payload = {
    "model": model_id,
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 200,
}
response = requests.post(api_url, headers=header, json=payload)

print(response.status_code, response.text)

response.raise_for_status()

print(response.json()["choices"][0]["message"]["content"].strip())
