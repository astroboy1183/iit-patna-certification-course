"""
02_load_pdf.py
--------------
Concept: PDF Document Loading

Goal:
Demonstrate how to extract text from PDFs using
LangChain’s PyPDFLoader.

LangChain Concept:
DocumentLoader (PDF) → Document[]
"""

import os
from langchain_community.document_loaders import PyPDFLoader

print("\n📘 PDF DOCUMENT LOADER DEMO\n" + "-" * 40)

# Sample file (can be any short PDF)
path = "01_data_ingestion/sample_docs/sample2.pdf"
if not os.path.exists(path):
    print("⚠️ Please add a sample PDF file at:", path)
else:
    loader = PyPDFLoader(path)
    docs = loader.load()

    print(f"✅ Loaded {len(docs)} pages from the PDF.")
    print(f"📖 First Page Preview:\n{docs[0].page_content[2000:2400]}...\n")

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ PyPDFLoader splits PDFs into page-wise Documents.
2️⃣ Perfect for multi-page files like reports or research papers.
3️⃣ Each `Document` has metadata including `page` and `source`.
""")
