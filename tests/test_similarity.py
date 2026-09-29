import numpy as np
from openai import OpenAI

from devassistant.config import LMSTUDIO_API_KEY, LMSTUDIO_BASE_URL


client = OpenAI(
    base_url=LMSTUDIO_BASE_URL,
    api_key=LMSTUDIO_API_KEY,
)


documents = [
    "Le Nutri-Score évalue la qualité nutritionnelle des aliments.",
    "Le produit contient beaucoup de protéines.",
    "Les pommes sont des fruits.",
]

question = "Comment évaluer la qualité nutritionnelle d'un aliment ?"


# Génération des embeddings
response = client.embeddings.create(
    model="text-embedding-nomic-embed-text-v1.5",
    input=documents + [question],
)


vectors = [np.array(item.embedding) for item in response.data]

document_vectors = vectors[:-1]
question_vector = vectors[-1]


# Similarité cosinus
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


results = []

for document, vector in zip(documents, document_vectors):
    similarity = cosine_similarity(question_vector, vector)
    results.append((similarity, document))


# Classement du plus pertinent au moins pertinent
results.sort(reverse=True)


for similarity, document in results:
    print(f"{similarity:.4f} | {document}")