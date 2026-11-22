"""
01_load_txt.py
--------------
Concept: Simple TXT Loader

Goal:
Demonstrate how to load plain text documents into LangChain
using the modern DocumentLoader interface.

LangChain Concept:
DocumentLoader → Document[]
"""

import os
from langchain_community.document_loaders import TextLoader

print("\n📄 TXT DOCUMENT LOADER DEMO\n" + "-" * 40)

# Ensure the file exists
path = "01_data_ingestion/sample_docs/sample1.txt"
if not os.path.exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("LangChain helps developers build applications powered by LLMs.")

# Load file
loader = TextLoader(path)
docs = loader.load()

print(f"✅ Loaded {len(docs)} document(s).")
print(f"📘 Content Preview:\n{docs[0].page_content}\n")

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ TextLoader is perfect for plain-text sources.
2️⃣ Each document becomes a LangChain `Document` object.
3️⃣ Useful for notes, logs, or pre-cleaned datasets.
""")
