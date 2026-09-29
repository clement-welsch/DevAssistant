import pytest

from devassistant.search import search


def test_search(monkeypatch):
    documents = [
        {
            "content": "Python is a programming language.",
            "source": "python.md",
        },
        {
            "content": "RAG retrieves relevant information.",
            "source": "rag.md",
        },
    ]

    def fake_embed(texts):
        if texts == [
            "Python is a programming language.",
            "RAG retrieves relevant information.",
        ]:
            return [
                [0, 1],
                [1, 0],
            ]

        return [[1, 0]]

    monkeypatch.setattr(
        "devassistant.search.embed",
        fake_embed,
    )

    results = search(
        documents,
        "What is RAG?",
    )

    assert results[0] == (
        1.0,
        {
            "content": "RAG retrieves relevant information.",
            "source": "rag.md",
        },
    )


def test_search_top_k(monkeypatch):
    documents = [
        {
            "content": "Python is a programming language.",
            "source": "python.md",
        },
        {
            "content": "RAG retrieves relevant information.",
            "source": "rag.md",
        },
        {
            "content": "C++ is used for game development.",
            "source": "cpp.md",
        },
    ]

    def fake_embed(texts):
        if texts == [
            "Python is a programming language.",
            "RAG retrieves relevant information.",
            "C++ is used for game development.",
        ]:
            return [
                [0, 1],
                [1, 0],
                [0, 0.5],
            ]

        return [[1, 0]]

    monkeypatch.setattr(
        "devassistant.search.embed",
        fake_embed,
    )

    results = search(
        documents,
        "What is RAG?",
        top_k=2,
    )

    assert len(results) == 2
    assert results[0][1]["source"] == "rag.md"


def test_search_keeps_document_metadata(monkeypatch):
    documents = [
        {
            "content": "Python is a programming language.",
            "source": "python.md",
        },
        {
            "content": "RAG retrieves relevant information.",
            "source": "rag.md",
        },
    ]

    def fake_embed(texts):
        if texts == [
            "Python is a programming language.",
            "RAG retrieves relevant information.",
        ]:
            return [
                [0, 1],
                [1, 0],
            ]

        return [[1, 0]]

    monkeypatch.setattr(
        "devassistant.search.embed",
        fake_embed,
    )

    results = search(
        documents,
        "What is RAG?",
    )

    assert results[0][1] == {
        "content": "RAG retrieves relevant information.",
        "source": "rag.md",
    }