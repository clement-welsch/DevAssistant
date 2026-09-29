import pytest

from devassistant.rag import get_answer


@pytest.fixture
def documents(tmp_path):
    python_file = tmp_path / "python.md"
    python_file.write_text(
        "Python is a high-level programming language."
    )

    rag_file = tmp_path / "rag.md"
    rag_file.write_text(
        "RAG combines document retrieval with language model generation."
    )

    return tmp_path


@pytest.fixture
def fake_search():
    def _fake_search(documents, question, top_k=3):
        return [
            (1.0, "RAG combines document retrieval with language model generation."),
            (0.7, "Python is a high-level programming language."),
        ]

    return _fake_search


@pytest.fixture
def fake_ask():
    captured = {}

    def _fake_ask(prompt):
        captured["prompt"] = prompt
        return "Here is the generated answer."

    return _fake_ask, captured


def test_get_answer(monkeypatch, documents, fake_ask):
    captured = {}

    def fake_search(documents, question, top_k=3):
        return [
            (
                1.0,
                {
                    "content": (
                        "RAG combines document retrieval "
                        "with language model generation."
                    ),
                    "source": "rag.md",
                },
            ),
            (
                0.7,
                {
                    "content": (
                        "Python is a high-level "
                        "programming language."
                    ),
                    "source": "python.md",
                },
            ),
        ]

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
        directory=documents,
        question="What is RAG?",
    )

    assert answer == "Here is the generated answer."

    assert captured["prompt"] == (
        "Context:\n"
        "RAG combines document retrieval with language model generation.\n"
        "Python is a high-level programming language.\n"
        "Question:\n"
        "What is RAG?"
    )


def test_get_answer_empty_directory(monkeypatch, tmp_path, fake_ask):
    ask, captured = fake_ask

    monkeypatch.setattr(
        "devassistant.rag.search",
        lambda documents, question, top_k=3: [],
    )

    monkeypatch.setattr(
        "devassistant.rag.ask",
        ask,
    )

    answer = get_answer(
        directory=tmp_path,
        question="What is RAG?",
    )

    assert answer == "Here is the generated answer."

    assert captured["prompt"] == (
        "Context:\n\n"
        "Question:\n"
        "What is RAG?"
    )


def test_get_answer_with_chunks(monkeypatch, tmp_path):
    document = tmp_path / "document.md"
    document.write_text(
        "Python is a programming language. "
        "RAG retrieves relevant document chunks. "
        "C++ is commonly used for game development."
    )

    captured = {}

    def fake_search(documents, question, top_k=3):
        captured["documents"] = documents
        return [
            (1.0, documents[1]),
        ]

    def fake_ask(prompt):
        captured["prompt"] = prompt
        return "RAG retrieves relevant information."

    monkeypatch.setattr(
        "devassistant.rag.search",
        fake_search,
    )

    monkeypatch.setattr(
        "devassistant.rag.ask",
        fake_ask,
    )

    answer = get_answer(
        directory=tmp_path,
        question="What does RAG retrieve?",
        chunk_size=10,
        overlap=2,
    )

    assert answer == "RAG retrieves relevant information."

    assert len(captured["documents"]) > 1

    assert captured["prompt"] == (
    "Context:\n"
    f"{captured['documents'][1]['content']}\n"
    "Question:\n"
    "What does RAG retrieve?"
)


def test_get_answer_with_top_k(monkeypatch, tmp_path):
    document = tmp_path / "document.md"
    document.write_text(
        "Python is a programming language. "
        "RAG retrieves relevant document chunks. "
        "C++ is commonly used for game development."
    )

    captured = {}

    def fake_search(documents, question, top_k=3):
        captured["top_k"] = top_k
        return []

    def fake_ask(prompt):
        return "Answer"

    monkeypatch.setattr(
        "devassistant.rag.search",
        fake_search,
    )

    monkeypatch.setattr(
        "devassistant.rag.ask",
        fake_ask,
    )

    answer = get_answer(
        directory=tmp_path,
        question="What does RAG retrieve?",
        chunk_size=10,
        overlap=2,
        top_k=5,
    )

    assert answer == "Answer"
    assert captured["top_k"] == 5