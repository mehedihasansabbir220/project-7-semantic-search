"""
Complete Document Ingestion and Indexing Pipeline

This script demonstrates the full pipeline:
  1. Load text documents from files
  2. Chunk documents into smaller pieces
  3. Generate embeddings for each chunk
  4. Build a searchable local index

PIPELINE OVERVIEW
=================

Document         A file containing text we want to search (e.g., paper.txt)
    ↓
Loader           Reads files and creates Document objects
    ↓
Chunk            Splits documents into smaller, embeddable pieces
    ↓
Chunk Embedding  Converts each chunk to a 384-dimensional vector
    ↓
Local Index      Dictionary mapping chunk_id → (embedding, chunk_text, metadata)
    ↓
Search Ready!    Query embeddings are compared with chunk embeddings

KEY CONCEPTS
============

Document:  The original text file. Too large to embed as one vector.
           Example: A 10,000-word research paper.

Chunk:     A piece of a document (e.g., 300 characters).
           Each chunk gets its own embedding.
           Example: 3 paragraphs from a research paper.

Embedding: A 384-dimensional vector representing a chunk's meaning.
           Similar chunks have similar embeddings (close vectors).
           Generated using sentence-transformers model.

Vector:    A list of numbers (the embedding).
           Cosine similarity compares vectors to find matches.

Metadata:  Additional information about a chunk.
           - Which document it came from
           - Its position in the document
           - The chunk's character range

Indexing:  Building a data structure that enables fast search.
           Maps chunk_id → (embedding, text, metadata)
           In this version: a simple dictionary (local index)
           In production: databases like Pinecone, Weaviate, Milvus

WHY CHUNKS?
===========

Embeddings have token limits (usually 512-2048 tokens).
A 100-page document exceeds this limit when encoded as one chunk.
Solution: Split the document into overlapping chunks.

Without chunks:
  Large Doc (too big) → Can't embed → Can't search

With chunks:
  Large Doc → Split into 50 chunks → Each embeddable → Searchable

CHUNK OVERLAP
=============

Overlap prevents important information from being split across boundaries.

No overlap (chunk_size=300):
  Chunk 1: chars 0-300
  Chunk 2: chars 300-600
  ✗ Problem: A sentence split at boundary loses context

With overlap (chunk_size=300, overlap=50):
  Chunk 1: chars 0-300
  Chunk 2: chars 250-550      (50 chars overlap)
  Chunk 3: chars 500-800      (50 chars overlap)
  ✓ Better: Context preserved at boundaries
  ✓ Search might match multiple overlapping chunks

WHY LOCAL INDEXING?
===================

This project keeps everything local (no cloud vector DBs):
  • Data privacy: Nothing leaves your machine
  • No API costs: No external service calls
  • For learning: See how search fundamentals work
  • Suitable for: Small to medium datasets (<10M chunks)

Production systems use vector databases:
  • Pinecone: Fully managed vector DB
  • Weaviate: Open-source vector DB
  • Milvus: Scalable open-source vector DB
  • FAISS: Facebook's similarity search library
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import Dict, List

from ingestion.loader import DocumentLoader
from ingestion.chunker import DocumentChunker, print_chunk_stats


class LocalChunkIndex:
    """
    A simple local index that stores chunk embeddings in memory.
    Maps chunk_id → (embedding, chunk_text, metadata)
    """

    def __init__(self):
        self.chunks = {}  # chunk_id → chunk object
        self.embeddings = {}  # chunk_id → embedding vector

    def add_chunk(self, chunk, embedding):
        """Add a chunk and its embedding to the index."""
        self.chunks[chunk.chunk_id] = chunk
        self.embeddings[chunk.chunk_id] = embedding

    def get_chunk(self, chunk_id: str):
        """Retrieve a chunk by ID."""
        return self.chunks.get(chunk_id)

    def get_embedding(self, chunk_id: str):
        """Retrieve an embedding by chunk ID."""
        return self.embeddings.get(chunk_id)

    def get_all_embeddings(self) -> np.ndarray:
        """Return all embeddings as a matrix."""
        chunk_ids = sorted(self.chunks.keys())
        embeddings_list = [self.embeddings[cid] for cid in chunk_ids]
        return np.array(embeddings_list), chunk_ids

    def size(self) -> int:
        """Return number of indexed chunks."""
        return len(self.chunks)

    def save(self, filepath: str):
        """Save index to disk (simplified - embeddings only)."""
        data = {
            "chunks": {
                cid: {
                    "text": chunk.text,
                    "document_id": chunk.document_id,
                    "metadata": chunk.metadata,
                }
                for cid, chunk in self.chunks.items()
            },
            "embeddings": {
                cid: embedding.tolist()
                for cid, embedding in self.embeddings.items()
            }
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✓ Index saved to {filepath}")


def build_index(
    documents_dir: str,
    chunk_size: int = 300,
    overlap: int = 50,
    model_name: str = "all-MiniLM-L6-v2"
) -> LocalChunkIndex:
    """
    Build a complete index from documents.

    Args:
        documents_dir: Path to directory with .txt files
        chunk_size: Characters per chunk
        overlap: Overlapping characters between chunks
        model_name: Sentence transformer model

    Returns:
        LocalChunkIndex object
    """

    print("\n" + "=" * 100)
    print("DOCUMENT INGESTION AND INDEXING PIPELINE")
    print("=" * 100)

    # Step 1: Load documents
    print("\n[STEP 1] Loading Documents")
    print("-" * 100)
    loader = DocumentLoader(documents_dir)
    documents = loader.load_documents()

    if not documents:
        raise ValueError(f"No documents found in {documents_dir}")

    print(f"✓ Loaded {len(documents)} documents\n")

    # Step 2: Chunk documents
    print("[STEP 2] Chunking Documents")
    print(f"Chunk size: {chunk_size} chars, Overlap: {overlap} chars")
    print("-" * 100)
    chunker = DocumentChunker(chunk_size=chunk_size, overlap=overlap)
    chunks = chunker.chunk_documents(documents)

    print(f"✓ Created {len(chunks)} chunks\n")
    print_chunk_stats(chunks)

    # Step 3: Load embedding model
    print("[STEP 3] Loading Embedding Model")
    print("-" * 100)
    print(f"Model: {model_name}")
    print("Downloading (may take a moment on first run)...")

    model = SentenceTransformer(model_name)
    print(f"✓ Model loaded: {model_name}")
    print(f"✓ Embedding dimension: 384\n")

    # Step 4: Generate embeddings
    print("[STEP 4] Generating Embeddings")
    print("-" * 100)
    print(f"Embedding {len(chunks)} chunks...")

    chunk_texts = [chunk.text for chunk in chunks]
    embeddings = model.encode(chunk_texts, show_progress_bar=True)

    print(f"✓ Generated {len(embeddings)} embeddings")
    print(f"✓ Shape: {embeddings.shape}\n")

    # Step 5: Build index
    print("[STEP 5] Building Index")
    print("-" * 100)

    index = LocalChunkIndex()

    for chunk, embedding in zip(chunks, embeddings):
        index.add_chunk(chunk, embedding)

    print(f"✓ Index contains {index.size()} chunks\n")

    print("=" * 100)
    print("INDEXING COMPLETE!")
    print("=" * 100)
    print(f"\nYour data is ready for semantic search.")
    print(f"Total indexed chunks: {index.size()}")
    print(f"Embedding dimensions: 384")
    print(f"Index type: Local (in-memory dictionary)\n")

    return index


def print_sample_chunks(index: LocalChunkIndex, num_samples: int = 3):
    """Print sample chunks from the index."""
    print("=" * 100)
    print("SAMPLE CHUNKS FROM INDEX")
    print("=" * 100)

    chunk_ids = list(index.chunks.keys())[:num_samples]

    for i, chunk_id in enumerate(chunk_ids, 1):
        chunk = index.chunks[chunk_id]

        print(f"\n[Chunk {i}]")
        print(f"  ID: {chunk_id}")
        print(f"  Document: {chunk.document_id}")
        print(f"  Position: chars {chunk.start_position}-{chunk.end_position}")
        print(f"  Size: {len(chunk.text)} characters")
        print(f"  Text preview: {chunk.text[:100]}...")
        print()

    print("=" * 100 + "\n")


def experiment_chunk_size_effect():
    """
    Experiment: How does chunk size affect search results?

    This demonstrates why chunking strategy matters.
    """
    print("\n" + "=" * 100)
    print("EXPERIMENT: CHUNK SIZE EFFECT ON SEARCH")
    print("=" * 100)
    print("""
