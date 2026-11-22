"""
01_recursive_splitter.py
------------------------
Concept: RecursiveCharacterTextSplitter

Goal:
Show how recursive splitting maintains context while chunking
large documents for RAG systems.

LangChain Concept:
TextSplitter → list of smaller Documents
"""

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

path = "02_text_splitters/sample_texts/long_article.txt"
if not os.path.exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(
            "LangChain is a framework for developing applications powered by large language models. "
            "It provides modules to handle prompt templates, chains, agents, and memory. "
            "When building RAG pipelines, it’s important to chunk long documents so they fit "
            "within model context limits while preserving meaning and coherence."
        )

loader = TextLoader(path, encoding="utf-8")
docs = loader.load()
print(f"\n📘 Loaded {len(docs)} document(s).")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,  # characters
    chunk_overlap=20,  # characters
)

chunks = splitter.split_documents(docs)

print("\n✂️ RecursiveCharacterTextSplitter Demo\n" + "-" * 40)
for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i}: {repr(chunk.page_content)}\n")

print(f"✅ Created {len(chunks)} chunks.\n")

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ RecursiveCharacterTextSplitter preserves sentence boundaries.
2️⃣ Overlap (20–50 chars) helps maintain context continuity.
3️⃣ Best for general-purpose RAG ingestion.
""")
