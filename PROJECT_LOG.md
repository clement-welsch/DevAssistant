# Recall — Project Log

This document records the development history of Recall, including implementation milestones, architectural decisions, validation results, and known limitations.

Unlike the README, which describes the current state of the project, this log preserves the progression of the implementation over time.

Dates and commit references are taken from the Git history where available. Validation results are recorded only when they have been observed.

---

## Project Overview

**Project name:** Recall
**Repository:** https://github.com/clement-welsch/Recall
**Python package:** `devassistant`
**Initial development:** September 24, 2026
**Current documented state:** October 9, 2026

Recall is a local AI-powered knowledge retrieval assistant for developers. It combines semantic search with Retrieval-Augmented Generation (RAG) to retrieve relevant passages from Markdown documentation and generate answers using a locally hosted language model.

The project uses LM Studio's OpenAI-compatible API for both text embeddings and language generation.

### Current technology stack

* Python 3.12+
* LM Studio
* Gemma 4 E4B for text generation
* Nomic Embed Text v1.5 for embeddings
* OpenAI Python client for API communication
* NumPy for numerical operations
* pytest for automated testing

---

## September 24, 2026 — Initial Repository Setup

**Objective:** Establish the initial project repository.

### Implementation

* Created the Git repository.
* Started the initial Python project structure.
* Added the first Python package initialization files.

### Milestones

* `05252e1` — Initial commit.
* `4771d54` — Python initialization.

### Outcome

The repository was initialized and ready for the first implementation work.

---

## September 28, 2026 — Python Package and Embeddings

**Objective:** Establish a reusable Python package and implement communication with the local embedding model.

### Implementation

* Reworked the initial project structure.
* Started and completed the embedding feature.
* Introduced the `devassistant` package structure.
* Configured the package so that it could be installed and imported by the test suite.
* Updated the README to reflect the implementation.

### Testing

* Introduced pytest-based tests.
* Tested embedding and language-model communication.
* Investigated behavior when LM Studio was disconnected.

### Milestones

* `eaa7e69` — Project rework.
* `ff2dd77` — Started embedding implementation.
* `eedc15f` — Completed embedding feature.
* `95f724a` — Created an initial pytest test.
* `5ee7f5c` — Made the package visible to pytest.
* `a1259f0` — Added pytest.
* `1ae3ec3` — Merged pull request #2 for the embedding feature.

### Outcome

The project gained its first reusable AI integration component and an initial automated testing setup.

---

## September 29, 2026 — Embedding Tests and Similarity Search

**Objective:** Build the retrieval foundation required for a RAG pipeline.

### Implementation

* Corrected embedding and language-model tests.
* Added tests that could run without a live language-model connection.
* Implemented cosine-similarity-based document comparison.
* Ranked documents according to their similarity to a question.
* Added support for retrieving a configurable number of results through `top_k`.

### Testing

Tests were developed around the individual components rather than relying exclusively on live model calls.

This made it possible to validate parts of the retrieval logic independently of LM Studio.

### Milestones

* `2ca0ed2` — Created tests that do not require LM Studio.
* `9273d7b` — Corrected embedding and language-model tests.
* `74b112c` — Added initial similarity tests.
* `e72192b` — Tested similarity search.
* `d94e075` — Returned the three most similar documents.
* `1cdf8d8` — Introduced the `top_k` parameter.
* `6fad598` — Merged pull request #3 for similarity search.

### Outcome

Recall could compare document embeddings with a question embedding, rank the results, and return the most relevant candidates.

---

## September 29, 2026 — Initial RAG Pipeline

**Objective:** Combine document retrieval with language-model generation.

### Implementation

* Introduced the initial RAG pipeline.
* Integrated semantic retrieval with response generation.
* Added tests for the RAG components.
* Separated prompt construction into a dedicated module.
* Preserved document metadata during retrieval.
* Integrated document loading into the RAG workflow.

### Architectural progression

The initial pipeline evolved toward the following structure:

1. Load documents.
2. Generate document embeddings.
3. Embed the user's question.
4. Rank documents by cosine similarity.
5. Select the most relevant results.
6. Construct a prompt from the retrieved information and the question.
7. Send the prompt to the language model.
8. Return the generated answer.

### Milestones