This experiment shows how chunk size affects search results.

Question: If we change chunk size, do we get different search results?

Hypothesis: Smaller chunks are more granular but may lack context.
            Larger chunks have more context but fewer total chunks.

Test: Index the same documents with different chunk sizes and observe:
  1. How many chunks are created
  2. Sample chunk contents
  3. How chunk overlap affects results

Let's try two configurations:
""")

    documents_dir = Path(__file__).parent.parent / "data" / "sample_documents"

    # Configuration 1: Small chunks
    print("\n" + "-" * 100)
    print("CONFIGURATION A: Small chunks (100 chars, 20 char overlap)")
    print("-" * 100)

    index_small = build_index(
        str(documents_dir),
        chunk_size=100,
        overlap=20,
    )

    # Configuration 2: Large chunks
    print("\n" + "-" * 100)
    print("CONFIGURATION B: Large chunks (500 chars, 50 char overlap)")
    print("-" * 100)

    index_large = build_index(
        str(documents_dir),
        chunk_size=500,
        overlap=50,
    )

    # Compare
    print("\n" + "=" * 100)
    print("COMPARISON: Small vs. Large Chunks")
    print("=" * 100)

    print(f"\nSmall chunks (100 chars):")
    print(f"  Total chunks: {index_small.size()}")
    print(f"  Pros: More granular, finds specific concepts")
    print(f"  Cons: Less context, may lose surrounding meaning")

    print(f"\nLarge chunks (500 chars):")
    print(f"  Total chunks: {index_large.size()}")
    print(f"  Pros: More context, keeps paragraphs together")
    print(f"  Cons: Fewer chunks, may match less-relevant material")

    print(f"\nRatio: {index_small.size() / index_large.size():.1f}x more chunks with small size")

    print("\n" + "=" * 100)
    print("INSIGHTS")
    print("=" * 100)
    print("""
