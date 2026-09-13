# Semantic Search: Understanding the Concepts

This document explains how semantic search works. Read it before writing any code.

## 1. Keyword Search (What You Already Know)

**Keyword search** finds documents by matching exact words or phrases.

```
Query: "apple fruit"
Document 1: "apple pie recipe"           ✓ Match (has "apple")
Document 2: "orange and banana"          ✗ No match
Document 3: "An apple a day..."          ✓ Match (has "apple")
```

**Problem**: Keyword search doesn't understand *meaning*.

```
Query: "sweet red fruit"
Document: "I love apples"                ✗ No match (no exact keywords)
```

Even though the document is clearly about a fruit, there's no keyword overlap.

---

## 2. Semantic Search (What We're Building)

**Semantic search** finds documents based on *meaning*, not just words.

```
Query: "sweet red fruit"
Document: "I love apples"                ✓ Match (meaning is related)
Document: "This orange is juicy"         ✓ Match (meaning is related)
Document: "I like programming"           ✗ No match (meaning is unrelated)
```

Semantic search understands that "sweet red fruit" is related to "apples" even if they don't share keywords.

**How?** By converting text into vectors (lists of numbers) and measuring how similar they are.

---

## 3. What is an Embedding?

An **embedding** is a way to represent text as numbers.

Think of it like this: instead of storing the word "apple", we store it as a list of 384 numbers:

```
Word: "apple"
Embedding: [0.12, -0.45, 0.78, 0.33, ..., -0.21]  (384 dimensions)
```

These numbers capture the *meaning* of the word in a mathematical space.

### Why numbers?

Because mathematics can measure the *distance* between numbers. Words with similar meaning will have embeddings that are *close together* mathematically.

```
Embedding("apple"):     [0.12, -0.45, 0.78, ...]
Embedding("orange"):    [0.15, -0.42, 0.80, ...]
                        ↑ Very similar (both are fruits)

Embedding("car"):       [0.88, 0.12, -0.50, ...]
                        ↑ Very different (not a fruit)
```

---

## 4. Why Can Text Be Converted Into Vectors?

**Principle**: Words that appear in similar contexts have similar meanings.

"apple" typically appears with words like: fruit, sweet, red, eat, seed
"orange" typically appears with words like: fruit, sweet, color, eat, seed

Because they share context, their embeddings are mathematically similar.

### How Embeddings Are Created

Modern embeddings are created using **neural networks** trained on billions of sentences.

The neural network learns that:
- "apple" and "orange" should have similar embeddings (both fruits)
- "apple" and "car" should have different embeddings (different categories)
- "dog runs fast" and "The canine moves quickly" should have similar embeddings (same meaning)

This training happens once. Then, we can feed any new text through the network and get its embedding instantly.

**In our project**: We'll use pre-trained Sentence Transformers models (already trained on billions of sentences, ready to use).

---

## 5. Cosine Similarity: Measuring How Similar Two Embeddings Are

Now we have embeddings (vectors). How do we measure if two vectors are similar?

**Cosine similarity** measures the angle between two vectors.

```
Imagine two arrows pointing in space:
- If they point in the same direction → angle is 0° → similarity = 1.0 (identical)
- If they point perpendicular → angle is 90° → similarity = 0 (unrelated)
- If they point opposite → angle is 180° → similarity = -1.0 (opposite)
```

**Formula**: 
```
similarity = (dot product) / (magnitude of vector1 × magnitude of vector2)
Result: Always between -1 and 1
```

### Example

```
Query embedding: "sweet fruit"        [0.10, -0.40, 0.80]
Doc1 embedding:  "apple"              [0.12, -0.38, 0.82]
Doc2 embedding:  "programming"        [0.88, 0.15, -0.50]

Cosine Similarity("sweet fruit", "apple") = 0.98  ✓ Very similar
Cosine Similarity("sweet fruit", "programming") = 0.15  ✗ Not similar
```

**In semantic search**: We compute similarity between the query embedding and all document embeddings, then return the most similar ones.

---

## 6. Vector Search: Putting It Together

**Vector search** combines everything:

1. **Convert query to embedding**
   - User types: "What's a delicious red fruit?"
   - System creates embedding: [0.11, -0.42, 0.79, ...]

2. **Compare to all document embeddings**
   - Doc1 "apple": similarity = 0.96
   - Doc2 "orange": similarity = 0.94
   - Doc3 "programming": similarity = 0.12

3. **Return top matches**
   - Sort by similarity score
   - Return most similar documents

---

