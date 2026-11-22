rag-components-hands-on/
│── README.md                                # Learning roadmap
│── requirements.txt                         # All RAG-related dependencies
│
├── 01_data_ingestion/
│   │── 01_load_txt.py                       # Simple TXT loader demo
│   │── 02_load_pdf.py                       # PyPDFLoader demo
│   │── 03_load_web_bs4.py                   # Web page loader with BeautifulSoup
│   │── 04_load_web_unstructured.py          # Unstructured.io web loader (modern)
│   │── 05_compare_loaders.py                # Compare different loaders
│   │── sample_docs/                         # Example .txt, .pdf, .html docs
│
├── 02_text_splitters/
│   │── 01_recursive_splitter.py             # RecursiveCharacterTextSplitter demo
│   │── 02_token_splitter.py                 # TokenTextSplitter demo
│   │── 03_chunk_tuning_experiment.py        # Chunk size, overlap comparison
│   │── 04_best_practices_notes.md           # Guidelines on chunking tradeoffs
│
├── 03_vectorstores/
│   │── 01_faiss_basic.py                    # Create FAISS vector store (local)
│   │── 02_chroma_basic.py                   # Chroma vector DB demo
│   │── 03_faiss_vs_chroma_comparison.py     # Compare speed & persistence
│   │── 04_store_embeddings_best_practices.md# Embedding storage & reuse
│
├── 04_retrievers/
│   │── 01_base_retriever.py                 # Simple retriever with FAISS
│   │── 02_multiquery_retriever.py           # MultiQueryRetriever demo
│   │── 03_contextual_retriever.py           # ContextualCompressionRetriever demo
│   │── 04_comparison_summary.md             # Compare retriever behaviors

