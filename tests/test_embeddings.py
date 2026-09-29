from devassistant.embeddings import embed
import pytest


texts = [
    "Le Nutri-Score évalue la qualité nutritionnelle des aliments.",
    "Le produit contient beaucoup de protéines.",
    "Les pommes sont des fruits.",
]

def test_embedding_count():
    vectors = embed(texts)
    assert len(vectors) == len(texts)

def test_embedding_dimension():
    vectors = embed(texts)

    for vector in vectors:
        assert len(vector) == 768

def test_embedding_type():
    vectors = embed(texts)
    
    for vector in vectors:
        assert isinstance(vector, list)

def test_embedding_values():
    vectors = embed(texts)
    for vector in vectors:
        for value in vector:
            assert isinstance(value, float)

def test_embedding_empty_input():
    with pytest.raises(ValueError):
        embed([])

def test_embedding_single_text():
    vectors = embed(["Le Nutri-Score évalue la qualité nutritionnelle."])

    assert len(vectors) == 1

###

from types import SimpleNamespace

@pytest.fixture
def mock_lmstudio(monkeypatch):
    monkeypatch.setattr(
        "devassistant.embeddings.client.embeddings.create",
        fake_create,
    )

def fake_create(model, input):
    if not input:
        raise ValueError("No embedding data received")

    return SimpleNamespace(
        data=[
            SimpleNamespace(embedding=[0.1] * 768)
            for _ in input
        ]
    )

def test_embedding_count_without_lmstudio(monkeypatch):
    vectors = embed(texts)
    assert len(vectors) == len(texts)

def test_embedding_dimension_without_lmstudio(monkeypatch):
    vectors = embed(texts)

    for vector in vectors:
        assert len(vector) == 768

def test_embedding_type_without_lmstudio(monkeypatch):
    vectors = embed(texts)
    for vector in vectors:
        assert isinstance(vector, list)

def test_embedding_values_without_lmstudio(monkeypatch):
    vectors = embed(texts)
    for vector in vectors:
        for value in vector:
            assert isinstance(value, float)

def test_embedding_empty_input_without_lmstudio(monkeypatch):
    with pytest.raises(ValueError):
        embed([])

def test_embedding_single_text_without_lmstudio(monkeypatch):
    vectors = embed(["Le Nutri-Score évalue la qualité nutritionnelle."])
    assert len(vectors) == 1