from langchain_core.documents import Document

import config


def retrieve(
    vector_store,
    question: str,
    k: int = config.RETRIEVER_K,
) -> list[Document]:
    if not question or not question.strip():
        raise ValueError("Enter a question before searching the documents.")
    if k < 1:
        raise ValueError("retriever_k in config.json must be at least 1.")

    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(question.strip())
