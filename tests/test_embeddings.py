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

def fake_create(model, input):
    # Simule la réponse renvoyée par LM Studio
    return SimpleNamespace(
        data=[
            SimpleNamespace(embedding=[0.1, 0.2, 0.3]),
            SimpleNamespace(embedding=[0.4, 0.5, 0.6]),
            SimpleNamespace(embedding=[0.7, 0.8, 0.9]),
        ]
    )

def test_embedding_count_without_lmstudio(monkeypatch):
    monkeypatch.setattr(
        "devassistant.embeddings.client.embeddings.create",
        fake_create,
    )

    vectors = embed(texts)

    assert len(vectors) == len(texts)

    