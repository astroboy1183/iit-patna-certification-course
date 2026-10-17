# Lecture 18 · Introduction to RAG (Week 4)

## Why plain LLMs aren't enough

LLMs such as GPT-4 or Gemini are trained once on a large, **static** snapshot of public data. After that:

- they know nothing about your **private** data (HR policies, claim files, internal FAQs);
- their knowledge stops at a **training cut-off**, so they can't see today's data;
- asked about facts they never saw, they may **hallucinate**: give a confident but false answer.

For a business, that turns into four problems:

| Problem | What goes wrong |
|---|---|
| **Compliance risk** | You can't control or check which sources the answer came from |
| **Accuracy risk** | A hallucinated answer leads to a wrong business decision |
| **Freshness** | The model can't read this week's report |
| **Costly retraining** | Teaching the model new facts by retraining means updating billions of parameters |

The question the lecture builds towards: *can we connect an LLM to trusted company data without retraining it?*

## The core idea: retrieval + generation

**RAG (Retrieval-Augmented Generation)** = before answering, the system **retrieves** relevant passages from an external knowledge base and gives them to the LLM, which **generates** the answer from them.

| Part | Job |
|---|---|
| **Retriever** | Finds the passages most relevant to the question |
| **Generator** (the LLM) | Reads those passages and writes a coherent answer |

- **Without RAG:** the model answers from memory, so there is a hallucination risk.
- **With RAG:** the model answers from retrieved evidence, so the answer can be accurate, up to date and **auditable** (you can show the sources).

Example from the slide, for the prompt *"Summarise the latest insurance claim report"*:

| Without RAG | With RAG |
|---|---|
| "Sorry, I don't have access to recent data." | "According to the August 2025 report, total claims = 312 (+5%), top 3 fraud patterns are …" |

> "If prompting is asking better questions, RAG is giving the model better study notes."

## The RAG pipeline, step by step

RAG has two phases. **Indexing** runs once (and again whenever documents change). **Retrieval + generation** runs on every question.

```
INDEXING (offline)
  documents ──► 1. load ──► 2. split ──► 3. embed ──► 4. store in vector DB

QUERY TIME (per question)
  question ──► embed ──► 5. retrieve top-k chunks ──► 6. LLM(prompt + chunks) ──► grounded answer
```

| # | Step | What it does | Example |
|---|---|---|---|
| 1 | **Document loader** | Reads raw data from `.txt`, `.pdf`, `.docx`, web pages or APIs into documents (text + metadata such as the source) | HR policies, claims data, internal FAQs |
| 2 | **Text splitter** | Breaks long documents into smaller chunks, usually with some **overlap** so a sentence cut at a boundary still appears whole in one chunk | A 20-page PDF → ~500-word chunks |
| 3 | **Embeddings** | Turns each chunk into a vector that captures its meaning; similar meanings give nearby vectors | "fraudulent claim detection" ≈ "insurance scam report" |
| 4 | **Vector store** | A database built for fast similarity search over those vectors: a semantic search engine for your private data | FAISS, Chroma, Pinecone, Milvus |
| 5 | **Retriever** | Embeds the question and returns the **top-k** most similar chunks | "Explain reserve loss adjustment expense" → 3 most relevant policy sections |
| 6 | **LLM (generator)** | Receives the chunks as context in the prompt and writes a grounded, natural-language answer | Answer + citations |

Notes on the steps:

- **Embeddings** are the same idea as in Lecture 3 ([03_what_are_llms.md](../../week_01/notes/03_what_are_llms.md)): text → vector of numbers. Embedding models named on the slide: OpenAI's `text-embedding-3-small` (hosted, paid) and `all-MiniLM-L6-v2` (small, open, runs locally). The **same** embedding model must be used for the chunks and the question, otherwise the vectors aren't comparable.
- **Chunk size is a trade-off.** Too large and a chunk mixes several topics, which blurs its embedding and wastes prompt tokens. Too small and a chunk loses the surrounding context needed to answer.
- **k is a trade-off too.** A small k may miss the right chunk; a large k adds noise and cost.

> **Correction to the slide:** the loader slide says "each document becomes a source chunk". A loader produces whole **documents** (text plus metadata); the **chunks** are created in step 2 by the splitter.

> **Correction to the slide:** the splitter slide gives "GPT-4 = 128k tokens". The original GPT-4 (2023) had an 8k or 32k context window; 128k was **GPT-4 Turbo** and later GPT-4o. Current models go much further (several offer around 1 million tokens), so today the main reasons to split are **retrieval precision and cost**, not just making text fit.

## Benefits of RAG

| Challenge | How RAG helps |
|---|---|
| Outdated model knowledge | Injects current internal or real-world data at question time |
| Hallucinations | Answers are grounded in retrieved text |
| Data privacy | Documents live in your own vector store, not in model weights |
| Fine-tuning cost | No retraining when data changes; just re-index |
| Transparency | Can return the sources as citations |
| Scalability | Add or remove data sources at any time |

