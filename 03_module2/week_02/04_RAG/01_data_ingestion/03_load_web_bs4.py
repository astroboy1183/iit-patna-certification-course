"""
03_load_web_bs4.py
------------------
Concept: Web Page Loader (BeautifulSoup)

Goal:
Extract text content from a live web page using LangChain’s
`BSHTMLLoader` — ideal for static web scraping.

LangChain Concept:
HTMLLoader → Document[]
"""

from langchain_community.document_loaders import BSHTMLLoader
import tempfile, requests, os

print("\n🌐 WEB LOADER (BS4) DEMO\n" + "-" * 40)

# Example page (you can replace)
url = "https://langchain.com/"
html = requests.get(url).text

# Save temporarily
tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
with open(tmp_path, "w", encoding="utf-8") as f:
    f.write(html)

# Load using BS4 loader
loader = BSHTMLLoader(tmp_path, open_encoding="utf-8")
docs = loader.load()

print(f"✅ Loaded {len(docs)} document(s) from {url}")
print(f"📄 Content snippet:\n{docs[0].page_content[1000:1200]}...\n")

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ BSHTMLLoader cleans and parses HTML via BeautifulSoup.
2️⃣ Great for extracting readable content from static pages.
3️⃣ Use responsibly — avoid scraping dynamic or restricted sites.
""")
