# DevAssistant

A local AI development assistant built around **Python, LM Studio, embeddings, semantic similarity, document chunking, and RAG**.

The goal of this project is to build a lightweight and modular assistant capable of retrieving relevant information from a collection of documents and using a local LLM to generate an answer based on that context.

## Features

* Local LLM inference through **LM Studio**
* Text embeddings using a local embedding model
* Cosine similarity computation
* Semantic document search
* Top-k document retrieval
* Markdown document loading
* Fixed-size document chunking with configurable overlap
* Retrieval-Augmented Generation (RAG)
* Unit tests with mocked external dependencies
* Integration tests with LM Studio

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
│       ├── rag.py
│       ├── document_loader.py
│       └── chunking.py
├── tests/
│   ├── test_embeddings.py
│   ├── test_lmstudio.py
│   ├── test_similarity.py
│   ├── test_search.py
│   ├── test_rag.py
│   ├── test_rag_integration.py
│   ├── test_document_loader.py
│   └── test_chunking.py
├── pyproject.toml
└── README.md
```

## Architecture

The current pipeline is structured as follows:

```text
Documents
    │
    ▼
Markdown Loader
    │
    ▼
Document Chunking
    │
    ▼
Embeddings
    │
    ▼
Semantic Search
    │
    ▼
Top-k Relevant Chunks
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

### Document Loading

`document_loader.py` loads Markdown files from a directory.

Non-Markdown files are ignored.

Documents are automatically split into smaller chunks before being passed to the embedding and search pipeline.

### Document Chunking

`chunking.py` splits documents into fixed-size word chunks with configurable overlap.

The default configuration is:

```text
Chunk size:
60 words

Overlap:
12 words
```

For example, with a chunk size of 4 words and an overlap of 1 word:

```text
Chunk 1:
one two three four

Chunk 2:
four five six
```

The overlap helps preserve contextual information between neighboring chunks.

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

`search.py` embeds the document chunks and the user's question, then ranks the chunks according to their cosine similarity with the question.

The search function supports a `top_k` parameter to limit the number of retrieved chunks.

### RAG

`rag.py` combines document loading, chunking, semantic search, and local LLM generation.

The retrieved chunks are converted into a context and passed to the LLM together with the original question.

The current pipeline is:

```text
Question
   │
   ▼
Document Loading
   │
   ▼
Document Chunking
   │
   ▼
Semantic Search
   │
   ▼
Relevant Chunks
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

The chunking configuration can be customized when calling `get_answer()`:

```python
from devassistant.rag import get_answer

answer = get_answer(
    directory="documents",
    question="What is RAG?",
    chunk_size=60,
    overlap=12,
)
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

## Usage Example

Create a directory containing Markdown documents:

```text
documents/
├── python.md
├── rag.md
└── cpp.md
```

Then use the RAG pipeline directly from Python:

```python
from devassistant.rag import get_answer

answer = get_answer(
    directory="documents",
    question="What is RAG?",
)

print(answer)
```

The pipeline performs the following steps:

1. Load Markdown documents from the directory.
2. Split the documents into overlapping chunks.
3. Generate embeddings for the chunks.
4. Generate an embedding for the question.
5. Compute cosine similarity between the question and each chunk.
6. Retrieve the most relevant chunks.
7. Build a context from the retrieved chunks.
8. Send the context and question to the local LLM through LM Studio.
9. Return the generated answer.

The chunking parameters can also be customized:

```python
answer = get_answer(
    directory="documents",
    question="What is RAG?",
    chunk_size=100,
    overlap=20,
)

print(answer)
```

## Running the Tests

Run the complete test suite with:

```bash
pytest
```

The test suite covers:

* Embedding generation
* Embedding dimensions and types
* LM Studio integration
* Cosine similarity
* Semantic search
* Top-k retrieval
* Markdown document loading
* Empty document handling
* Document chunking
* Chunk overlap
* RAG context construction
* Chunk-based RAG retrieval
* Empty document handling in the RAG pipeline
* RAG integration with LM Studio

All tests currently pass.

## Development

The project is developed incrementally, with each component tested independently before being integrated into the RAG pipeline.

The current development stages are:

1. LM Studio client
2. Embedding generation
3. Cosine similarity
4. Semantic search
5. RAG context construction
6. Markdown document loading
7. Document chunking
8. Chunk-based RAG integration
9. Local LLM generation

Future work will focus on improving document ingestion, retrieval quality, prompt construction, and the overall RAG pipeline.

## License

This project is currently intended as a personal learning and development project.
