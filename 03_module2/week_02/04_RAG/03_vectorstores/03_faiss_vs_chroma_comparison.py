"""
03_faiss_vs_chroma_comparison.py
--------------------------------
Concept: Compare FAISS vs. Chroma

Goal:
Show key differences between FAISS and Chroma for vector storage and retrieval.
"""

from utils.embedding_utils import get_embedding_model
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.documents import Document

print("\n FAISS VS CHROMA COMPARISON\n" + "-" * 40)

docs = [
    Document(page_content="LangChain supports multiple vector stores."),
    Document(page_content="FAISS is optimized for fast in-memory search."),
    Document(page_content="Chroma supports persistent local databases."),
]

embedding_model = get_embedding_model("openai")

# Create both stores
faiss_store = FAISS.from_documents(docs, embedding_model)
chroma_store = Chroma.from_documents(
    docs,
    embedding_model,
    persist_directory="03_vectorstores/chroma_compare"
)

query = "Which one is faster for search?"
print("\n Query:", query)

faiss_results = faiss_store.similarity_search(query, k=1)
chroma_results = chroma_store.similarity_search(query, k=1)

print("\n FAISS Result:", faiss_results[0].page_content)
print(" Chroma Result:", chroma_results[0].page_content)

print("""
----------------------------------------
 Key Takeaways:
- FAISS → In-memory, super fast, ideal for quick experiments.
- Chroma → Persistent, reloadable, great for long-term storage.
- Both integrate seamlessly into LangChain retrievers.
""")
