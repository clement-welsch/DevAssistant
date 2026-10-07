from devassistant.embeddings import embed
from devassistant.similarity import cosine_similarity


def search(
    documents,
    question,
    top_k=3,
    score_threshold=0.0,
):
    contents = [document["content"] for document in documents]

    vectors_docs = embed(contents)
    vectors_question = embed([question])

    question_vector = vectors_question[0]

    scored_chunks = []

    for vector, document in zip(vectors_docs, documents):
        score = cosine_similarity(vector, question_vector)

        if score >= score_threshold:
            scored_chunks.append(
                (
                    score,
                    document,
                )
            )

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    document_scores = aggregate_document_scores(
        scored_chunks
    )

    selected_sources = {
        source
        for _, source in document_scores[:top_k]
    }

    return [
        item
        for item in scored_chunks
        if item[1]["source"] in selected_sources
    ]

def aggregate_document_scores(results):
    document_scores = {}

    for score, document in results:
        source = document["source"]

        if source not in document_scores:
            document_scores[source] = score
        else:
            document_scores[source] = max(
                document_scores[source],
                score,
            )

    return sorted(
        [
            (score, source)
            for source, score in document_scores.items()
        ],
        reverse=True,
    )