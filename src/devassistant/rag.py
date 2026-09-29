from devassistant.document_loader import load_documents
from devassistant.search import search
from devassistant.lmstudio_client import ask

def get_answer(directory, question):
    documents = load_documents(directory)
    best_docs = search(documents, question)
    contexts = []

    for document in best_docs:
        contexts.append(document[1])

    context = "\n".join(contexts)
    prompt = f"Context:\n{context}\nQuestion:\n{question}"

    response = ask(prompt)

    return response