from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

import config


def get_chat_model():
    config.require_api_key()
    provider = config.provider_name()
    model_name = config.chat_model_name()

    if provider == "openai":
        return ChatOpenAI(model=model_name, temperature=0)

    return ChatGoogleGenerativeAI(model=model_name, temperature=0)


def read_model_text(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        texts: list[str] = []
        for block in content:
            if isinstance(block, str):
                texts.append(block)
            elif isinstance(block, dict):
                text = block.get("text") or ""
                if text:
                    texts.append(str(text))
        return "\n".join(texts).strip()

    return str(content).strip()
