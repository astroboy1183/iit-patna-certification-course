import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.8-flash")
response = model.generate_content("Explain Python Lists in short and simple way.")
print(response)
print(response.text)
