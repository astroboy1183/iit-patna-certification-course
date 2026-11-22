"""
02_multiquery_retriever.py
--------------------------
Concept: MultiQueryRetriever
Goal:
Demonstrate how to improve retrieval results by expanding a user’s query
into multiple rephrased versions using an LLM.
"""

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from utils.embedding_utils import get_embedding_model

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("\nMULTI-QUERY RETRIEVER DEMO\n" + "-" * 40)

load_dotenv()

docs = [
    Document(page_content="LangChain helps developers build powerful LLM apps."),
    Document(page_content="Retrievers in LangChain fetch relevant data chunks."),
    Document(page_content="FAISS is a local vector store for semantic search."),
    Document(page_content="OpenAI provides APIs for text embeddings and chat models."),
    Document(page_content="Chroma and FAISS are both vector databases used in RAG pipelines."),
]

embedding_model = get_embedding_model("openai")

vectorstore = FAISS.from_documents(docs, embedding_model)
print("✅ FAISS index built successfully.")

base_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm
)

query = "How does LangChain retrieve relevant data?"
print(f"\n Main Query: {query}")

# This will automatically generate multiple reformulations and merge results
unique_docs = multiquery_retriever.invoke(query)

print("\n Retrieved Documents:")
for i, doc in enumerate(unique_docs, 1):
    print(f"{i}. {doc.page_content}")


print("""
----------------------------------------
Key Takeaways:
      
This script shows how to improve search results by automatically turning your question into several different versions, searching with all of them, and combining the results. This helps find more relevant information, even if it’s worded differently in your data.

---

The script will automatically create several similar questions, such as:

- "What is the process LangChain uses to fetch information?"
- "How does LangChain find the right data chunks?"
- "In what way does LangChain search for relevant content?"

It will search using all these versions and combine the results, so you get more complete and accurate answers—even if your data uses different words.      
      
---
      
Pros:

- Finds more relevant results by searching with multiple versions of your question, increasing the chances of matching different ways information is written.
- Reduces the risk of missing important data due to wording differences or synonyms.
      

Cons:

- Uses more resources (time, API calls, and cost) since it runs several searches instead of one.
- May return some duplicate or less relevant results that need to be filtered out.
""")
