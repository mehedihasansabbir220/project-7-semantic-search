# Backend: Semantic Search Core & API

This folder contains Phases 1 and 2 of the project.

## Phase 1: Core Semantic Search (Python)

The foundation that powers everything. We'll build:

- **Embedding Generator**: Convert text to vectors using Sentence Transformers
- **Vector Store**: Store embeddings in NumPy arrays (in-memory)
- **Search Engine**: Find similar vectors using cosine similarity
- **CLI Interface**: Command-line tool to test the system

### What You'll Learn

- How pre-trained models work
- Storing and manipulating embeddings with NumPy
- Computing cosine similarity between vectors
- Building a simple search engine from scratch

### Expected Output

A Python CLI that can:
```
$ python search.py index documents.txt
$ python search.py query "What's a red fruit?"
Results:
  1. apple (similarity: 0.98)
  2. cherry (similarity: 0.95)
  3. strawberry (similarity: 0.93)
```

---

## Phase 2: REST API (FastAPI)

Wrap Phase 1 in an HTTP API.

- **Endpoints**: `/search` and `/index`
- **JSON**: Structured request/response
- **Server**: Runs on localhost:8000

### What You'll Learn

- Building REST APIs with FastAPI
- Connecting frontend and backend
- Request validation
- Response formatting

### Expected Output

```bash
$ python -m uvicorn api:app --reload
$ curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a red fruit?"}'
```

---

## Implementation Status

- [ ] Phase 1: Core implementation
- [ ] Phase 1: CLI testing
- [ ] Phase 2: FastAPI setup
- [ ] Phase 2: Endpoints

---

## Dependencies (Will Install in Phase 1)

```
sentence-transformers   # Embeddings
numpy                   # Vector operations
fastapi                 # API (Phase 2)
uvicorn                 # Server (Phase 2)
```

---

## Folder Structure (Will Grow)

```
backend/
├── README.md
├── requirements.txt          (Phase 1)
├── search_engine.py          (Phase 1 - core logic)
├── cli.py                    (Phase 1 - CLI interface)
├── api.py                    (Phase 2 - FastAPI)
└── documents/                (sample documents)
```

---

## Getting Started

When ready:

1. Set up Python environment
2. Install dependencies
3. Understand embeddings concept
4. Build core search engine
5. Test with CLI
6. Wrap in FastAPI (Phase 2)

**Next**: Proceed to Phase 1 when you understand the concepts in `docs/semantic-search.md`.
