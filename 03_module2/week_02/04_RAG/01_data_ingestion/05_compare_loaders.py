"""
05_compare_loaders.py
---------------------
Concept: Comparing Document Loaders

Goal:
Show side-by-side behavior of TXT, PDF, and Web loaders.
"""

import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, BSHTMLLoader
import requests, tempfile

print("\n📊 DOCUMENT LOADER COMPARISON\n" + "-" * 40)

# TXT
txt_loader = TextLoader("01_data_ingestion/sample_docs/sample1.txt")
txt_docs = txt_loader.load()

# PDF
pdf_path = "01_data_ingestion/sample_docs/sample2.pdf"
pdf_docs = []
if os.path.exists(pdf_path):
    pdf_docs = PyPDFLoader(pdf_path).load()
else:
    print("⚠️ Skipping PDF test (sample missing)")

# WEB
url = "https://langchain.com/"
html = requests.get(url).text
tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
with open(tmp_path, "w", encoding="utf-8") as f:
    f.write(html)
web_docs = BSHTMLLoader(tmp_path).load()

# Compare
print(f"TXT: {len(txt_docs)} doc(s)")
print(f"PDF: {len(pdf_docs)} doc(s)")
print(f"WEB: {len(web_docs)} doc(s)")
print(f"🧩 Combined total: {len(txt_docs) + len(pdf_docs) + len(web_docs)} document objects\n")

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ Each loader is tailored for a different content source.
2️⃣ All produce LangChain `Document` objects → easy downstream use.
3️⃣ Mix & match loaders for hybrid corpora (PDFs + Web + Notes).
""")
