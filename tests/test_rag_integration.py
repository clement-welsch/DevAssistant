from devassistant.rag import get_answer


def test_rag_integration():
    documents = [
        "Python is a high-level programming language.",
        "C++ is a compiled programming language commonly used for game development.",
        "RAG combines document retrieval with language model generation.",
    ]

    question = "What is RAG?"

    answer = get_answer(
        documents=documents,
        question=question,
    )

    assert isinstance(answer, str)
    assert answer