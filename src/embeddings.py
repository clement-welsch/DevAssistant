from openai import OpenAI

from .config import (
    LMSTUDIO_API_KEY,
    LMSTUDIO_BASE_URL,
    LMSTUDIO_EMBEDDING_MODEL,
)


client = OpenAI(
    base_url=LMSTUDIO_BASE_URL,
    api_key=LMSTUDIO_API_KEY,
)


def embed(texts):
    response = client.embeddings.create(
        model=LMSTUDIO_EMBEDDING_MODEL,
        input=texts,
    )

    return [embedding.embedding for embedding in response.data]