"""
SearchService - Business logic for semantic search.

This module handles all semantic search operations:
- Loading the embedding model
- Building the search index
- Executing searches
- Computing similarity scores

SEPARATION OF CONCERNS:
This service is INDEPENDENT of FastAPI/HTTP concerns.
It can be used by API routes, CLI tools, or other interfaces.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from sentence_transformers import SentenceTransformer
from ingestion.loader import DocumentLoader
from ingestion.chunker import DocumentChunker


class SearchService:
    """
    Semantic search service.

    Features:
    - Load and cache embedding model (avoid reloading)
    - Build search index from documents
    - Execute semantic searches
    - Rank results by similarity
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the search service.

        Args:
            model_name: SentenceTransformer model to use
        """
        self.model_name = model_name
        self.model = None
        self.index = {}  # chunk_id → chunk data
        self.embeddings = {}  # chunk_id → embedding vector
        self.chunk_ids = []  # ordered list of chunk IDs

    def load_model(self):
        """
        Load the embedding model lazily (only when needed).

        WHY LAZY LOADING?
        - Models are large (~200MB)
        - Loading takes time (~5 seconds)
        - Only load if we'll actually use it
        - Avoids unnecessary overhead in testing
        """
        if self.model is not None:
            return  # Already loaded

        print(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print(f"✓ Model loaded: {self.model_name}")

    def build_index(self, documents_dir: str,
                    chunk_size: int = 300,
                    overlap: int = 50) -> int:
        """
        Build the search index from documents.

        Process:
        1. Load all .txt files from directory
        2. Chunk documents with overlap
        3. Generate embeddings for each chunk
        4. Store in index

        Args:
            documents_dir: Path to documents directory
            chunk_size: Characters per chunk
            overlap: Overlap between chunks

        Returns:
            Number of chunks indexed
        """
        print(f"\n[1/3] Loading documents from {documents_dir}...")

        loader = DocumentLoader(documents_dir)
        documents = loader.load_documents()

        if not documents:
            raise ValueError(f"No documents found in {documents_dir}")

        print(f"✓ Loaded {len(documents)} documents\n")

        print(f"[2/3] Chunking documents (size={chunk_size}, overlap={overlap})...")

        chunker = DocumentChunker(chunk_size=chunk_size, overlap=overlap)
        chunks = chunker.chunk_documents(documents)

        print(f"✓ Created {len(chunks)} chunks\n")

        print(f"[3/3] Generating embeddings...")

        # Load model for embedding
        self.load_model()

        # Generate embeddings
        chunk_texts = [chunk.text for chunk in chunks]
        embeddings = self.model.encode(chunk_texts, show_progress_bar=True)

        print(f"✓ Generated {len(embeddings)} embeddings\n")

        # Build index
        print("Building index...")
        for chunk, embedding in zip(chunks, embeddings):
            self.index[chunk.chunk_id] = {
                "text": chunk.text,
                "document_id": chunk.document_id,
                "filename": chunk.metadata.get("filename", "unknown"),
                "position": chunk.start_position,
                "chunk_index": chunk.chunk_index,
            }
            self.embeddings[chunk.chunk_id] = embedding
            self.chunk_ids.append(chunk.chunk_id)

        print(f"✓ Index built: {len(self.index)} chunks ready for search\n")

        return len(self.index)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Execute a semantic search.

        Process:
        1. Encode query to embedding
        2. Compute similarity with all chunk embeddings
        3. Rank by similarity score
        4. Return top-k results

        Args:
            query: Search query text
            top_k: Number of results to return

        Returns:
            List of search results with metadata

        Raises:
            ValueError: If index is empty or model not loaded
        """
        if not self.index:
            raise ValueError("Index is empty. Call build_index() first.")

        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        # Encode query
        query_embedding = self.model.encode([query])[0]

        # Compute similarities
        similarities = []
        for chunk_id in self.chunk_ids:
            embedding = self.embeddings[chunk_id]
            score = self._cosine_similarity(query_embedding, embedding)
            similarities.append((chunk_id, score))

        # Sort by score (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Get top-k results
        results = []
        for chunk_id, score in similarities[:top_k]:
            chunk_data = self.index[chunk_id]

            # Truncate text for API response
            text_preview = chunk_data["text"]
            if len(text_preview) > 200:
                text_preview = text_preview[:200] + "..."

            results.append({
                "chunk_id": chunk_id,
                "document_id": chunk_data["document_id"],
                "score": float(score),
                "text": text_preview,
                "filename": chunk_data["filename"],
            })

        return results

    @staticmethod
    def _cosine_similarity(vec1, vec2) -> float:
        """
        Compute cosine similarity between two vectors.

        Formula: cos(θ) = (A·B) / (|A| × |B|)

        Range: 0.0 to 1.0 (normalized)
        - 1.0 = identical vectors
        - 0.0 = orthogonal (no similarity)

        Args:
            vec1: First vector (list of floats)
            vec2: Second vector (list of floats)

        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # Magnitudes
        mag1 = math.sqrt(sum(x**2 for x in vec1))
        mag2 = math.sqrt(sum(x**2 for x in vec2))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def get_stats(self) -> Dict:
        """
        Get service statistics.

        Returns:
            Dictionary with service metrics
        """
        return {
            "model_loaded": self.model is not None,
            "model_name": self.model_name,
            "chunks_indexed": len(self.index),
            "embedding_dimension": 384,
        }


# Global service instance (singleton pattern)
# This ensures we load the model only once
_search_service = None


def get_search_service() -> SearchService:
    """
    Get or create the global search service instance.

    WHY SINGLETON?
    - Embedding model is large and takes time to load
    - Don't want to reload it for every request
    - One instance serves all requests
    - Thread-safe (FastAPI handles this)

    Returns:
        SearchService instance
    """
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service


def initialize_search_service(documents_dir: str):
    """
    Initialize the global search service with an index.

    Call this once at application startup.

    Args:
        documents_dir: Path to documents directory
    """
    service = get_search_service()
    service.load_model()
    service.build_index(documents_dir)
    print(f"\n✓ Search service initialized with {service.get_stats()['chunks_indexed']} chunks")
