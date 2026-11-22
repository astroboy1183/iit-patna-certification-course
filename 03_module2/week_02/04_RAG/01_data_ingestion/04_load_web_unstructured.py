"""
04_load_web_unstructured.py
----------------------------
Concept: Unstructured Web Loader

Goal:
Showcase Unstructured.io integration for cleaner, chunked,
semantic text extraction from web pages.

LangChain Concept:
UnstructuredURLLoader → Document[]
"""

from langchain_community.document_loaders import UnstructuredURLLoader

print("\n🧠 UNSTRUCTURED WEB LOADER DEMO\n" + "-" * 40)

urls = [
    "https://scikit-learn.org/stable/",
    "https://www.langchain.com/"
]

loader = UnstructuredURLLoader(urls=urls)
docs = loader.load()

print(f"✅ Loaded {len(docs)} document(s) across {len(urls)} URLs.")
print(f"📘 Sample Extract:\n{docs[0].page_content[:1000]}...\n")

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ Unstructured.io handles complex layouts (e.g. articles, blog posts).
2️⃣ Extracts only meaningful text — skips navigation and HTML noise.
3️⃣ Excellent for RAG ingestion from modern websites.
""")
