import pytest

from devassistant.rag import get_answer


@pytest.fixture
def documents():
    return [
        "Document peu pertinent",
        "Document très pertinent",
        "Document moyennement pertinent",
    ]


@pytest.fixture
def fake_search():
    def _fake_search(documents, question):
        return [
            (1.0, "Document très pertinent"),
            (0.7, "Document moyennement pertinent"),
        ]

    return _fake_search


@pytest.fixture
def fake_ask():
    captured = {}

    def _fake_ask(prompt):
        captured["prompt"] = prompt
        return "Voici la réponse générée."

    return _fake_ask, captured


def test_get_answer(monkeypatch, documents, fake_search, fake_ask):
    ask, captured = fake_ask

    monkeypatch.setattr(
        "devassistant.rag.search",
        fake_search,
    )

    monkeypatch.setattr(
        "devassistant.rag.ask",
        ask,
    )

    answer = get_answer(
        documents=documents,
        question="Ma question",
    )

    assert answer == "Voici la réponse générée."

    assert captured["prompt"] == (
        "Context:\n"
        "Document très pertinent\n"
        "Document moyennement pertinent\n"
        "Question:\n"
        "Ma question"
    )

def test_get_answer_empty_documents(monkeypatch, fake_ask):
    ask, captured = fake_ask

    monkeypatch.setattr(
        "devassistant.rag.search",
        lambda documents, question: [],
    )

    monkeypatch.setattr(
        "devassistant.rag.ask",
        ask,
    )

    answer = get_answer(
        documents=[],
        question="Ma question",
    )

    assert answer == "Voici la réponse générée."

    assert "Context:" in captured["prompt"]
    assert "Question:" in captured["prompt"]
    assert "Ma question" in captured["prompt"]

    assert captured["prompt"] == "Context:\n\nQuestion:\nMa question"