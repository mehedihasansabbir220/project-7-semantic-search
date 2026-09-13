"""
Semantic Search Engine
Builds a searchable index from documents and finds similar documents to queries.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict


class SemanticSearchEngine:
    """
    A semantic search engine that finds relevant documents based on meaning.

    Process:
    1. Load documents
    2. Generate embeddings for all documents (precomputed)
    3. Accept user query
    4. Generate embedding for query
    5. Calculate similarity between query and all documents
    6. Rank and return top-k results
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the semantic search engine.

        Args:
            model_name: Name of sentence transformer model to use
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"✓ Model loaded. Output dimensions: 384\n")

        # Storage for documents and embeddings
        self.documents = []
        self.embeddings = None
        self.is_indexed = False

    def index_documents(self, documents: List[Dict]) -> None:
        """
        Create embeddings for all documents and store them.

        Args:
            documents: List of document dictionaries with 'text' key

        Returns:
            None (modifies self.documents and self.embeddings)
        """
        print(f"Indexing {len(documents)} documents...")

        self.documents = documents

        # Extract text from each document
        texts = [doc["text"] for doc in documents]

        # Generate embeddings for all documents at once
        # This is efficient - all embeddings computed in parallel
        self.embeddings = self.model.encode(texts)

        print(f"✓ Generated {len(self.embeddings)} embeddings")
        print(f"✓ Shape: {self.embeddings.shape}")
        print(f"✓ Ready for searching\n")

        self.is_indexed = True

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for documents similar to the query.

        Process:
        1. Convert query to embedding
        2. Calculate similarity with all document embeddings
        3. Sort by similarity (highest first)
        4. Return top_k results

        Args:
            query: Search query (natural language text)
            top_k: Number of results to return (default: 5)

        Returns:
            List of dictionaries with results, ranked by similarity
        """

        # Verify documents are indexed
        if not self.is_indexed:
            raise RuntimeError("Documents not indexed yet. Call index_documents() first.")

        # Step 1: Convert query to embedding using same model
        query_embedding = self.model.encode(query)

        # Step 2: Calculate cosine similarity between query and all documents
        # reshape query for sklearn (needs 2D array)
        similarities = cosine_similarity(
            [query_embedding],
            self.embeddings
        )[0]

        # Step 3: Create result list with scores
        results = []
        for idx, doc in enumerate(self.documents):
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "category": doc["category"],
                "similarity_score": float(similarities[idx])
            })

        # Step 4: Sort by similarity score (highest first)
        results.sort(key=lambda x: x["similarity_score"], reverse=True)

        # Step 5: Return only top_k results
        return results[:top_k]

    def search_with_details(self, query: str, top_k: int = 5) -> tuple:
        """
        Search and return additional metadata for displaying results.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            Tuple of (query_embedding, results list, top_k)
        """
        query_embedding = self.model.encode(query)
        results = self.search(query, top_k)
        return query_embedding, results, top_k

    def get_document_embedding(self, doc_id: int) -> np.ndarray:
        """
        Get the embedding for a specific document.

        Args:
            doc_id: Document ID

        Returns:
            Embedding vector for that document
        """
        if not self.is_indexed:
            raise RuntimeError("Documents not indexed yet.")

        # Find document by id
        for idx, doc in enumerate(self.documents):
            if doc["id"] == doc_id:
                return self.embeddings[idx]

        raise ValueError(f"Document with id {doc_id} not found")

    def get_stats(self) -> Dict:
        """
        Get statistics about the indexed documents.

        Returns:
            Dictionary with stats
        """
        if not self.is_indexed:
            return {"indexed": False}

        return {
            "indexed": True,
            "num_documents": len(self.documents),
            "embedding_dimensions": self.embeddings.shape[1],
            "categories": list(set(doc["category"] for doc in self.documents))
        }


def print_search_results(query: str, results: List[Dict], top_k: int) -> None:
    """
    Pretty print search results.

    Args:
        query: Original search query
        results: List of result dictionaries
        top_k: Number of results to display
    """

    print("\n" + "=" * 100)
    print(f"SEARCH RESULTS FOR: \"{query}\"")
    print("=" * 100)

    if not results:
        print("No results found.")
        return

    for rank, result in enumerate(results, 1):
        # Color coding by similarity (visual indicator)
        score = result["similarity_score"]

        if score > 0.8:
            quality = "★★★★★ EXCELLENT"
        elif score > 0.6:
            quality = "★★★★☆ GOOD"
        elif score > 0.4:
            quality = "★★★☆☆ FAIR"
        else:
            quality = "★★☆☆☆ WEAK"

        print(f"\n[{rank}] {result['title']}")
        print(f"    Category: {result['category']}")
        print(f"    Similarity: {score:.4f} ({quality})")

        # Show preview of text (first 120 characters)
        preview = result["text"][:120].replace("\n", " ")
        if len(result["text"]) > 120:
            preview += "..."
        print(f"    Preview: {preview}")

    print("\n" + "=" * 100 + "\n")
