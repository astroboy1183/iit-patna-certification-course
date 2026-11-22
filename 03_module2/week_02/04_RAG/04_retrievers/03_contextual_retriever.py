"""
03_contextual_retriever.py
--------------------------
Concept: ContextualCompressionRetriever
Goal:
Show how to use an LLM to filter and condense retrieved chunks dynamically,
keeping only the most relevant text for the query.
"""

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from utils.embedding_utils import get_embedding_model

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("\nCONTEXTUAL COMPRESSION RETRIEVER DEMO\n" + "-" * 40)

load_dotenv()

docs = [
    Document(page_content="LangChain is a framework for building applications powered by LLMs like GPT-4."),
    Document(page_content="LangChain includes retrievers, memory, and chains for modular AI app development."),
    Document(page_content="FAISS and Chroma are popular vector databases used for semantic search."),
    Document(page_content="Retrievers fetch relevant chunks of information to answer a query."),
    Document(page_content="In RAG, the retriever brings in context which the LLM uses to generate grounded answers."),
    Document(page_content="OpenAI’s GPT models can summarize, filter, and rank text based on relevance."),
]

embedding_model = get_embedding_model("local")
vectorstore = FAISS.from_documents(docs, embedding_model)
print("✅ FAISS store built successfully.")

base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
compressor = LLMChainFilter.from_llm(llm)
contextual_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever,
)

query = "What are retrievers used for in LangChain?"
print(f"\nQuery: {query}\n")

compressed_docs = contextual_retriever.invoke(query)

print("Filtered & Compressed Contexts:")
for i, doc in enumerate(compressed_docs, 1):
    print(f"{i}. {doc.page_content}")

print("""
----------------------------------------
 Key Takeaways:

High-level explanation:
This script shows how to use an AI model to filter and shorten search results, so you only get the most relevant parts of the information for your question.
---
Example:
If you ask, "What are retrievers used for in LangChain?" and some documents talk about many topics, the script will pick out and return only the sentences or sections that explain what retrievers do, ignoring unrelated details.
---
Pros & Cons of Contextual Compression Retriever:

Pros:
- Gives you focused, relevant answers by removing unrelated or extra information.
- Useful when documents are long or cover many topics.

Cons:
- Uses more compute and may be slower, since it runs an AI model on each result.
- Might accidentally filter out useful context if not set up carefully.      
""")
