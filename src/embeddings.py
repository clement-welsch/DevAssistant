from openai import OpenAI

from config import LMSTUDIO_API_KEY, LMSTUDIO_BASE_URL, LMSTUDIO_EMBEDDING_MODEL


client = OpenAI(
    base_url=LMSTUDIO_BASE_URL,
    api_key=LMSTUDIO_API_KEY,
)


texts = [
    "Le Nutri-Score évalue la qualité nutritionnelle des aliments.",
    "Le produit contient beaucoup de protéines.",
    "Les pommes sont des fruits."
]

def embed(model, texts):
    response = client.embeddings.create(
        model=LMSTUDIO_EMBEDDING_MODEL,
        input=texts,
    )

    return [embedding.embedding for embedding in response.data]


for i, embedding in enumerate(response.data):
    vector = embedding.embedding

    print(f"Texte {i + 1}")
    print(f"Nombre de dimensions : {len(vector)}")
    print(f"Premières valeurs : {vector[:5]}")
    print()


def embed(texts: list[str]) -> ...:
