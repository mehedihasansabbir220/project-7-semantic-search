# Task 09: Semantic vs Keyword Search Evaluation

## 📊 Evaluation Framework

### What We're Testing

```
10 Test Queries
├── Exact Matches (1-2 queries)
│   └─ "algorithms for machine learning"
├── Paraphrases (2-3 queries)
│   └─ "how do computers learn from data?"
├── Synonyms (2-3 queries)
│   └─ "neural networks and deep architectures"
├── Related Concepts (1-2 queries)
│   └─ "tree-based decision making models"
└── Technical Terms (1-2 queries)
    └─ "SVM kernel trick nonlinear data"
```

Each query has **expected relevant chunks** for evaluation.

---

## 🔍 Search Approaches

### Keyword Search

**How it works:**
```
Query: "machine learning algorithms"
  ↓
Split into words: ["machine", "learning", "algorithms"]
  ↓
Find documents containing these words
  ↓
Score by: number of matching words
  ↓
Return results with highest scores
```

**Scoring example:**
```
Query: "machine learning algorithms"

Doc A: "Machine learning is using algorithms..."
       Matched: [machine, learning, algorithms] = score 3

Doc B: "Deep learning uses neural networks"
       Matched: [learning] = score 1

Doc C: "Classification algorithms for ML"
       Matched: [algorithms, learning] = score 2

Result order: Doc A (3) > Doc C (2) > Doc B (1)
```

**Pros:**
- ✅ Fast (simple word matching)
- ✅ Transparent (easy to explain why a result matched)
- ✅ Good for exact technical terms
- ✅ No model needed (no computational cost)

**Cons:**
- ❌ Doesn't understand synonyms ("learning" ≠ "studying")
- ❌ Can't handle paraphrases
- ❌ Misses related concepts
- ❌ Sensitive to exact wording

### Semantic Search

**How it works:**
```
Query: "machine learning algorithms"
  ↓
Convert to embedding: [0.23, -0.15, 0.89, ...]
  ↓
Compare with all document embeddings
  ↓
Score by: vector similarity (cosine)
  ↓
Return results with highest similarity
```

**Key property:**
```
Similar meanings = Similar embeddings

"machine learning"      ≈ [0.23, -0.15, 0.89, ...]
"systems that learn"    ≈ [0.24, -0.14, 0.88, ...]  ← Very similar!
"computer algorithms"   ≈ [0.25, -0.16, 0.87, ...]  ← Similar!
"pizza recipes"         ≈ [0.01, 0.92, -0.02, ...]  ← Very different!

Semantic search WOULD match the related queries
Keyword search would NOT (different words)
```

**Pros:**
- ✅ Understands meaning (synonyms, paraphrases)
- ✅ Handles related concepts
- ✅ More forgiving of wording differences
- ✅ Better for natural language queries

**Cons:**
- ❌ Slower (requires neural network inference)
- ❌ Less transparent (hard to explain why)
- ❌ Requires embedding model
- ❌ Can match unrelated concepts with similar embeddings

---

## 📈 Evaluation Metrics

### Precision@K: "Are results GOOD?"

**Question:** What fraction of top-K results are actually relevant?

**Example:**
```
You search for "machine learning" and get 5 results:

Result 1: "ML Basics"                 ✓ RELEVANT
Result 2: "How to bake cookies"       ✗ NOT relevant
Result 3: "Deep learning guide"       ✓ RELEVANT
Result 4: "Shopping list"             ✗ NOT relevant
Result 5: "Neural networks"           ✓ RELEVANT

Precision@5 = 3 relevant / 5 total = 0.60 = 60%

Interpretation: 60% of my results are relevant (40% garbage)
```

**Use case:**
- Search engines (Google aims for high precision)
- Medical search (false positives are costly)
- When quality > quantity matters

**Values:**
- 1.0 = All results relevant (perfect)
- 0.5 = Half are relevant
- 0.0 = No relevant results

### Recall@K: "Did we find EVERYTHING?"

**Question:** What fraction of all relevant documents did we find?

**Example:**
```
Total relevant documents about "machine learning": 5

You search and find:
Result 1: "ML Basics"           ✓ Found
Result 3: "Deep learning"       ✓ Found
Result 5: "Neural networks"     ✓ Found
(Results 2 and 4 are missing)

Recall@5 = 3 found / 5 total = 0.60 = 60%

Interpretation: I found 60% of all relevant results (missed 40%)
```

**Use case:**
- Legal discovery (must find all relevant documents)
- Patent search (need comprehensive coverage)
- When quantity > quality matters

**Values:**
- 1.0 = Found all relevant (perfect)
- 0.5 = Found half
- 0.0 = Found none

### Precision vs Recall Trade-off

```
High Precision (narrow results)
├─ Show only what you're confident about
├─ Few results, high quality
└─ Risk: Miss relevant documents

High Recall (broad results)
├─ Show everything that might match
├─ Many results, some irrelevant
└─ Risk: Overwhelm user with options
```

**In practice:**
```
Perfect search would be:
- Precision@5: 1.0 (all 5 are relevant)
- Recall@5: 1.0 (includes all relevant docs)

But usually these trade off:
- High precision, low recall: Few good results
- Low precision, high recall: Many mixed results
```

### Mean Reciprocal Rank (MRR): "How far to first match?"

**Question:** What position is the first relevant result?

**Example:**
```
Result 1: "Pizza recipes"         ✗ NOT relevant
Result 2: "Cooking tips"          ✗ NOT relevant
Result 3: "Machine learning"      ✓ RELEVANT! (first match)
Result 4: "Deep learning"         ✓ RELEVANT
Result 5: "Neural networks"       ✓ RELEVANT

MRR = 1 / 3 = 0.33

Interpretation: First relevant result at position 3
```