Why chunk size matters for search:

1. GRANULARITY:
   Small chunks (100 chars): Search finds precise, specific concepts
   Large chunks (500 chars): Search finds broader topics

2. RECALL vs. PRECISION:
   Small chunks: Higher recall (find more relevant chunks)
   Large chunks: Higher precision (fewer false positives)

3. OVERLAP BENEFITS:
   With overlap, context is preserved across chunk boundaries
   Query matching one chunk often matches overlapping chunk too
   This improves result quality

4. PRODUCTION CHOICE:
   Typical production systems use: 300-500 character chunks with 50-100 char overlap
   Balances granularity, context, and search performance

5. EXPERIMENT FURTHER:
   Try different chunk sizes on your own data
   Observe which size gives best search results for your use case
   There's no one-size-fits-all answer!
""")

    print("=" * 100 + "\n")

    return index_small, index_large


if __name__ == "__main__":
    # Option 1: Build index once
    print("\n🚀 Starting document ingestion pipeline...\n")

    documents_dir = Path(__file__).parent.parent / "data" / "sample_documents"

    try:
        index = build_index(
            str(documents_dir),
            chunk_size=300,
            overlap=50,
        )

        # Show some samples
        print_sample_chunks(index, num_samples=5)

        # Save index for later use
        index_path = Path(__file__).parent / "local_index.json"
        index.save(str(index_path))

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    # Option 2: Run the chunk size experiment
    print("\nWould you like to run the chunk size experiment? (uncomment below)")
    # Uncomment to run:
    # index_small, index_large = experiment_chunk_size_effect()

    print("✅ Pipeline complete! Index ready for semantic search.\n")
