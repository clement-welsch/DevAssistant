from devassistant.embeddings import embed
from devassistant.similarity import cosine_similarity


def search(documents, question, top_k=3):
    contents = [document["content"] for document in documents]

    vectors_docs = embed(contents)
    vectors_question = embed([question])

    question_vector = vectors_question[0]

    array_cos = []

    for vector, document in zip(vectors_docs, documents):
        array_cos.append(
            (
                cosine_similarity(vector, question_vector),
                document,
            )
        )

    array_cos.sort(key=lambda item: item[0], reverse=True)

    return array_cos[:top_k]