* `3d81a4c` — Added RAG and RAG tests.
* `79544f6` — Merged pull request #4 for RAG integration.
* `81c9936` — Integrated document loading into the RAG workflow.
* `27131fd` — Merged pull request #5 for document loading.
* `44abc64` — Extracted RAG prompt construction.
* `2bd708c` — Merged pull request #9 for prompt construction.
* `70e5605` — Preserved document metadata during retrieval.
* `6a20ddb` — Merged pull request #10 for document metadata.

### Outcome

Recall moved from isolated embedding and similarity components to an integrated retrieval-and-generation pipeline.

---

## September 29, 2026 — Markdown Chunking

**Objective:** Support documents that are too long to retrieve and process effectively as single units.

### Implementation

* Added document chunking.
* Updated the document loader to return chunks rather than whole Markdown files.
* Integrated chunking into the RAG pipeline.
* Updated the README to document chunking behavior.

### Current chunking strategy

Recall uses fixed-size word windows with overlapping content between consecutive chunks.

The current defaults are:

* Chunk size: 60 words.
* Overlap: 12 words.

The overlap preserves some context across chunk boundaries.

### Milestones

* `fab7998` — Split Markdown files into chunks.
* `a86e265` — Updated `load_documents()` to use chunks.
* `1c0a8fa` — Merged pull request #6 for document chunking.
* `70e7e17` — Integrated chunking into RAG.
* `1321d6c` — Merged pull request #7 for RAG chunk integration.

### Outcome

The retrieval pipeline could operate on smaller document passages instead of treating every Markdown file as a single retrieval unit.

---

## September 29, 2026 — Configurable Retrieval and Prompt Refactoring

**Objective:** Make retrieval behavior configurable and improve separation of responsibilities.

### Implementation

* Added configurable retrieval parameters.
* Introduced `top_k` as a RAG configuration option.
* Extracted prompt construction into a dedicated module.
* Preserved document metadata through retrieval.

### Milestones

* `bd7082f` — Made RAG retrieval configurable.
* `58b34ad` — Merged pull request #8 for configurable `top_k`.
* `44abc64` — Extracted prompt construction.

### Outcome

Retrieval behavior became configurable without requiring changes to the internal search implementation.

Prompt construction also became a separate responsibility, making it easier to test and evolve independently.

---

## October 7, 2026 — Source Tracking and Context Construction

**Objective:** Make the origin of retrieved information visible in RAG results.

### Implementation

* Included document source information in the RAG context.
* Exposed source filenames in the final RAG result.
* Removed duplicate source filenames from the returned source list.
* Extracted context construction into a dedicated function.

### Current result structure

The `get_answer()` function returns a dictionary containing:

* `answer`: the generated response.
* `sources`: a list of unique source filenames associated with the retrieved passages.

The source list provides traceability to the files used to construct the context. It does not independently guarantee that every statement in the generated answer is supported by those files.

### Milestones

* `faf9503` — Included document sources in RAG context.
* `eebdcc6` — Merged pull request #11 for source-aware context.
* `4b6ac48` — Exposed RAG sources in the answer.
* `62e8635` — Merged pull request #12 for RAG sources.
* `0f0490b` — Deduplicated RAG sources.
* `757eeb8` — Merged pull request #13 for unique sources.
* `5ee3a59` — Extracted the RAG context builder.
* `f5ab1f5` — Merged pull request #14 for context construction.

### Outcome

The RAG pipeline gained explicit source tracking and a dedicated context-building function.

---

## October 7, 2026 — Similarity Score Threshold

**Objective:** Allow retrieval results to be filtered according to a minimum similarity score.

### Implementation

* Added the `score_threshold` parameter to semantic search.
* Added the same configuration option to the RAG entry point.
* Filtered out retrieval results whose cosine similarity score falls below the configured threshold.

### Current behavior

The default threshold is `0.0`.

The search implementation ranks results by descending cosine similarity, filters out results below the threshold, and returns up to `top_k` remaining results.

The threshold must be tuned empirically for the selected embedding model, document collection, and application. A cosine similarity score is not a calibrated probability of relevance.

### Milestones

* `2aebcf7` — Added the RAG similarity score threshold.
* `ad8a91d` — Merged pull request #15 for the score threshold.

### Outcome

Recall gained a retrieval control that can exclude low-scoring results before context construction.

---

## October 9, 2026 — Environment Validation and Dependency Management

**Objective:** Validate the development environment and make dependency installation more explicit.

### Environment

The project was validated in a Windows development environment using:

