from pathlib import Path

def load_documents(directory):
    content = []
    for file in Path(directory).glob("*.md"):
        content.append(file.read_text())
    return content
