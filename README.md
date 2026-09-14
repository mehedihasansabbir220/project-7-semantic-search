# Semantic Search Engine

A complete, educational implementation of a semantic search system. Find documents by **meaning**, not just keywords.

## 🎯 Problem

Traditional keyword search finds documents with exact word matches:
```
Query: "How do computers learn?"
Keyword Search: ❌ No results (exact phrase not found)
Semantic Search: ✅ Returns "Machine Learning" article
```

Semantic search understands **meaning** using AI embeddings:
- Finds synonyms ("learning" ≈ "understanding")
- Handles paraphrases ("systems that learn" ≈ "machine learning")
- Grasps related concepts (transformers in NLP)
- Tolerates natural language phrasing

## ✨ Features

- **🧠 Semantic Search**: Meaning-based document retrieval using embeddings
- **📊 Embeddings**: 384-dimensional vectors from Sentence Transformers
- **📄 Document Chunking**: Split large documents into searchable pieces with overlap
- **⚡ Vector Search**: Cosine similarity for ranking results
- **🎯 Ranked Results**: Results sorted by relevance score (0.0-1.0)
- **🔌 FastAPI Backend**: RESTful API for all search operations
- **🎨 Next.js Frontend**: Modern, responsive web interface
- **💾 Local Vector Search**: In-memory search with Python dictionary
- **☁️ Pinecone Integration**: Optional cloud vector database (not implemented in starter version)

## 🏗️ Architecture

```
Next.js Frontend (http://localhost:3000)
        ↓ HTTP POST /search
        ↓
FastAPI Backend (http://localhost:8000)
        ↓
Sentence Transformer Model
        ↓ Encodes query to embedding
        ↓
[0.23, -0.15, 0.89, ..., -0.34]  ← 384-dimensional vector
        ↓
Vector Store (Local or Pinecone)
        ↓
Compare query embedding with all document embeddings
        ↓ Cosine Similarity
        ↓
Rank by score (highest first)
        ↓
Return top-K results with metadata
        ↓
Frontend displays ranked results
```

## 📚 How Semantic Search Works

### Step 1: Document Preparation
```
Raw Document (10,000 words)
  ↓
Split into chunks (300 chars, 50 char overlap)
  ↓
57 chunks from 3 documents
```

### Step 2: Embedding Generation
```
Each chunk text:
"Machine learning is a subset of artificial intelligence..."
  ↓
SentenceTransformer model encodes
  ↓
[0.23, -0.15, 0.89, ..., -0.34]  ← Fixed 384-dimensional vector
```

### Step 3: Query Encoding
```
User query:
"What is machine learning?"
  ↓
Same SentenceTransformer encodes
  ↓
[0.24, -0.14, 0.87, ..., -0.33]  ← Similar to ML document!
```

### Step 4: Similarity Search
```
Compare query vector with all 57 document vectors
  ↓
Cosine similarity: cos(θ) = (A·B) / (|A| × |B|)
  ↓
chunk_001: 0.987 ✓
chunk_002: 0.234
chunk_003: 0.912 ✓
...
```

### Step 5: Ranking & Display
```
Sort by similarity score (highest first)
  ↓
Return top-5 results
  ↓
Frontend displays with:
  • Similarity percentage
  • Document snippet
  • Source file
  • Relevance badge
```

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- FastAPI (web framework)
- Uvicorn (ASGI server)
- sentence-transformers (embeddings)
- PyTorch (neural networks)
- NumPy (numerical computing)

**Frontend:**
- Next.js 14 (React framework)
- TypeScript (type safety)
- Tailwind CSS (styling)
- React Hooks (state management)

**Vector Search:**
- Local: Python dictionary + cosine similarity
- Optional: Pinecone (cloud vector database)

**Development:**
- Git (version control)
- Python venv (environment management)
- npm/Node.js (frontend package management)

## 📁 Project Structure

```
project-7-semantic-search/
├── README.md                          # This file
├── SETUP_GUIDE.md                     # Installation instructions
├── TASK_05_GUIDE.md                   # Document chunking guide
├── TASK_09_EVALUATION.md              # Search evaluation framework
│
├── backend/                           # Python backend
│   ├── main.py                        # FastAPI application
│   ├── requirements.txt               # Python dependencies
│   │
│   ├── api/                           # HTTP API layer
│   │   ├── routes.py                  # Endpoints (/search, /health)
│   │   └── schemas.py                 # Pydantic models
│   │
│   ├── services/                      # Business logic
│   │   └── search_service.py          # Search orchestration
│   │
│   ├── ingestion/                     # Document processing
│   │   ├── loader.py                  # Load .txt files
│   │   └── chunker.py                 # Split into chunks
│   │
│   ├── evaluation/                    # Evaluation framework
│   │   ├── dataset.py                 # Test queries
│   │   ├── keyword_search.py          # Keyword search impl.
│   │   ├── metrics.py                 # Precision, recall, MRR
│   │   └── compare.py                 # Semantic vs keyword comparison
│   │
│   ├── data/
│   │   └── sample_documents/          # Example documents
│   │       ├── machine_learning.txt
│   │       ├── deep_learning.txt
│   │       └── nlp_guide.txt
│   │
│   └── embeddings/                    # Embedding generation
│       ├── generate_embeddings.py
│       ├── index_documents.py         # Full pipeline
│       └── demo_pipeline.py           # Demo without dependencies
│
├── frontend/                          # Next.js frontend
│   ├── app/
│   │   ├── page.tsx                   # Main search page
│   │   ├── layout.tsx                 # Root layout
│   │   └── globals.css                # Global styles
│   │
│   ├── components/                    # React components
│   │   ├── Header.tsx
│   │   ├── SearchForm.tsx
│   │   ├── SearchResult.tsx
│   │   ├── LoadingState.tsx
│   │   └── EmptyState.tsx
│   │
│   ├── lib/                           # Utilities
│   │   └── api.ts                     # API client
│   │
│   ├── types/                         # TypeScript types
│   │   └── index.ts
│   │
│   ├── package.json                   # Node dependencies
│   ├── tsconfig.json                  # TypeScript config
│   ├── tailwind.config.ts             # Tailwind config
│   └── next.config.js                 # Next.js config
│
└── docs/                              # Documentation
    ├── architecture.md                # System design
    └── learning-notes.md              # Concepts learned
```

