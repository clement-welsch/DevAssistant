def build_prompt(context, question):
    prompt = (
        "Context:\n"
        f"{context}\n"
        "Question:\n"
        f"{question}"
    )

    return prompt