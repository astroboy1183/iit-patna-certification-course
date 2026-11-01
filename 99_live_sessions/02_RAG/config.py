import json
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_FILE = PROJECT_ROOT / "config.json"

load_dotenv(PROJECT_ROOT / ".env")

TEXT_SETTINGS = (
    "llm_provider",
    "openai_chat_model",
    "openai_embedding_model",
    "gemini_chat_model",
    "gemini_embedding_model",
)

NUMBER_SETTINGS = ("chunk_size", "chunk_overlap", "retriever_k")


def load_settings(path: Path = CONFIG_FILE) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Setting file not found: {path}. Create config.json")
    try:
        settings = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"config.json is not valid JSON (line {exc.lineno}, column {exc.colno}). "
            "Check for a missing comma or quote."
        ) from exc

    if not isinstance(settings, dict):
        raise ValueError("not dictionary")

    allowed = TEXT_SETTINGS + NUMBER_SETTINGS

    for name in settings:
        if name not in allowed:
            raise ValueError(
                f"Unknown setting '{name}' in config.json. "
                f"Allowed settings: {', '.join(allowed)}."
            )
    for name in allowed:
        if name not in settings:
            raise ValueError(f"config.json is missing the setting '{name}'.")

    for name in TEXT_SETTINGS:
        if not isinstance(settings[name], str) or not settings[name].strip():
            raise ValueError(
                f"'{name}' in config.json must be a non-empty text value in quotes."
            )

    for name in NUMBER_SETTINGS:
        value = settings[name]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                f"'{name}' in config.json must be a whole number without quotes."
            )
    return settings


_settings = load_settings()

OPENAI_CHAT_MODEL = _settings["openai_chat_model"]
OPENAI_EMBEDDING_MODEL = _settings["openai_embedding_model"]
LLM_PROVIDER = _settings["llm_provider"]

GEMINI_CHAT_MODEL = _settings["gemini_chat_model"]
GEMINI_EMBEDDING_MODEL = _settings["gemini_embedding_model"]

CHUNK_SIZE = _settings["chunk_size"]
CHUNK_OVERLAP = _settings["chunk_overlap"]
RETRIEVER_K = _settings["retriever_k"]

DATA_DIR = PROJECT_ROOT / "data"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"


def provider_name():
    name = str(LLM_PROVIDER).lower().strip()
    if name not in ("openai", "gemini"):
        raise ValueError(f"Unsupported provider {LLM_PROVIDER}. ")
    return name


def chat_model_name() -> str:
    """Return the chat model that matches the selected provider."""
    if provider_name() == "openai":
        return OPENAI_CHAT_MODEL
    return GEMINI_CHAT_MODEL


def embedding_model_name() -> str:
    """Return the embedding model that matches the selected provider."""
    if provider_name() == "openai":
        return OPENAI_EMBEDDING_MODEL
    return GEMINI_EMBEDDING_MODEL


def require_api_key() -> None:
    provider = provider_name()
    if provider == "openai":
        if os.getenv("OPENAI_API_KEY", "").strip():
            return
        raise RuntimeError("Missing OPENAI API Key")

    if os.getenv("GOOGLE_API_KEY", "").strip():
        return
    raise RuntimeError(
        "Missing Google API key. Copy .env.example to .env, "
        "set GOOGLE_API_KEY, and restart the app."
    )