## 🚀 Local Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- ~5GB free disk space (for embedding model)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --port 8000
```

Backend runs at: **http://localhost:8000**

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:3000**

### Configuration

Create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📡 API Documentation

### Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "chunks_indexed": 57
}
```

### Search
```bash
POST /search
Content-Type: application/json

{
  "query": "machine learning algorithms",
  "top_k": 5
}
```

**Response:**
```json
{
  "query": "machine learning algorithms",
  "top_k": 5,
  "total_results": 3,
  "results": [
    {
      "chunk_id": "doc_001_chunk_0000",
      "document_id": "doc_001",
      "score": 0.987,
      "text": "Machine learning is a subset...",
      "filename": "machine_learning.txt"
    }
  ]
}
```

### Interactive Docs
- Swagger UI: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

## 📊 Search Evaluation

Includes comparison framework for evaluating semantic vs keyword search:

```bash
cd backend
python evaluation/compare.py
```

Results show:
- **Precision@K**: % of top-K results that are relevant
- **Recall@K**: % of all relevant docs found
- **Winner**: Which approach works better for each query

See [TASK_09_EVALUATION.md](TASK_09_EVALUATION.md) for detailed analysis.

## 📖 What I Learned

### Tasks 1-4: Foundations
- How embeddings represent semantic meaning
- Vector mathematics (dot product, magnitude, cosine similarity)
- Why pre-trained models are more efficient than training from scratch

### Task 5: Document Preparation
- Why documents must be chunked (token limits)
- Importance of overlap in chunking (context preservation)
- Metadata tracking for search result interpretation

### Task 6: API Design
- FastAPI for rapid API development
- Pydantic for data validation
- Separation of concerns (routes vs services)
- CORS for frontend-backend communication

### Task 7: Frontend Development
- Next.js and App Router patterns
- React Hooks for state management
- TypeScript for type safety
- Tailwind CSS for responsive design

### Task 8: Vector Databases
- Local vs cloud-based search trade-offs
- Why vector databases are necessary at scale
- Abstraction layers for swappable implementations

### Task 9: Evaluation
- Precision vs recall trade-off
- When keyword search outperforms semantic
- Importance of evaluation metrics
- Why hybrid search combines strengths

## 🔮 Future Improvements

- **Hybrid Search**: Combine semantic + keyword ranking
- **Reranking**: Secondary ranking to improve precision
- **Better Chunking**: Sentence/semantic-based instead of fixed-size
- **PDF Ingestion**: Support PDF documents, not just text
- **Multilingual Search**: Support multiple languages
- **Filtering**: Filter results by document, date, category
- **Authentication**: User accounts and access control
- **Analytics**: Track popular queries and search patterns
- **Batch Upload**: Upload multiple documents at once
- **Query Expansion**: Automatically expand queries with related terms
- **Caching**: Cache frequent query results
- **Performance**: GPU acceleration for faster embeddings

## 🎓 Key Insights

1. **Semantic search is powerful but not universal**
   - Great for synonyms, paraphrases, related concepts
   - Weaker at exact technical terms

2. **Keyword search has unexpected strengths**
   - Better precision on technical queries
   - Faster with no model overhead
   - More interpretable (clear why results matched)

3. **Hybrid approaches are practical**
   - Semantic for recall, keyword for precision
   - Combine scores: 70% semantic + 30% keyword
   - Best performance on diverse queries

4. **Evaluation matters**
   - Always measure precision and recall
   - Different domains have different priorities
   - Benchmarking reveals non-obvious trade-offs

## 🔗 Resources

- [Sentence Transformers](https://www.sbert.net/) - Embedding models
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [Semantic Search Deep Dive](docs/architecture.md) - System design

## 📝 License

Educational project. Feel free to use for learning purposes.

## 🤝 Contributing

This is an educational project. Suggestions and improvements welcome!

---

**Start searching:** `npm run dev` in frontend, `uvicorn main:app --reload` in backend, then visit http://localhost:3000

**Questions?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for installation help or [docs/](docs/) for deep dives.
