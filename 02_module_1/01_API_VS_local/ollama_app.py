import ollama

prompt = "What is the capital of singapore?"

response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

print(response["message"]["content"].strip())