**Use case:**
- When users only check top few results
- Web search (users rarely go past page 1)

**Values:**
- 1.0 = First result is relevant
- 0.5 = First relevant at position 2
- 0.33 = First relevant at position 3
- 0.0 = No relevant results

---

## 🎯 When Each Approach Wins

### Semantic Search Wins

**Scenario 1: Paraphrases**
```
Query: "How do systems learn from data?"
Expected: Document about machine learning

Keyword Search:
  "how"=common, "systems"=common, "learn"=not present
  Score: low (doesn't match "machine learning")
  Result: ✗ MISS

Semantic Search:
  Understands: "learn from data" ≈ "machine learning"
  Similarity: High
  Result: ✓ HIT
```

**Scenario 2: Synonyms**
```
Query: "deep neural architectures"
Expected: Document about deep learning

Keyword Search:
  No "deep learning" phrase
  Score: low
  Result: ✗ MISS (different words)

Semantic Search:
  "neural architectures" ≈ "deep learning"
  Similarity: High
  Result: ✓ HIT
```

**Scenario 3: Related Concepts**
```
Query: "tree-based classification models"
Expected: Document mentioning decision trees

Keyword Search:
  "tree" not mentioned, "decision" not present
  Score: low
  Result: ✗ MISS (different words)

Semantic Search:
  Understands ML concept relationships
  "classification models" related to decision trees
  Result: ✓ HIT (partial match on concept)
```

### Keyword Search Wins

**Scenario 1: Exact Technical Terms**
```
Query: "SVM kernel trick"
Expected: Document about Support Vector Machines

Keyword Search:
  "SVM" present (exact match)
  "kernel" present
  Score: very high
  Result: ✓ HIT (perfect precision)

Semantic Search:
  Understands "SVM" ≈ "support vector machine"
  But might also match "machine learning" generically
  Lower precision (false positives)
  Result: ✗ Lower precision
```

**Scenario 2: Domain-Specific Terms**
```
Query: "convolutional neural networks CNN"
Expected: Document about CNN architecture

Keyword Search:
  "convolutional", "neural", "networks", "CNN" all present
  Score: very high
  Result: ✓ HIT (precise match)

Semantic Search:
  "CNN" understood, but also matches "deep learning" generically
  Less precise
  Result: ✗ Lower precision
```

**Scenario 3: Speed-Critical Scenarios**
```
Query: "machine learning algorithms"

Keyword Search:
  Time: <1ms (simple word matching)
  Result: ✓ FAST

Semantic Search:
  Time: 500ms (model inference)
  Result: ✗ SLOW
```

---

## 🔄 Hybrid Search: Best of Both Worlds

**Concept:** Use both approaches together

```
Query: "how to train neural networks"
  ↓
Step 1: SEMANTIC search for candidates
  Find semantically similar chunks
  Broad recall (catches paraphrases)
  Result: [doc_1, doc_2, doc_3, doc_4, doc_5]
  ↓
Step 2: KEYWORD filter for precision
  Keep only docs with "train", "neural", or "networks"
  Narrow down results
  Result: [doc_1, doc_3] (best matches)
  ↓
Step 3: RERANK using both signals
  Score = 0.7 * semantic_score + 0.3 * keyword_score
  Result: Best of both approaches
```

### Hybrid Benefits

```
✅ High recall (semantic finds paraphrases)
✅ High precision (keywords validate relevance)
✅ Interpretable (can see why each result matched)
✅ Robust (if one approach fails, other can help)
```

### Real-World Examples

**Elasticsearch:**
```
GET /documents/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"text": "machine learning"}},    # Keyword
        {"knn": {"embedding": [0.23, -0.15, ...]}} # Semantic
      ]
    }
  }
}
```

**Production Search Pipeline:**
```
1. Keyword search for broad matching
2. Semantic search for related concepts
3. Combine and rerank
4. Apply domain rules
5. Return top-K to user
```

---

## 📋 Evaluation Results Summary

### What We Measure

For each query, we calculate:
- **Precision@5**: % of top-5 results that are relevant
- **Recall@5**: % of all relevant docs found in top-5
- **MRR**: Position of first relevant result

### Expected Findings

**Semantic search should excel at:**
- Paraphrases: +60% better recall
- Synonyms: +50% better recall
- Related concepts: +40% better recall
- Natural language: +30% better overall

**Keyword search should excel at:**
- Technical terms: +50% better precision
- Exact phrases: +40% better precision
- Short queries: Similar or better performance

**Trade-offs:**
- Semantic: Better recall, lower precision
- Keyword: Better precision, lower recall

---

## 🎓 Key Lessons

### 1. No Single Best Approach
Different queries benefit from different methods

### 2. Context Matters
- Medical search: Precision first (avoid false positives)
- Legal search: Recall first (find all relevant docs)
- Web search: Balance (precision and usability)

### 3. Hybrid is Powerful
Combining approaches usually beats either alone

### 4. Metrics Drive Decisions
Always measure, don't assume

### 5. Trade-offs are Fundamental
Can't have perfect precision AND recall simultaneously

---

## 🚀 Running the Evaluation

```bash
cd backend
python evaluation/compare.py
```

This will:
1. Load 10 test queries
2. Run keyword search for each
3. Run semantic search for each
4. Compare results
5. Calculate metrics
6. Display analysis

**Output includes:**
- Query details
- Results from both methods
- Metric comparison
- Winner analysis
- Category breakdown
- Key insights

---

**Summary:** Semantic search is powerful but not universal. Keywords solve problems semantic can't, and hybrid approaches combine their strengths. Evaluation matters! 📊

