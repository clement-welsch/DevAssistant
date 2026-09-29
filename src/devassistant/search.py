from devassistant.embeddings import embed
from devassistant.similarity import cosine_similarity

def search(documents, question, top_k=3):
    vectors_docs = embed(documents)
    vectors_question = embed([question])

    question_vector = vectors_question[0]

    array_cos = []

    for vector, doc in zip(vectors_docs, documents):
        array_cos.append((cosine_similarity(vector, question_vector), doc))

    array_cos.sort(reverse=True)

    return array_cos[:top_k]