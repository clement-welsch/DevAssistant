from devassistant.document_loader import load_documents
from devassistant.search import search
from devassistant.lmstudio_client import ask


def get_answer(directory, question, chunk_size=60, overlap=12, top_k=3):
    documents = load_documents(
        directory,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    best_docs = search(
        documents,
        question,
        top_k=top_k,
    )

    contexts = []

    for document in best_docs:
        contexts.append(document[1])

    context = "\n".join(contexts)
    prompt = f"Context:\n{context}\nQuestion:\n{question}"

    response = ask(prompt)

    return response