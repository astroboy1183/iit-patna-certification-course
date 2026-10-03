import logging
import os

import google.generativeai as genai
import ollama
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
huggingface_api_key = os.getenv("HUGGING_FACE_API_KEY")

# prompt
prompt = "What is the currency of USA?"


def run_openai(prompt: str) -> str:
    from openai import OpenAI

    try:
        client = OpenAI(api_key=openai_api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API failed: {e}")
        return e


def run_gemini(prompt: str) -> str:

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        logging.error(f"Gemini API failed: {e}")
        return e


def run_ollama(prompt: str) -> str:

    try:
        response = ollama.chat(
            model="mistral", messages=[{"role": "user", "content": prompt}]
        )

        return response
    except Exception as e:
        logging.error(f"Ollama API failed: {e}")
        return e


def run_huggingface(prompt: str) -> str:
    import requests

    try:
        api_url = "https://router.huggingface.co/v1/chat/completions"
        header = {"Authorization": f"Bearer {huggingface_api_key}"}
        payload = {
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
        }

        response = requests.post(api_url, headers=header, json=payload)

        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"HuggingFace API failed: {e}")
        return e


if __name__ == "__main__":
    print("********CHATGPT**********")
    print(run_openai(prompt))
    # print("********OLLAMMA**********")
    # print(run_ollama(prompt))
    print("********GEMINI**********")
    print(run_gemini(prompt))
    print("********HUGGINGFACE**********")
    print(run_huggingface(prompt))
    print("********ALL DONE**********")
