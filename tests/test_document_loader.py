from devassistant.document_loader import load_documents


def test_load_documents(tmp_path):
    python_file = tmp_path / "python.md"
    python_file.write_text("Python content")

    rag_file = tmp_path / "rag.md"
    rag_file.write_text("RAG content")

    documents = load_documents(tmp_path)

    assert documents == [
        "Python content",
        "RAG content",
    ]


def test_load_documents_empty_directory(tmp_path):
    documents = load_documents(tmp_path)

    assert documents == []


def test_load_documents_ignores_non_markdown_files(tmp_path):
    markdown_file = tmp_path / "python.md"
    markdown_file.write_text("Python content")

    text_file = tmp_path / "notes.txt"
    text_file.write_text("This file should be ignored")

    documents = load_documents(tmp_path)

    assert documents == ["Python content"]


def test_load_documents_empty_markdown_file(tmp_path):
    empty_file = tmp_path / "empty.md"
    empty_file.write_text("")

    documents = load_documents(tmp_path)

    assert documents == []


def test_load_documents_with_chunking(tmp_path):
    document = tmp_path / "document.md"
    document.write_text(
        "one two three four five six"
    )

    documents = load_documents(
        tmp_path,
        chunk_size=4,
        overlap=1,
    )

    assert documents == [
        "one two three four",
        "four five six",
    ]


def test_load_documents_default_chunking(tmp_path):
    document = tmp_path / "document.md"
    document.write_text(
        "one two three"
    )

    documents = load_documents(tmp_path)

    assert documents == [
        "one two three",
    ]