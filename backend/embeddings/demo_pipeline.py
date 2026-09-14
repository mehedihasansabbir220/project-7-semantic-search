"""
Demo: Document Ingestion and Chunking Pipeline

This is a DEMONSTRATION version that shows the complete pipeline
without requiring sentence-transformers or numpy.

It uses SIMULATED embeddings so you can understand the flow and structure.
For real embeddings, use index_documents.py

WHAT THIS SHOWS:
  1. How documents are loaded
  2. How they are chunked
  3. How metadata is tracked
  4. How chunks are indexed
  5. How chunk size affects results
"""

import sys
import os
from pathlib import Path
import random
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from ingestion.loader import DocumentLoader
from ingestion.chunker import DocumentChunker, print_chunk_stats


def simulate_embeddings(texts):
    """
    SIMULATION: Generate fake embeddings based on text properties.

    In real world:
      text → sentence-transformers model → 384-dimensional vector

    For this demo:
      We create embeddings based on simple text properties
      (This is NOT how real embeddings work, just for demonstration)
    """
    embeddings = []

    for text in texts:
        # Fake embedding: deterministic based on text hash
        random.seed(hash(text) % (2**31))
        embedding = [random.gauss(0, 1) for _ in range(384)]

        # Normalize
        norm = math.sqrt(sum(x**2 for x in embedding))
        embedding = [x / norm if norm > 0 else 0 for x in embedding]

        embeddings.append(embedding)

    return embeddings


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(x**2 for x in vec1))
    norm2 = math.sqrt(sum(x**2 for x in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


class LocalChunkIndex:
    """A simple local index for chunks and embeddings."""

    def __init__(self):
        self.chunks = {}
        self.embeddings = {}

    def add_chunk(self, chunk, embedding):
        self.chunks[chunk.chunk_id] = chunk
        self.embeddings[chunk.chunk_id] = embedding

    def get_chunk(self, chunk_id: str):
        return self.chunks.get(chunk_id)

    def get_embedding(self, chunk_id: str):
        return self.embeddings.get(chunk_id)

    def size(self) -> int:
        return len(self.chunks)

    def search(self, query_embedding, top_k=5):
        """Search index using cosine similarity."""
        if self.size() == 0:
            return []

        # Compute similarity for all chunks
        similarities = []
        for chunk_id, embedding in self.embeddings.items():
            sim = cosine_similarity(query_embedding, embedding)
            chunk = self.chunks[chunk_id]
            similarities.append((chunk_id, sim, chunk))

        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top-k
        results = []
        for chunk_id, score, chunk in similarities[:top_k]:
            text_preview = chunk.text[:100] + "..." if len(chunk.text) > 100 else chunk.text
            results.append({
                "chunk_id": chunk_id,
                "score": float(score),
                "text": text_preview,
                "document": chunk.document_id,
                "position": chunk.start_position
            })

        return results


def print_demo_banner():
    """Print welcome banner."""
    print("\n" + "=" * 100)
    print(" " * 30 + "DOCUMENT PIPELINE DEMONSTRATION")
    print("=" * 100)
    print("""
This demo shows the complete document ingestion pipeline:

1. LOAD:   Documents (.txt files)
2. CHUNK:  Split into smaller pieces
3. INDEX:  Create embeddings and index
4. SEARCH: Query semantic similarity

IMPORTANT: This uses SIMULATED embeddings for demonstration.
For production, use index_documents.py with real embeddings.
""")
    print("=" * 100 + "\n")


def demo_basic_pipeline():
    """Show the basic pipeline in action."""
    print("[DEMO 1] Basic Pipeline - Load, Chunk, Index")
    print("-" * 100)

    documents_dir = Path(__file__).parent.parent / "data" / "sample_documents"

    # Step 1: Load
    print("\n1️⃣  LOADING DOCUMENTS...")
    loader = DocumentLoader(str(documents_dir))
    documents = loader.load_documents()

    if not documents:
        print("❌ No documents found!")
        return None

    print(f"✓ Loaded {len(documents)} documents\n")

    for doc in documents:
        print(f"  • {doc.document_id}: {doc.filename}")
        print(f"    Size: {len(doc.text):,} characters")
        print()

    # Step 2: Chunk
    print("\n2️⃣  CHUNKING DOCUMENTS...")
    chunker = DocumentChunker(chunk_size=300, overlap=50)
    chunks = chunker.chunk_documents(documents)

    print(f"✓ Created {len(chunks)} chunks\n")
    print_chunk_stats(chunks)

    # Step 3: Generate embeddings (simulated)
    print("\n3️⃣  GENERATING EMBEDDINGS (SIMULATED)...")
    chunk_texts = [chunk.text for chunk in chunks]
    embeddings = simulate_embeddings(chunk_texts)

    print(f"✓ Generated {len(embeddings)} simulated embeddings")
    print(f"✓ Embedding dimension: 384\n")

    # Step 4: Index
    print("\n4️⃣  BUILDING INDEX...")
    index = LocalChunkIndex()

    for chunk, embedding in zip(chunks, embeddings):
        index.add_chunk(chunk, embedding)

    print(f"✓ Indexed {index.size()} chunks\n")

    return index, documents


def demo_chunk_size_effect():
    """Show how chunk size affects the pipeline."""
    print("\n" + "=" * 100)
    print("[DEMO 2] Chunk Size Effect")
    print("=" * 100)

    documents_dir = Path(__file__).parent.parent / "data" / "sample_documents"

    loader = DocumentLoader(str(documents_dir))
    documents = loader.load_documents()

    if not documents:
        print("❌ No documents found!")
        return

    print("\nTesting different chunk sizes on the same documents...\n")

    configurations = [
        {"name": "Small", "chunk_size": 100, "overlap": 20},
        {"name": "Medium", "chunk_size": 300, "overlap": 50},
        {"name": "Large", "chunk_size": 500, "overlap": 100},
    ]

    results = []

    for config in configurations:
        print(f"\n{config['name'].upper()} CHUNKS:")
        print(f"  Chunk size: {config['chunk_size']} chars")
        print(f"  Overlap: {config['overlap']} chars")
        print(f"  Step size: {config['chunk_size'] - config['overlap']} chars")
        print("-" * 50)

        chunker = DocumentChunker(
            chunk_size=config['chunk_size'],
            overlap=config['overlap']
        )
        chunks = chunker.chunk_documents(documents)

        # Analyze
        total_chars = sum(len(c.text) for c in chunks)
        avg_size = total_chars / len(chunks) if chunks else 0

        print(f"  Total chunks: {len(chunks)}")
        print(f"  Total chars: {total_chars:,}")
        print(f"  Avg chunk size: {avg_size:.1f} chars")

        results.append({
            "name": config["name"],
            "chunk_count": len(chunks),
            "avg_size": avg_size
        })

    # Summary
    print("\n" + "=" * 100)
    print("SUMMARY: Chunk Size Comparison")
    print("=" * 100)

    print(f"\n{'Configuration':<12} {'Total Chunks':<15} {'Avg Size':<15}")
    print("-" * 50)
    for r in results:
        print(f"{r['name']:<12} {r['chunk_count']:<15} {r['avg_size']:<15.1f}")

    print("\n" + "=" * 100)
    print("INSIGHTS:")
    print("=" * 100)
    print("""
1. GRANULARITY:
   Smaller chunks → More granular, finds specific concepts
   Larger chunks → Broader scope, includes more context

2. CHUNK COUNT:
   Small chunks create MORE total chunks
   Large chunks create FEWER total chunks
   (More chunks = more storage, more comparisons in search)

3. OVERLAP BENEFIT:
   Without overlap: Sentences split at boundaries
   With overlap: Context preserved across chunk boundaries
   Example with 50-char overlap:
     Last 50 chars of Chunk 1 = First 50 chars of Chunk 2

4. PRODUCTION CHOICE:
   Most systems use 300-500 characters per chunk
   Overlap: 50-150 characters
   This balances granularity, context, and search performance

5. YOUR TASK:
   Experiment with sizes on your own data
   Observe which size gives best search results for your use case
""")

    print("=" * 100 + "\n")


def demo_search(index, documents):
    """Demonstrate search functionality."""
    print("\n" + "=" * 100)
    print("[DEMO 3] Semantic Search Example")
    print("=" * 100)

    if index is None or index.size() == 0:
        print("❌ Index is empty!")
        return

    # Test queries
    test_queries = [
        "machine learning algorithms",
        "deep neural networks",
        "natural language processing",
        "transformer models",
    ]

    print(f"\nSearching across {index.size()} indexed chunks...\n")

    for query in test_queries:
        print(f"\n📝 Query: \"{query}\"")
        print("-" * 100)

        # Generate query embedding (simulated)
        query_embedding = simulate_embeddings([query])[0]

        # Search
        results = index.search(query_embedding, top_k=3)

        # Display results
        for i, result in enumerate(results, 1):
            print(f"\n  [{i}] Match Score: {result['score']:.4f}")
            print(f"      Chunk: {result['chunk_id']}")
            print(f"      Document: {result['document']}")
            print(f"      Text: {result['text']}")

    print("\n" + "=" * 100 + "\n")


def main():
    """Run all demonstrations."""
    print_demo_banner()

    # Demo 1: Basic pipeline
    result = demo_basic_pipeline()
    if result:
        index, documents = result
    else:
        print("Failed to load documents. Exiting.")
        return

    # Demo 2: Chunk size effect
    demo_chunk_size_effect()

    # Demo 3: Search
    demo_search(index, documents)

    # Final notes
    print("=" * 100)
    print("NEXT STEPS")
    print("=" * 100)
    print("""
Now that you understand the pipeline structure:

1. REAL EMBEDDINGS:
   Run: python backend/embeddings/index_documents.py
   (After installing: pip install -r backend/requirements.txt)
   This generates REAL embeddings using sentence-transformers

2. MODIFY SAMPLES:
   Add your own .txt files to backend/data/sample_documents/
   The pipeline will automatically process them

3. EXPERIMENT:
   Change chunk_size and overlap values
   Observe how search results change

4. SCALE UP:
   Process larger documents and see performance impact
   Monitor memory usage with larger indexes

PRODUCTION CONSIDERATIONS:
  • Use vector databases (Pinecone, Weaviate) for scale
  • Implement streaming for memory efficiency
  • Add filtering and metadata search
  • Use GPU for faster embedding generation
""")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
