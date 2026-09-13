# Project 7: Simple Semantic Search Engine

A learning project to understand how semantic search works from the ground up.

## Goal

Build a semantic search engine that can find relevant documents based on *meaning*, not just keyword matching. Learn how embeddings, vectors, and similarity metrics power modern search.

## Technology Phases

### Phase 1: Core Semantic Search (Python)
- Sentence embeddings using Sentence Transformers
- In-memory vector storage with NumPy
- Cosine similarity search
- **Output**: Python CLI that searches documents

### Phase 2: REST API (FastAPI)
- HTTP endpoints for searching and indexing
- **Output**: Backend server

### Phase 3: Web Interface (Next.js + TypeScript)
- React UI for searching
- Real-time results
- **Output**: Frontend application

### Phase 4: Production Features
- Document ingestion pipeline
- Text chunking strategies
- Metadata handling
- **Output**: Scalable document processing

### Phase 5: Vector Database (Pinecone)
- Replace in-memory storage with cloud vector DB
- Scale to millions of documents
- **Output**: Production-ready system

## Project Structure

```
project-7-semantic-search/
├── README.md                    (this file)
├── docs/
│   └── semantic-search.md       (concepts & architecture)
├── backend/
│   ├── README.md               (Phase 1-2 setup)
│   └── (implementation coming)
└── frontend/
    ├── README.md               (Phase 3 setup)
    └── (implementation coming)
```

## Next Steps

1. Read `docs/semantic-search.md` to understand the concepts
2. Start Phase 1 when ready
3. Each phase builds on the previous one

---

**Status**: Project initialized, documentation phase