## 7. Keyword Search vs. Semantic Search

| Aspect | Keyword Search | Semantic Search |
|--------|---|---|
| **Matches on** | Exact words | Meaning |
| **Representation** | Words/phrases | Vectors/numbers |
| **Similarity metric** | Present/absent | Distance/angle |
| **Paraphrases** | ✗ Miss | ✓ Find |
| **Typos** | ✗ Miss | ✓ May find |
| **Context-aware** | ✗ No | ✓ Yes |
| **Speed** | ⚡ Fast | 🐢 Slower |
| **Storage** | Inverted index | Vector database |
| **Example** | "find apple" | Find fruits like apple |

### Real Example

Query: "How to cook pasta?"

| Type | Result |
|------|--------|
| **Keyword** | Only returns docs with "cook" AND "pasta" |
| **Semantic** | Returns docs about: cooking, recipes, pasta dishes, Italian food, noodles |

---

## 8. Complete Architecture We'll Build

Here's what the final system will look like:

```
┌─────────────────────────────────────────────────────┐
│ Next.js Frontend (Phase 3)                          │
│ - React UI                                          │
│ - Search bar & results display                      │
└────────────────────┬────────────────────────────────┘
                     │ HTTP requests
                     ↓
┌─────────────────────────────────────────────────────┐
│ FastAPI Backend (Phase 2)                           │
│ - /search endpoint                                  │
│ - /index endpoint                                   │
│ - Handles requests & responses                      │
└────────────────────┬────────────────────────────────┘
                     │ Uses
                     ↓
┌─────────────────────────────────────────────────────┐
│ Semantic Search Core (Phase 1)                      │
│                                                     │
│ ┌──────────────────┐         ┌──────────────────┐  │
│ │ Text → Embedding │         │ Similarity Search│  │
│ │ (Sentence Trans) │────────▶│ (Cosine sim)     │  │
│ └──────────────────┘         └──────────────────┘  │
│           ↓                            ↑            │
│    Input text string          Output top-k docs    │
│                                                     │
│ Storage: NumPy arrays (Phase 1-4) or Pinecone      │
│          (Phase 5)                                  │
└─────────────────────────────────────────────────────┘
```

### Data Flow Example

```
User enters: "delicious red fruit"
    ↓
[Frontend] Sends query to backend
    ↓
[Backend] Receives query
    ↓
[Core] Convert to embedding: [0.11, -0.42, 0.79, ...]
    ↓
[Core] Compare to all stored doc embeddings
    ↓
[Core] Rank by cosine similarity
    ↓
[Core] Return top 5: [{id: 1, name: "apple", score: 0.96}, ...]
    ↓
[Backend] Formats response as JSON
    ↓
[Frontend] Displays results to user
```

### Phase Breakdown

**Phase 1 (Core)**: 
- Load pre-trained embedding model
- Convert text to vectors
- Store in NumPy arrays (in-memory)
- Implement cosine similarity search
- CLI interface

**Phase 2 (API)**:
- Wrap Phase 1 in FastAPI endpoints
- Handle HTTP requests
- JSON responses

**Phase 3 (Frontend)**:
- React app
- Search UI
- Display results

**Phase 4 (Production)**:
- Ingest documents from files
- Chunk long documents
- Store metadata (source, date, etc.)

**Phase 5 (Scale)**:
- Replace NumPy storage with Pinecone
- Handle millions of vectors
- Cloud-based

---

## Key Concepts Summary

| Concept | What It Is | Why It Matters |
|---------|-----------|---|
| **Embedding** | Text represented as numbers | Allows mathematical similarity |
| **Vector** | List of numbers (embedding) | The actual data we work with |
| **Cosine Similarity** | Angle between two vectors | Measures how related two meanings are |
| **Vector Search** | Finding similar vectors quickly | The core search operation |
| **Semantic** | Based on meaning | Understanding intent, not keywords |

---

## What You'll Learn in Each Phase

1. **Phase 1**: How embeddings work + implementing vector search in pure Python
2. **Phase 2**: Building APIs with FastAPI
3. **Phase 3**: Frontend state management & UI
4. **Phase 4**: Text processing & chunking strategies
5. **Phase 5**: Production vector databases

---

## Before You Code

Make sure you understand:
- [ ] How keyword search differs from semantic search
- [ ] What an embedding is
- [ ] Why embeddings can represent meaning
- [ ] How cosine similarity measures relatedness
- [ ] The basic flow: text → embedding → similarity search
- [ ] How all phases connect

If any of these are unclear, re-read the relevant section before moving on.
