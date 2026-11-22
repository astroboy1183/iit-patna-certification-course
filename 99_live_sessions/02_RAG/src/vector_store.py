import hashlib
import json
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

import config
from src.loader import _supported_files

MANIFEST_NAME = "manifest.json"
APP_MARKER = "rag-live-session"
INDEX_FILE_NAMES = ("index.faiss", "index.pkl", MANIFEST_NAME)


def _read_own_manifest(directory: Path) -> dict | None:
    manifest_path = directory / MANIFEST_NAME
    index_path = directory / "index.faiss"
    store_path = directory / "index.pkl"
    has_index_files = index_path.exists() or store_path.exists()

    if not manifest_path.exists():
        if has_index_files:
            raise RuntimeError(
                "The vector_store folder has index files without a manifest "
                "from this app. Click Rebuild index, or remove those files."
            )
        return None

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "vector_store/manifest.json could not be read. "
            "Click Rebuild index to create a new index."
        ) from exc

    if manifest.get("created_by") != APP_MARKER:
        raise RuntimeError(
            "The vector_store folder was not created by this app. "
            "Remove its files or choose a different VECTOR_STORE_DIR in config.py."
        )
    if not index_path.exists() or not store_path.exists():
        raise RuntimeError(
            "The saved index is incomplete. Click Rebuild index to create it again."
        )
    return manifest


def make_fingerprint(data_dir: Path = config.DATA_DIR) -> str:
    if not data_dir.exists():
        raise FileNotFoundError(
            f"Data folder not found: {data_dir}. "
            "Create it and add .txt, .pdf, or .docx files."
        )

    pieces = [
        config.provider_name(),
        config.embedding_model_name(),
        str(config.CHUNK_SIZE),
        str(config.CHUNK_OVERLAP),
    ]
    supported_files, _duplicate_warnings = _supported_files(data_dir)
    for path in supported_files:
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        pieces.append(f"{path.name}:{file_hash}")

    return hashlib.sha256("\n".join(pieces).encode("utf-8")).hexdigest()


def clear_index(directory: Path = config.VECTOR_STORE_DIR) -> None:
    if not directory.exists():
        return
    for name in INDEX_FILE_NAMES:
        path = directory / name
        if path.exists():
            path.unlink()


def save_index(
    chunks: list[Document],
    embeddings,
    directory: Path = config.VECTOR_STORE_DIR,
    data_dir: Path = config.DATA_DIR,
):
    if not chunks:
        raise ValueError("Cannot build an index because there are no text chunks.")

    directory.mkdir(parents=True, exist_ok=True)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(str(directory))

    manifest = {
        "created_by": APP_MARKER,
        "fingerprint": make_fingerprint(data_dir),
        "provider": config.provider_name(),
        "embedding_model": config.embedding_model_name(),
    }
    manifest_path = directory / MANIFEST_NAME
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return vector_store


def load_index(
    embeddings,
    directory: Path = config.VECTOR_STORE_DIR,
    data_dir: Path = config.DATA_DIR,
):
    manifest = _read_own_manifest(directory)
    if manifest is None:
        return None
    if manifest.get("fingerprint") != make_fingerprint(data_dir):
        return None

    return FAISS.load_local(
        str(directory),
        embeddings,
        allow_dangerous_deserialization=True,
    )
