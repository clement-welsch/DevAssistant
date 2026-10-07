from devassistant.document_loader import load_documents
from devassistant.search import search
from devassistant.lmstudio_client import ask
from devassistant.prompt import build_prompt

def build_context(documents):
    contexts = []

    for document in documents:
        source = document[1]["source"]

        contexts.append(
            f"Source: {source}\n"
            f"{document[1]['content']}"
        )

    return "\n".join(contexts)


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

    sources = []

    for document in best_docs:
        source = document[1]["source"]

        if source not in sources:
            sources.append(source)

    context = build_context(best_docs)

    prompt = build_prompt(
        context,
        question,
    )

    response = ask(prompt)

    return {
        "answer": response,
        "sources": sources,
    }