> **Correction to the slide:** two rows overstate things. **Hallucinations** are *reduced*, not removed: retrieval can miss the right chunk, and the model can still ignore or misread its context, so prompts should say "answer only from the context, otherwise say you don't know". **Data privacy:** the store may be yours, but the retrieved chunks are sent to the LLM (and the documents to the embedding API, if it's hosted). Sensitive data needs self-hosted models or a provider agreement that covers it.

## Fine-tuning vs RAG (and long context)

The slide's comparison:

| Aspect | Fine-tuning | RAG |
|---|---|---|
| Purpose | Teaches new **behaviour** or style | Adds new **factual knowledge** |
| Where the data lives | Inside the model weights | Outside, in a vector DB |
| Updating | Slow: retrain | Fast: re-embed the changed documents |
| Cost | High (compute + training) | Low (embedding + storage) |
| Use case | Brand tone, a specific task format | Company data, frequently changing knowledge |

This matches the rule of thumb from Lecture 7 ([07_prompt_tuning_vs_fine_tuning.md](../../week_03/notes/07_prompt_tuning_vs_fine_tuning.md)): fine-tune for behaviour, retrieve for facts. The two combine well: a fine-tuned model can still use RAG.

The slides don't cover a third option, **long context**: paste the whole document set into a model with a very large context window. It's simple and works well for a few documents, but every question pays for all those tokens, it gets slow, models can overlook facts buried in the middle of a long prompt, and it stops working once the data outgrows the window. RAG sends only the relevant chunks, so it scales to large, changing collections.

| | Fine-tuning | RAG | Long context |
|---|---|---|---|
| Best for | Behaviour, style, format | Large or changing knowledge bases | A small, fixed set of documents |
| Cost per question | Low | Low to medium (only k chunks) | High (all documents every time) |
| Updating knowledge | Retrain | Re-index | Change the prompt |

## Practical use cases

| Use case | Example |
|---|---|
| Chatbot on private data | "Chat with your policy documents", employee-handbook assistant |
| Research assistant | Pull insights from many PDFs, papers or claim files |
| Knowledge management | Employees search company data in plain language |
| Customer-support copilot | Draft replies from CRM notes and FAQs, faster responses |
| Fraud insights (insurance) | Compare a new claim with retrieved summaries of past claims |

## In code (minimal, runs offline)

A whole retrieve-then-generate flow in LangChain, using an LCEL chain like the ones in [15_chains_in_langchain.md](15_chains_in_langchain.md) and [17_runnables_in_langchain.md](17_runnables_in_langchain.md). To run it without an API key, it uses a toy keyword embedding and a fake chat model; in a real project, swap in e.g. `OpenAIEmbeddings` and `ChatOpenAI` from `langchain-openai`.

```python
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.language_models.fake_chat_models import FakeListChatModel

class KeywordEmbeddings(Embeddings):          # toy stand-in for a real embedding model
    VOCAB = ["leave", "holiday", "claim", "fraud", "laptop", "refund"]
    def _vec(self, text):
        t = text.lower()
        return [float(t.count(w)) + 0.01 for w in self.VOCAB]
    def embed_documents(self, texts):
        return [self._vec(t) for t in texts]
    def embed_query(self, text):
        return self._vec(text)

llm = FakeListChatModel(responses=["Employees get 24 days of annual leave [hr_policy.pdf]."])

# 1. Indexing: (load -> split ->) embed -> store
chunks = [
    Document("Annual leave: employees get 24 days of paid leave (holiday) per year.", metadata={"source": "hr_policy.pdf"}),
    Document("Suspected fraud on a claim must be reported to the claims team within 48 hours.", metadata={"source": "claims_manual.pdf"}),
    Document("Laptops are refreshed every 3 years; contact IT for a replacement.", metadata={"source": "it_faq.txt"}),
]
store = InMemoryVectorStore(embedding=KeywordEmbeddings())
store.add_documents(chunks)
retriever = store.as_retriever(search_kwargs={"k": 1})   # top-k

# 2. Retrieval + generation
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the context. If it isn't there, say you don't know. "
               "Cite the source.\n\nContext:\n{context}"),
    ("human", "{question}"),
])

def format_docs(docs):
    return "\n\n".join(f"[{d.metadata['source']}] {d.page_content}" for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

print(retriever.invoke("How many days of leave do I get?")[0].metadata["source"])  # hr_policy.pdf
print(rag_chain.invoke("How many days of leave do I get?"))
```

Tested with langchain-core 1.6.6: the retriever returns `hr_policy.pdf` for the leave question (and the right file for a fraud and a laptop question), and the system message the model receives contains that chunk with its source tag. The answer text itself is fixed by the fake model; a real LLM would write it from the context.

**Loading and splitting** (steps 1–2) need extra packages that aren't in my live-session venv, so this part is reference only and wasn't run:

```python
# pip install langchain-text-splitters langchain-community pypdf
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = PyPDFLoader("hr_policy.pdf").load()                     # one Document per page
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)                         # sizes are in characters by default
```

> **Takeaway:** RAG doesn't change the model; it changes what the model gets to read. Index your documents once (load → split → embed → store), then for each question retrieve the top-k chunks and let the LLM answer from them, with sources.

## Check yourself

1. Name the four business problems with plain LLMs from the lecture, and say which ones RAG fixes.
2. List the six pipeline steps in order and mark which belong to indexing and which run on every question.
3. Why do chunks overlap, and what goes wrong if chunks are far too large or far too small?
4. Why must the question and the chunks be embedded with the same model?
5. A company wants its bot to answer in its brand voice **and** know this month's prices. Fine-tuning, RAG, or both? Why?
6. "RAG eliminates hallucinations and keeps my data private." Correct both halves of this claim.