* Python 3.12.10.
* A project-specific virtual environment.
* LM Studio running locally.
* Gemma 4 E4B for generation.
* Nomic Embed Text v1.5 for embeddings.

The configured embedding model returns 768-dimensional vectors.

### Dependency management

The project uses the following direct runtime dependencies:

* `openai==3.19.2`
* `numpy==2.5.3`

The development dependency file, `requirements-dev.txt`, includes the runtime requirements and:

* `pytest==9.1.1`

The existing `pyproject.toml` defines the Python package metadata but does not yet declare runtime dependencies. Consequently, installing the project with `pip install -e .` alone does not install the runtime dependencies.

### Validation

The following checks were completed:

* Installed dependencies through `requirements-dev.txt`.
* Checked installed package dependencies with `python -m pip check`.
* Executed the full test suite with `python -m pytest -v`.
* Confirmed that all **48 tests passed**.
* Tested embedding generation against the configured LM Studio model.
* Tested language-model generation against the configured LM Studio model.
* Executed the RAG integration test against the running local models.

The RAG integration test passed independently, and the full suite passed after the dependency files were updated.

### Outcome

The local development environment and current automated test suite were validated.

These results establish that the tested execution paths work in the current environment. They do not establish retrieval quality across large corpora or guarantee that generated answers are factually correct.

---

## Current Architecture

The current implementation is organized into the following modules:

| Module               | Responsibility                                                  |
| -------------------- | --------------------------------------------------------------- |
| `config.py`          | Local model and API configuration                               |
| `lmstudio_client.py` | Communication with the language model                           |
| `embeddings.py`      | Generation of text embeddings                                   |
| `similarity.py`      | Cosine similarity calculation                                   |
| `search.py`          | Semantic ranking, `top_k`, and score filtering                  |
| `chunking.py`        | Fixed-size word chunking with overlap                           |
| `document_loader.py` | Loading and chunking Markdown documents                         |
| `prompt.py`          | Prompt construction                                             |
| `rag.py`             | Coordination of retrieval, context construction, and generation |

The Python package remains named `devassistant`, although the repository and product are now named Recall.

---

## Known Limitations

The following limitations are identified from the current implementation.

### 1. No persistent embedding index

Document embeddings are recomputed during each search.

This is simple for a small corpus but can become expensive as the document collection grows.

### 2. Basic chunking strategy

Chunking is based on word counts rather than Markdown structure, semantic boundaries, or programming-language syntax.

Headings, code blocks, and related passages can therefore be separated across chunks.

### 3. Minimal prompt constraints

The current prompt combines the retrieved context and the user's question.

It does not yet provide explicit, robust instructions requiring every answer to be grounded in the retrieved context or defining how to handle insufficient evidence.

### 4. Limited retrieval evaluation

Automated tests validate individual components and execution paths, but no systematic retrieval benchmark has been established.

Retrieval relevance, threshold selection, answer faithfulness, and performance on larger corpora still require evaluation.

### 5. Markdown-only document ingestion

The document loader currently supports Markdown files.

Other formats would require additional ingestion and text-extraction logic.

### 6. Dependency declaration in package metadata

Runtime dependencies are currently managed through requirements files rather than being declared in `pyproject.toml`.

The package installation workflow can be improved so that installing the package automatically installs its runtime dependencies.

---

## Potential Next Steps

The following items are candidates for future work. They are not yet considered implemented features.

* Add explicit grounding instructions to the RAG prompt.
* Test how the system behaves when the retrieved context does not contain the answer.
* Build a retrieval evaluation dataset and measure retrieval quality.
* Evaluate different chunk sizes and overlap settings.
* Investigate persistent embeddings and vector indexing.
* Measure search latency and memory consumption on larger document collections.
* Improve chunking for technical documentation and source code.
* Consider support for additional document formats.
* Declare runtime dependencies in `pyproject.toml`.
* Improve error handling for unavailable models and API failures.

Future work should be prioritized based on measured limitations rather than assumed benefits.

---

## Logging Policy

This file is intended to remain a chronological development log.

When recording future work:

1. Add a dated entry after a meaningful implementation milestone.
2. Record the objective and the changes actually made.
3. Include relevant commit or pull request references when available.
4. Record test results only after executing the tests.
5. Distinguish implemented functionality from planned improvements.
6. Update the known limitations when a limitation is resolved or a new one is identified.

The README describes the current project. This file explains how the project reached that state.
