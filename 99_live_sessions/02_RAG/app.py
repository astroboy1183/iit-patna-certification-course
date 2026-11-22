import streamlit as st

import config
from src.embeddings import get_embeddings
from src.llm_client import get_chat_model, read_model_text
from src.loader import find_file_warnings, load_documents
from src.retriever import retrieve
from src.splitter import split_documents
from src.vector_store import clear_index, load_index, make_fingerprint, save_index


def build_prompt(question: str, documents: list) -> str:
    blocks: list[str] = []
    for number, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "unknown")
        blocks.append(f"[{number}] Source: {source}\n{document.page_content}")

    if blocks:
        context = "\n\n".join(blocks)
    else:
        context = "No document passages were retrieved."
    prompt = f"""You answer questions about the Riverdale Science Museum.
Use only the context below. If the context does not contain enough information, say that you do not have enough information in the documents.
Do not invent prices, times, names, or rules.

Context:
{context}

Question: {question}
"""
    return prompt


def answer_question(vector_store, question: str) -> tuple[str, list[str]]:
    documents = retrieve(vector_store, question, k=config.RETRIEVER_K)
    if not documents:
        return (
            "I could not find any passages in the local documents for that question.",
            [],
        )

    model = get_chat_model()
    response = model.invoke(build_prompt(question, documents))
    answer = read_model_text(response)
    if not answer:
        raise RuntimeError("The chat model returned an empty answer.")

    sources: list[str] = []
    for document in documents:
        name = str(document.metadata.get("source", "unknown"))
        if name not in sources:
            sources.append(name)
    return answer, sources


@st.cache_resource(show_spinner=False)
def load_or_build_index(fingerprint: str):
    embeddings = get_embeddings()
    vector_store = load_index(embeddings)
    if vector_store is not None:
        return vector_store

    documents, _warnings = load_documents()
    chunks = split_documents(documents)
    if not chunks:
        raise ValueError("The documents did not contain any text to index.")
    return save_index(chunks, embeddings)


def main() -> None:
    st.title("Basic RAG Chatbot")
    st.write(
        "Ask a question about the Riverdale Science Museum sample documents. "
        "The app searches the local files first, then asks the chat model to "
        "answer from the passages it found."
    )
    try:
        st.caption(
            f"Provider: {config.provider_name()} | "
            f"Chat model: {config.chat_model_name()} | "
            f"Embedding model: {config.embedding_model_name()}"
        )
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    st.caption(
        "Try: What is the dinosaur skeleton named? "
        "What time does the museum close on Sunday? "
        "How much is the Saturday robotics workshop?"
    )

    if st.button("Rebuild index"):
        clear_index()
        load_or_build_index.clear()
        st.session_state.messages = []

    try:
        for warning in find_file_warnings():
            st.warning(warning)
        with st.spinner("Preparing the local search index..."):
            vector_store = load_or_build_index(make_fingerprint())
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            sources = message.get("sources") or []
            if sources:
                st.caption("Sources: " + ", ".join(sources))

    question = st.chat_input("Ask a question about the museum documents.")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching the documents and writing an answer..."):
                answer, sources = answer_question(vector_store, question)
        except Exception as exc:
            st.error(f"The language model request failed. Details: {exc}")
            return

        st.markdown(answer)
        if sources:
            st.caption("Sources: " + ", ".join(sources))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )


if __name__ == "__main__":
    main()
