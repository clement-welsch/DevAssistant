# DevAssistant

A local AI development assistant built around **Python, LM Studio, embeddings, semantic similarity, and RAG**.

The goal of this project is to build a lightweight and modular assistant capable of retrieving relevant information from a collection of documents and using a local LLM to generate an answer based on that context.

## Features

* Local LLM inference through **LM Studio**
* Text embeddings using a local embedding model
* Cosine similarity computation
* Semantic document search
* Top-k document retrieval
* Retrieval-Augmented Generation (RAG)
* Unit tests with mocked external dependencies

## Project Structure

```text
DevAssistant/
├── src/
│   └── devassistant/
│       ├── __init__.py
│       ├── config.py
│       ├── embeddings.py
│       ├── lmstudio_client.py
│       ├── similarity.py
│       ├── search.py
│       └── rag.py
├── tests/
│   ├── test_embeddings.py
│   ├── test_lmstudio.py
│   ├── test_similarity.py
│   ├── test_search.py
│   └── test_rag.py
├── pyproject.toml
└── README.md
```

## Architecture

The current pipeline is structured as follows:

```text
Documents
    │
    ▼
Embeddings
    │
    ▼
Semantic Search
    │
    ▼
Top-k Relevant Documents
    │
    ▼
Context Construction
    │
    ▼
Local LLM
    │
    ▼
Generated Answer
```

### Embeddings

`embeddings.py` uses the OpenAI-compatible API provided by LM Studio to generate vector representations of text.

The current embedding model is:

```text
text-embedding-nomic-embed-text-v1.5
```

The generated embeddings have a dimension of **768**.

### Similarity

`similarity.py` provides cosine similarity between two vectors.

Cosine similarity is used to measure how semantically close two embeddings are.

### Search

`search.py` embeds the documents and the user's question, then ranks the documents according to their cosine similarity with the question.

The search function supports a `top_k` parameter to limit the number of retrieved documents.

### RAG

`rag.py` combines semantic search with the local LLM.

The retrieved documents are converted into a context and passed to the LLM together with the original question.

The current pipeline is:

```text
Question
   │
   ▼
Semantic Search
   │
   ▼
Relevant Documents
   │
   ▼
Context + Question
   │
   ▼
LM Studio
   │
   ▼
Answer
```

## Requirements

* Python **3.12+**
* LM Studio
* A compatible local chat model
* A compatible local embedding model

The project currently uses:

```text
Chat model:
gemma-4-e4b

Embedding model:
text-embedding-nomic-embed-text-v1.5
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the project in editable mode:

```bash
pip install -e .
```

Install the required development dependencies:

```bash
pip install pytest numpy openai
```

## LM Studio Configuration

Start LM Studio and make sure the required models are available.

The project expects the LM Studio OpenAI-compatible API to be available at:

```text
http://localhost:1234/v1
```

The configuration is defined in:

```text
src/devassistant/config.py
```

Current configuration:

```python
LMSTUDIO_EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LMSTUDIO_API_KEY = "lm-studio"
LMSTUDIO_MODEL = "gemma-4-e4b"
```

## Running the Tests

Run the complete test suite with:

```bash
pytest
```

The current test suite covers:

* Embedding generation
* Embedding dimensions and types
* LM Studio integration
* Cosine similarity
* Semantic search
* Top-k retrieval
* RAG context construction
* Empty document handling

Current status:

```text
21 passed
```

## Development

The project is developed incrementally, with each component tested independently before being integrated into the RAG pipeline.

The current development stages are:

1. LM Studio client
2. Embedding generation
3. Cosine similarity
4. Semantic search
5. RAG context construction
6. Local LLM generation

Future work will focus on improving document ingestion, retrieval quality, prompt construction, and the overall RAG pipeline.

## Usage Example

The RAG pipeline can be used directly from Python:

```python
from devassistant.rag import get_answer

documents = [
    "Python is a high-level programming language.",
    "C++ is a compiled programming language commonly used for game development.",
    "RAG combines document retrieval with language model generation.",
]

question = "What is RAG?"

answer = get_answer(
    documents=documents,
    question=question,
)

print(answer)
```

The pipeline performs the following steps:

1. Generate embeddings for the documents.
2. Generate an embedding for the question.
3. Compute the cosine similarity between the question and each document.
4. Retrieve the most relevant documents.
5. Build a context from the retrieved documents.
6. Send the context and question to the local LLM through LM Studio.
7. Return the generated answer.

For the example above, the retrieved context should contain the document describing RAG, and the local LLM can use that context to generate the answer.


## License

This project is currently intended as a personal learning and development project.
