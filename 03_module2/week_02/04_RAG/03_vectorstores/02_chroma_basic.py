"""
02_chroma_basic.py
------------------
Concept: Chroma Vector Store (Persistent)

Goal:
Demonstrate how to store embeddings in Chroma
for persistent vector retrieval.
"""

import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.embedding_utils import get_embedding_model

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("\nCHROMA VECTOR STORE DEMO\n" + "-" * 40)

docs = [
    Document(page_content="Python is a great language for AI and data science."),
    Document(page_content="Chroma is an open-source vector database."),
    Document(page_content="Embeddings capture the meaning of text in vector form."),
]

print("🔹 Loading embedding model...")
embedding_model = get_embedding_model("openai")
print("✅ Embedding model ready.")

persist_dir = os.path.abspath("03_vectorstores/chroma_db")
os.makedirs(persist_dir, exist_ok=True)

print(f"🔹 Creating Chroma store at: {persist_dir}")
vectorstore = Chroma.from_documents(
    docs,
    embedding_model,
    persist_directory=persist_dir
)
print("✅ Chroma store created and persisted.")

query = "What is Chroma?"
print(f"\n🔍 Query: {query}")
results = vectorstore.similarity_search(query, k=2)
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")

print("\n♻️ Reloading Chroma store to test persistence...")
reloaded = Chroma(
    persist_directory=persist_dir,
    embedding_function=embedding_model
)
res2 = reloaded.similarity_search("AI language")
for doc in res2:
    print("→", doc.page_content)

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ Chroma provides persistent storage for embeddings.
2️⃣ Perfect for local mini-RAG systems.
3️⃣ Integrates natively with LangChain retrievers.
""")
