import pytest

from devassistant.search import search

@pytest.fixture
def documents():
    return [
        "Document peu pertinent",
        "Document très pertinent",
        "Document moyennement pertinent",
    ]

@pytest.fixture
def fake_embed(documents):
    # This fixture prepares a fake version of embed().
    # We define an inner function because pytest needs to provide
    # a function that monkeypatch can use to replace the real embed().
    def _fake_embed(texts):
        # search() calls embed() first with the documents.
        # We return one vector for each document.
        if texts == documents:
            return [
                [0, 1],
                [1, 0],
                [0.7, 0.7],
            ]

        # search() calls embed() a second time with the question.
        # We return the vector corresponding to the question.
        return [[1, 0]]

    # The fixture returns the inner function.
    # This is the function that the test will give to monkeypatch.
    return _fake_embed

def test_search(monkeypatch, documents, fake_embed):
    # search.py uses its own reference to embed().
    # We temporarily replace it with our fake function.
    monkeypatch.setattr(
        "devassistant.search.embed",
        fake_embed,
    )

    # We test search() itself, not fake_embed().
    answer = search(documents, "Ma question")

    # The second document has the same vector as the question,
    # so its cosine similarity is 1.0.
    assert answer[0] == (1.0, "Document très pertinent")
    assert len(answer) == 3

    answer = search(documents, "Ma question", top_k=2)
    assert len(answer) == 2
    assert answer[0] == (1.0, "Document très pertinent")

    answer = search(documents, "Ma question", top_k=1)
    assert len(answer) == 1
    assert answer[0] == (1.0, "Document très pertinent")

    answer = search(documents, "Ma question", top_k=10)
    assert len(answer) == 3
    assert answer[0] == (1.0, "Document très pertinent")

def test_search_empty_documents(monkeypatch, fake_embed):
    monkeypatch.setattr(
        "devassistant.search.embed",
        fake_embed,
    )

    answer = search([], "Ma question")

    assert answer == []