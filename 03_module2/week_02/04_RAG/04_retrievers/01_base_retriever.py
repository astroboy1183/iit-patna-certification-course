"""
01_base_retriever.py
--------------------
Concept: BaseRetriever with FAISS
Goal:
Demonstrate a simple retriever that fetches top-k relevant chunks from a vector store.
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from utils.embedding_utils import get_embedding_model

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("\n BASE RETRIEVER DEMO (FAISS)\n" + "-" * 40)

docs = [
    Document(page_content="LangChain is a framework for building applications using LLMs."),
    Document(page_content="FAISS is a library for efficient similarity search developed by Meta."),
    Document(page_content="Vector databases like FAISS and Chroma are used to store text embeddings."),
    Document(page_content="Retrievers help find the most relevant information from a knowledge base."),
    Document(page_content="OpenAI provides APIs for embeddings, chat models, and completions."),
]

embedding_model = get_embedding_model("local")  # Uses CPU-safe MiniLM embedding

vectorstore = FAISS.from_documents(docs, embedding_model)
print(" FAISS index built successfully.")

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

query = "How does FAISS help in retrieval?"
results = retriever.invoke(query)

print(f"\n Query: {query}")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")

print("""
----------------------------------------
 Key Takeaways:
1️. BaseRetriever simply wraps a vector store to fetch top-k similar docs.
2️. It’s the foundation for advanced retrievers like MultiQuery and Contextual.
3️. Search kwargs let you tune precision via top-k results.
""")
