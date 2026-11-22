"""
03_chunk_tuning_experiment.py
-----------------------------
Concept: Chunk Size & Overlap Tuning

Goal:
Show how changing chunk size and overlap affects
the number and readability of text chunks.

LangChain Concept:
Experiment-driven chunk optimization.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

print("\n📊 CHUNK TUNING EXPERIMENT\n" + "-" * 40)

path = "02_text_splitters/sample_texts/long_article.txt"

loader = TextLoader(path, encoding="utf-8")
docs = loader.load()

# Different settings
experiments = [
    {"chunk_size": 50, "overlap": 0},
    {"chunk_size": 100, "overlap": 20},
    {"chunk_size": 150, "overlap": 50},
]

for cfg in experiments:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["chunk_size"],
        chunk_overlap=cfg["overlap"],
    )
    chunks = splitter.split_documents(docs)
    print(f"\n🧪 Chunk Size: {cfg['chunk_size']} | Overlap: {cfg['overlap']}")
    print(f"➡️ Produced {len(chunks)} chunks")
    print(f"Example Chunk:\n{chunks[0].page_content}\n")

print("""
----------------------------------------
📘 Key Takeaways:
1️⃣ Larger chunk_size → fewer, longer documents.
2️⃣ Overlap improves coherence but adds redundancy.
3️⃣ Tune based on content complexity and model context window.
""")
