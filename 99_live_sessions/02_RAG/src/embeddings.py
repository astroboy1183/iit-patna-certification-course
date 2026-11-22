from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

import config


def get_embeddings():
    config.require_api_key()
    provider = config.provider_name()
    model_name = config.embedding_model_name()

    if provider == "openai":
        return OpenAIEmbeddings(model=model_name)

    return GoogleGenerativeAIEmbeddings(model=model_name)


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = 0.0
    left_size = 0.0
    right_size = 0.0
    for a, b in zip(left, right):
        dot += a * b
        left_size += a * a
        right_size += b * b
    return dot / ((left_size ** 0.5) * (right_size ** 0.5))


def _euclidean_distance(left: list[float], right: list[float]) -> float:
    total = 0.0
    for a, b in zip(left, right):
        total += (a - b) ** 2
    return total ** 0.5


if __name__ == "__main__":
    embeddings = get_embeddings()
    print(type(embeddings).__name__)
    print(embeddings.model)

    question = "What time does the museum open on Sunday?"
    similar = "When does the museum open on Sundays?"
    different = "How much does a membership cost?"
    question_vector = embeddings.embed_query(question)
    similar_vector = embeddings.embed_query(similar)
    different_vector = embeddings.embed_query(different)

    print("numbers in one vector:", len(question_vector))
    print("similar sentences:", round(_cosine_similarity(question_vector, similar_vector), 3))
    print("different sentences:", round(_cosine_similarity(question_vector, different_vector), 3))
    print("distance, similar sentences:", round(_euclidean_distance(question_vector, similar_vector), 3))
    print("distance, different sentences:", round(_euclidean_distance(question_vector, different_vector), 3))
    print("same list:", question_vector == similar_vector)
