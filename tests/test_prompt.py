from devassistant.prompt import build_prompt


def test_build_prompt():
    context = "RAG retrieves relevant document chunks."
    question = "What does RAG retrieve?"

    prompt = build_prompt(
        context,
        question,
    )

    assert prompt == (
        "Context:\n"
        "RAG retrieves relevant document chunks.\n"
        "Question:\n"
        "What does RAG retrieve?"
    )