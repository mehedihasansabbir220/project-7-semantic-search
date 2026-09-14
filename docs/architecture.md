# Semantic Search Architecture

Deep dive into how this semantic search system works, from raw documents to ranked results.

## 📋 Table of Contents

1. [High-Level Overview](#high-level-overview)
2. [Document Pipeline](#document-pipeline)
3. [Embedding Generation](#embedding-generation)
4. [Vector Search](#vector-search)
5. [API Design](#api-design)
6. [Comparison with Keyword Search](#comparison-with-keyword-search)
7. [Performance Considerations](#performance-considerations)
8. [Future Improvements](#future-improvements)

## 🎯 High-Level Overview

### The Problem We're Solving

Traditional keyword search:
```
User Query: "How do computers learn?"
Match exact words: machine, learning
Result: ❌ No exact match found
```

Semantic search:
```
User Query: "How do computers learn?"
Understand meaning
Result: ✅ Returns "Machine Learning" article
```

### Architecture Layers

```
┌─────────────────────────────────────┐
│   Next.js Frontend                  │  HTTP requests
│   (User Interface)                  │
└────────────┬────────────────────────┘
             │ POST /search + query
             │
┌────────────▼────────────────────────┐
│   FastAPI Backend                   │  Route requests
│   (HTTP API)                        │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Search Service                    │  Orchestrate search
│   (Business Logic)                  │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Sentence Transformer              │  Encode text to vectors
│   (Embedding Model)                 │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Vector Store                      │  Store & search vectors
│   (Local or Pinecone)               │
└─────────────────────────────────────┘
```

## 📄 Document Pipeline

### Step 1: Load Documents

**File:** `backend/ingestion/loader.py`

```python
DocumentLoader
  ├─ load_documents(directory)
  │   ├─ Scan .txt files
  │   ├─ Extract text content
  │   └─ Collect metadata
  └─ Returns: List[Document]
```

**Input:** Text files in `backend/data/sample_documents/`

**Output:**
```python
[
  Document(
    id="machine_learning.txt",
    text="Machine learning is...",
    filename="machine_learning.txt",
    size=3269
  ),
  ...
]
```

### Step 2: Chunk Documents

**File:** `backend/ingestion/chunker.py`

**Why chunk?** Embedding models have token limits (~512 tokens). Large documents must be split.

```python
DocumentChunker
  ├─ chunk_documents(documents)
  │   ├─ Split by character count (300 chars default)
  │   ├─ Add overlap (50 chars) to preserve context
  │   └─ Track positions
  └─ Returns: List[Chunk]
```

**Example:**

Original: "Machine learning is a subset of artificial intelligence. AI systems learn from data..."

**Chunks (with 50-char overlap):**
```
Chunk 1: "Machine learning is a subset of artificial
           intelligence. AI systems learn"

Chunk 2: "intelligence. AI systems learn from data without
           being explicitly programmed."

Chunk 3: "being explicitly programmed. This enables..."
```

**Why overlap?** Context at chunk boundaries is preserved. A sentence spanning chunk boundary doesn't lose meaning.

**Output Structure:**
```python
Chunk(
  id="machine_learning_chunk_0000",
  document_id="machine_learning.txt",
  text="Machine learning is...",
  start_position=0,
  end_position=300
)
```

### Step 3: Create Embeddings

**File:** `backend/embeddings/index_documents.py`

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

```python
LocalChunkIndex
  ├─ embed_chunks(chunks)
  │   ├─ Load Transformer model (384-dim)
  │   ├─ Encode each chunk to vector
  │   └─ Store in memory dict
  └─ Returns: {chunk_id: Vector}
```

**What's an embedding?**

A 384-dimensional vector representing semantic meaning.

```
"Machine learning" → [0.23, -0.15, 0.89, ..., -0.34]
"AI learning system" → [0.24, -0.14, 0.87, ..., -0.33]  ← Similar!
"Pizza recipes" → [0.01, 0.34, -0.12, ..., 0.92]      ← Different!
```

**Why Sentence Transformers?** 
- Specifically trained on sentence/document similarity
- Handles variable-length inputs
- Fast inference
- Good performance for semantic search

## 🔍 Vector Search

### Query Encoding

When user submits query:

```python
1. User types: "How do computers learn?"

2. SearchService.search(query, top_k=5)
   ├─ Encode query with same model
   └─ Returns: [0.22, -0.16, 0.90, ..., -0.33]
```

### Similarity Calculation

**Cosine Similarity:** Measure angle between vectors

```
cos(θ) = (A · B) / (|A| × |B|)

Where:
- A = query embedding
- B = document embedding
- Result: -1 to 1 (typically 0 to 1 for our use case)

High similarity (close to 1.0):
  Vectors point in same direction
  → Semantically similar

Low similarity (close to 0):
  Vectors point in different directions
  → Semantically different
```

**Example Calculation:**

Query: "machine learning"
```
Query embedding: [0.23, -0.15, 0.89, ...]

Against chunk_001 (ML article):
  chunk_001: [0.24, -0.14, 0.87, ...]
  Cosine similarity = 0.987 ✓ Very relevant

Against chunk_002 (Pizza recipe):
  chunk_002: [0.01, 0.34, -0.12, ...]
  Cosine similarity = 0.234 ✗ Not relevant
```

### Ranking

```python
VectorStore.query(query_embedding, top_k=5)
  ├─ Calculate similarity for all stored vectors
  ├─ Sort by similarity (highest first)
  └─ Return top-K results with scores
```

## 🔌 API Design

### Endpoint: POST /search

**Request:**
```json
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
      "chunk_id": "machine_learning_chunk_0000",
      "document_id": "machine_learning.txt",
      "score": 0.987,
      "text": "Machine learning is a subset...",
      "filename": "machine_learning.txt"
    },
    ...
  ]
}
```

### Data Flow

```
HTTP Request (JSON)
    ↓
FastAPI (routes.py)
    ├─ Validate Pydantic schema
    └─ Call SearchService.search()
    ↓
SearchService (search_service.py)
    ├─ Encode query
    ├─ Query vector store
    └─ Format results
    ↓
HTTP Response (JSON)
    ↓
Next.js Frontend (pages)
    ├─ Parse results
    └─ Render UI
```

### Error Handling

```python
@router.post("/search")
async def search(request: SearchRequest):
    try:
        # Validate input
        # Search
        # Return results
    except ValueError as e:
        return ErrorResponse(
            error="invalid_query",
            message=str(e)
        )
    except Exception as e:
        return ErrorResponse(
            error="server_error",
            message="Search service error"
        )
```

## 📊 Comparison with Keyword Search

### Keyword Search (Traditional)

**Algorithm:**
```
1. Tokenize query into words
2. Find exact word matches in documents
3. Score by word frequency
4. Rank results
```

**Example:**
```
Query: "machine learning"
Words: ["machine", "learning"]

Document 1: Contains "machine" and "learning" → Score: 2
Document 2: Contains "machine" only → Score: 1
Document 3: No match → Score: 0

Result: Document 1 > Document 2 > Document 3
```

**Strengths:**
- ✅ Fast (no model needed)
- ✅ Interpretable (you see why it matched)
- ✅ Good for technical terms ("SVM", "CNN")
- ✅ Exact phrase matching

**Weaknesses:**
- ❌ Misses synonyms ("learning" ≠ "understanding")
- ❌ Handles paraphrases poorly
- ❌ No semantic understanding

### Semantic Search (This Project)

**Algorithm:**
```
1. Encode query to 384-dimensional vector
2. Encode all documents to vectors
3. Calculate cosine similarity
4. Rank by similarity score
```

**Example:**
```
Query: "How do computers learn?"
Encoding: [0.23, -0.15, 0.89, ...]

Document 1 (ML article): [0.24, -0.14, 0.87, ...] 
  Similarity: 0.987 ✓

Document 2 (Pizza): [0.01, 0.34, -0.12, ...]
  Similarity: 0.234 ✗

Result: Document 1 >> Document 2
```

**Strengths:**
- ✅ Understands synonyms ("learning" ≈ "understanding")
- ✅ Handles paraphrases
- ✅ Grasps related concepts
- ✅ Works with natural language

**Weaknesses:**
- ❌ Slower (requires model inference)
- ❌ Less interpretable (black box)
- ❌ May be too broad (lower precision)

### Head-to-Head Comparison

| Feature | Keyword | Semantic |
|---------|---------|----------|
| Speed | ⚡ Very fast | ⚠️ Slower (0.5s) |
| Synonyms | ❌ No | ✅ Yes |
| Paraphrases | ❌ No | ✅ Yes |
| Related concepts | ❌ No | ✅ Yes |
| Technical terms | ✅ Precise | ⚠️ Approximate |
| Interpretability | ✅ Clear | ❌ Black box |
| Memory | ✅ Minimal | ⚠️ 5GB for model |

## ⚡ Performance Considerations

### Bottlenecks

**1. Model Loading (First Query)**
```
Problem: Sentence Transformer loads on first use (~10s)
Solution: Pre-load model on server startup
Current: DONE - Handled in FastAPI lifespan
```

**2. Embedding Generation**
```
Problem: Encoding each query takes ~0.5s
Reason: Deep neural network inference
Solutions:
  - GPU acceleration (not in starter version)
  - Query caching (optional future improvement)
  - Batch queries (optional future improvement)
```

**3. Similarity Calculation**
```
Problem: Must compare query with all 57 chunks
Time: O(n) where n = number of chunks
Solution: 
  - For <1M vectors: In-memory dict (current)
  - For >1M vectors: Use Pinecone/FAISS (future)
```

**4. Frontend Latency**
```
Total: ~1-2 seconds per search
Breakdown:
  - Network: 100ms
  - Query encoding: 500ms
  - Vector search: 50ms
  - Ranking & formatting: 50ms
  - Network back: 100ms
```

### Optimization Opportunities

**Current:**
- ✅ Lazy model loading (load once, reuse)
- ✅ In-memory storage (fast access)
- ✅ Efficient cosine similarity (NumPy)

**Future:**
- GPU acceleration (CUDA for faster inference)
- Query caching (cache popular queries)
- Pinecone integration (billions of vectors)
- FAISS index (better scaling than dict)
- Approximate nearest neighbor (trade accuracy for speed)

## 🔮 Future Improvements

### 1. Hybrid Search

Combine both approaches:
```
Score = 0.7 * semantic_score + 0.3 * keyword_score

Benefits:
- Semantic recall + keyword precision
- Better coverage of diverse queries
```

### 2. Reranking

Two-stage approach:
```
1. Fast semantic search → top 100 candidates
2. Slower but more precise model → rerank top 10

Result: Better quality with reasonable speed
```

### 3. Query Expansion

Automatically expand queries:
```
User: "machine learning"
Expanded: ["machine learning", "deep learning", 
           "neural networks", "AI", "data science"]

Benefit: Better recall without user typing more
```

### 4. Pinecone Integration

```python
class PineconeVectorStore:
    def query(self, embedding, top_k=5):
        # Query Pinecone cloud service
        # Returns ranked results
        # Supports billions of vectors
```

### 5. Better Chunking

```
Current: Fixed-size chunks (300 chars)

Improvements:
- Sentence-based chunks (preserve structure)
- Semantic chunks (similar meaning together)
- Hierarchical chunks (paragraph → section → doc)
```

### 6. PDF Support

```python
class PDFLoader:
    def load_documents(directory):
        # Extract text from PDFs
        # Preserve formatting
        # Handle tables & images
```

### 7. Multilingual Search

```
Model: multilingual-all-MiniLM-L12-v2
Support: 50+ languages
Benefit: Search across language barriers
```

### 8. Filtering

```python
results = search(
    query="machine learning",
    filters={
        "document": "machine_learning.txt",
        "min_score": 0.8
    }
)
```

### 9. Analytics

Track:
- Popular queries
- Search latency
- Click-through rates
- User engagement

### 10. Authentication

```python
@router.post("/search")
@require_auth
def search(request: SearchRequest, user: User):
    # Search with user context
    # Track per-user metrics
```

## 📚 Key Concepts Summary

### Embeddings
- Fixed-size vectors representing text meaning
- Generated by neural networks (384-dim here)
- Similar texts have similar embeddings

### Cosine Similarity
- Measure of angle between vectors
- Range: 0 to 1 (0=different, 1=identical)
- Fast computation with NumPy dot product

### Vector Search
- Find vectors closest to query vector
- Sort by similarity score
- Return top-K results

### Document Chunking
- Split large documents into pieces
- Add overlap to preserve context
- Necessary for embedding model limits

### Semantic vs Keyword
- Semantic: Understands meaning (better recall)
- Keyword: Exact word matching (better precision)
- Both have strengths; hybrid is best

---

For implementation details, see the source code:
- Backend: `backend/` directory
- Frontend: `frontend/` directory
- Evaluation: `backend/evaluation/` module

Questions? Check the main [README.md](../README.md)
