import os

import google.generativeai as genai
from openai import OpenAI


class LLMProvider:
    def __init__(self, config):
        self.provider = config["provider"]
        self.model = config["models"][self.provider]
        if self.provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise ValueError("OpenAI API KEY Environment Variable not set.")
            self.client = OpenAI(api_key=key)
        elif self.provider == "gemini":
            key = os.getenv("GEMINI_API_KEY")
            if not key:
                raise ValueError("Gemini API KEY Environment Variable not set.")
            genai.configure(api_key=key)
            self.client = genai.GenerativeModel(self.model)
        else:
            raise ValueError(f"Unsupported Provider: {self.provider}")
        print(f"{self.provider.title()} client initiated successfully.")

    def chat(self, user_message):
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": user_message}],
                    max_tokens=1000,
                )
                return response.choices[0].message.content
            elif self.provider == "gemini":
                response = self.client.generate_content(user_message)
                return response.text
        except Exception as e:
            raise Exception(f"Error in {self.provider} chat: {str(e)}")
