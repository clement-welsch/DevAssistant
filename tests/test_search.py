import pytest

from devassistant.search import search, aggregate_document_scores


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

def test_search_filters_results_below_score_threshold(monkeypatch):
    documents = [
        {
            "content": "Relevant document",
            "source": "relevant.md",
        },
        {
            "content": "Very relevant document",
            "source": "very_relevant.md",
        },
        {
            "content": "Irrelevant document",
            "source": "irrelevant.md",
        },
    ]

    def fake_embed(texts):
        if texts == ["What is relevant?"]:
            return [[1.0, 0.0]]

        return [
            [1.0, 0.0],
            [0.9, 0.0],
            [0.4, 0.0],
        ]

    def fake_similarity(a, b):
        return a[0]

    monkeypatch.setattr(
        "devassistant.search.embed",
        fake_embed,
    )

    monkeypatch.setattr(
        "devassistant.search.cosine_similarity",
        fake_similarity,
    )

    results = search(
        documents,
        question="What is relevant?",
        top_k=3,
        score_threshold=0.7,
    )

    assert [score for score, _ in results] == [1.0, 0.9]

def test_aggregate_document_scores_uses_max_chunk_score():
    results = [
        (
            0.6,
            {
                "content": "First RAG chunk.",
                "source": "rag.md",
            },
        ),
        (
            0.9,
            {
                "content": "Second RAG chunk.",
                "source": "rag.md",
            },
        ),
        (
            0.8,
            {
                "content": "Python chunk.",
                "source": "python.md",
            },
        ),
    ]

    scores = aggregate_document_scores(results)

    assert scores == [
        (0.9, "rag.md"),
        (0.8, "python.md"),
    ]

def test_search_top_k_limits_documents(monkeypatch):
    documents = [
        {
            "content": "RAG chunk one.",
            "source": "rag.md",
        },
        {
            "content": "RAG chunk two.",
            "source": "rag.md",
        },
        {
            "content": "Python chunk.",
            "source": "python.md",
        },
        {
            "content": "C++ chunk.",
            "source": "cpp.md",
        },
    ]

    def fake_embed(texts):
        if len(texts) == 1:
            return [[1.0, 0.0]]

        return [
            [0.9, 0.0],
            [0.8, 0.0],
            [0.7, 0.0],
            [0.6, 0.0],
        ]

    monkeypatch.setattr(
        "devassistant.search.embed",
        fake_embed,
    )

    results = search(
        documents,
        "What is relevant?",
        top_k=2,
    )

    sources = {
        document["source"]
        for _, document in results
    }

    assert sources == {
        "rag.md",
        "python.md",
    }

    assert len(results) == 3