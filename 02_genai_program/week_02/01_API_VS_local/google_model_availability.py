import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()
for model in models:
    if "generateContent" in getattr(model, "supported_generation_methods", []):
        print(f"Valid: {model.name}")
    else:
        print(f"lets skip this model -> {model.name}")
        print(f"It supports {getattr(model, 'supported_generation_methods', [])}")
