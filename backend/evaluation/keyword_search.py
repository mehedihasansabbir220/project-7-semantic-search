"""
Simple Keyword Search Implementation

For comparison with semantic search.
Uses basic TF-IDF concept: frequency of query terms in documents.
"""

from typing import List, Dict
import re
from collections import Counter


class KeywordSearcher:
    """
    Simple keyword-based search engine.

    HOW IT WORKS:
    1. Split query into words
    2. Search for exact word matches in documents
    3. Score by number of matching words
    4. Return highest-scoring results

    LIMITATIONS:
    ❌ Doesn't understand synonyms (cat ≠ feline)
    ❌ Doesn't handle paraphrases (learns from ≠ understands)
    ❌ Doesn't recognize related concepts
    ❌ Sensitive to exact spelling/capitalization
    """

    def __init__(self, documents: Dict[str, str]):
        """
        Initialize with documents.

        Args:
            documents: Dict of {chunk_id: text}
        """
        self.documents = documents
        self.inverted_index = self._build_index()

    def _build_index(self) -> Dict[str, List[str]]:
        """
        Build inverted index: word → list of chunks containing it

        Process:
        1. For each document
        2. Split into words
        3. Map each word to document IDs
        """
        index = {}

        for chunk_id, text in self.documents.items():
            # Extract words (lowercase, remove punctuation)
            words = self._tokenize(text)

            for word in set(words):  # Use set to avoid duplicates
                if word not in index:
                    index[word] = []
                index[word].append(chunk_id)

        return index

    def _tokenize(self, text: str) -> List[str]:
        """
        Split text into words.

        Process:
        1. Convert to lowercase
        2. Remove punctuation
        3. Split by whitespace
        4. Remove short words (< 3 chars)
        """
        # Convert to lowercase
        text = text.lower()

        # Remove punctuation (keep alphanumeric and spaces)
        text = re.sub(r'[^a-z0-9\s]', '', text)

        # Split into words
        words = text.split()

        # Remove short words (noise like 'a', 'the', 'is')
        words = [w for w in words if len(w) >= 3]

        return words

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for documents matching query keywords.

        Args:
            query: Search query text
            top_k: Number of results to return

        Returns:
            List of results: {chunk_id, score, text}

        SCORING:
        - Score = number of matching query words
        - Higher score = more query terms present
        - Example:
          Query: "machine learning algorithms"
          Doc with all 3 words: score = 3
          Doc with 2 words: score = 2
          Doc with 0 words: score = 0
        """
        query_words = self._tokenize(query)

        if not query_words:
            return []

        # Count matching words for each document
        scores = {}

        for word in query_words:
            # Find chunks containing this word
            if word in self.inverted_index:
                for chunk_id in self.inverted_index[word]:
                    scores[chunk_id] = scores.get(chunk_id, 0) + 1

        # Sort by score (descending)
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Format results
        results = []
        for chunk_id, score in sorted_results[:top_k]:
            results.append({
                "chunk_id": chunk_id,
                "score": score / len(query_words),  # Normalize by query length
                "text": self.documents.get(chunk_id, "")[:100] + "...",
                "matching_words": score
            })

        return results

    def explain_score(self, query: str, chunk_id: str) -> Dict:
        """
        Explain why a document was ranked for a query.

        Returns what words matched.
        """
        query_words = set(self._tokenize(query))
        doc_words = set(self._tokenize(self.documents.get(chunk_id, "")))

        matching = query_words & doc_words  # Intersection
        missing = query_words - doc_words   # In query but not doc

        return {
            "matching_words": list(matching),
            "missing_words": list(missing),
            "match_count": len(matching),
            "coverage": len(matching) / len(query_words) if query_words else 0
        }


# Example usage
if __name__ == "__main__":
    # Sample documents
    docs = {
        "doc_001": "Machine learning algorithms for data analysis",
        "doc_002": "Deep learning neural networks",
        "doc_003": "Natural language processing with transformers",
    }

    # Create searcher
    searcher = KeywordSearcher(docs)

    # Test query
    query = "machine learning algorithms"
    results = searcher.search(query, top_k=3)

    print(f"Query: {query}")
    print(f"Results:")
    for result in results:
        print(f"  - {result['chunk_id']}: score={result['score']:.2f}")
        explanation = searcher.explain_score(query, result['chunk_id'])
        print(f"    Matched: {explanation['matching_words']}")
        print(f"    Missing: {explanation['missing_words']}")
