"""
Information Retrieval Metrics

Educational explanation of common search evaluation metrics.
"""

from typing import List, Set


def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Precision@K: What fraction of top-K results are actually relevant?

    BEGINNER-FRIENDLY EXPLANATION:
    =====================================
    Imagine you searched for "machine learning" and got 5 results.

    Real results (top-5):
    1. Machine Learning Basics     ✓ RELEVANT
    2. How to Cook Pasta           ✗ NOT relevant
    3. Deep Learning Guide         ✓ RELEVANT
    4. Shopping List               ✗ NOT relevant
    5. Neural Networks             ✓ RELEVANT

    Precision@5 = 3 relevant / 5 total = 0.60 (60%)

    MEANING:
    - 1.0 (100%): All results are relevant (perfect!)
    - 0.5 (50%):  Half the results are relevant
    - 0.0 (0%):   No results are relevant (worst)

    USE CASE:
    When you want high-quality results, precision matters.
    Example: Medical search (better to miss results than show wrong ones)

    Args:
        retrieved: List of chunk IDs returned by search (top-k order)
        relevant: Set of chunk IDs that are actually relevant
        k: How many top results to consider

    Returns:
        Precision@K score (0.0 to 1.0)
    """
    if k <= 0:
        return 0.0

    # Get only top-K results
    top_k_retrieved = retrieved[:k]

    # Count how many of top-K are relevant
    correct = sum(1 for chunk_id in top_k_retrieved if chunk_id in relevant)

    # Precision = correct / total retrieved
    return correct / k


def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Recall@K: What fraction of all relevant documents did we find?

    BEGINNER-FRIENDLY EXPLANATION:
    =====================================
    Imagine there are 5 documents total about "machine learning"
    and you search and get results ranked like this:

    All relevant documents (should find):
    1. Machine Learning Basics     ✓ Found (position 1)
    2. Deep Learning Guide         ✓ Found (position 3)
    3. Neural Networks             ✓ Found (position 5)
    4. PyTorch Tutorial            ✗ NOT found (missing)
    5. TensorFlow Guide            ✗ NOT found (missing)

    Looking at top-5 results:
    Recall@5 = 3 found / 5 total = 0.60 (60%)

    MEANING:
    - 1.0 (100%): Found all relevant results (perfect!)
    - 0.5 (50%):  Found half of all relevant results
    - 0.0 (0%):   Found none of the relevant results

    USE CASE:
    When you need comprehensive coverage, recall matters.
    Example: Legal search (better to see many results than miss important ones)

    Args:
        retrieved: List of chunk IDs returned by search
        relevant: Set of chunk IDs that are actually relevant
        k: How many top results to consider

    Returns:
        Recall@K score (0.0 to 1.0)
    """
    if not relevant or len(relevant) == 0:
        return 0.0

    # Get only top-K results
    top_k_retrieved = retrieved[:k]

    # Count how many of top-K are relevant
    found = sum(1 for chunk_id in top_k_retrieved if chunk_id in relevant)

    # Recall = found / total relevant
    return found / len(relevant)


def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
    """
    Mean Reciprocal Rank (MRR): How far down the list is the first relevant result?

    BEGINNER-FRIENDLY EXPLANATION:
    =====================================
    You search and get ranked results:
    1. Pizza Recipes              ✗ NOT relevant
    2. Cooking Techniques         ✗ NOT relevant
    3. Machine Learning Basics    ✓ RELEVANT! (first match)
    4. Deep Learning              ✓ RELEVANT
    5. Neural Networks            ✓ RELEVANT

    MRR = 1 / (position of first relevant result)
        = 1 / 3
        = 0.33

    MEANING:
    - 1.0: First result is relevant (best!)
    - 0.5: First relevant result is at position 2
    - 0.33: First relevant result is at position 3
    - 0.1: First relevant result is at position 10
    - 0.0: No relevant results found

    USE CASE:
    When users only check the top results.
    Example: Google search (users rarely go past page 1)

    Args:
        retrieved: List of chunk IDs returned by search
        relevant: Set of chunk IDs that are actually relevant

    Returns:
        MRR score (0.0 to 1.0)
    """
    for position, chunk_id in enumerate(retrieved, 1):
        if chunk_id in relevant:
            return 1.0 / position

    return 0.0


class EvaluationMetrics:
    """Calculate and display evaluation metrics"""

    @staticmethod
    def calculate_all(retrieved: List[str], relevant: Set[str]) -> dict:
        """
        Calculate all metrics for a single query.

        Args:
            retrieved: List of chunk IDs returned by search (ranked)
            relevant: Set of chunk IDs that are actually relevant

        Returns:
            Dict with all metrics
        """
        return {
            "precision@5": precision_at_k(retrieved, relevant, 5),
            "precision@10": precision_at_k(retrieved, relevant, 10),
            "recall@5": recall_at_k(retrieved, relevant, 5),
            "recall@10": recall_at_k(retrieved, relevant, 10),
            "mrr": mean_reciprocal_rank(retrieved, relevant),
        }

    @staticmethod
    def average_metrics(all_results: List[dict]) -> dict:
        """
        Calculate average metrics across multiple queries.

        Args:
            all_results: List of metric dicts from calculate_all()

        Returns:
            Dict with averaged metrics
        """
        if not all_results:
            return {}

        metrics = {}
        for key in all_results[0].keys():
            values = [r[key] for r in all_results]
            metrics[f"{key}_avg"] = sum(values) / len(values)

        return metrics

    @staticmethod
    def print_results(query: str, retrieved: List[str], relevant: Set[str]):
        """Pretty print results and metrics"""
        metrics = EvaluationMetrics.calculate_all(retrieved, relevant)

        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Expected relevant: {len(relevant)} | Retrieved top-10: {len(retrieved[:10])}")
        print(f"{'-'*60}")

        # Show which results were relevant
        for i, chunk_id in enumerate(retrieved[:10], 1):
            is_relevant = "✓" if chunk_id in relevant else "✗"
            print(f"  {i}. {chunk_id} {is_relevant}")

        print(f"{'-'*60}")
        print(f"Precision@5:  {metrics['precision@5']:.2f} (What % of top-5 are relevant?)")
        print(f"Recall@5:     {metrics['recall@5']:.2f} (Found what % of relevant docs?)")
        print(f"MRR:          {metrics['mrr']:.2f} (How far to first relevant?)")
        print(f"{'='*60}")


# Example and explanation
if __name__ == "__main__":
    print("""
METRICS EXPLAINED
=================

Precision@K
-----------
Question: "Are the results GOOD?"
Answer: What fraction of top-K results are relevant?

If you return 5 results and 3 are relevant:
Precision@5 = 3/5 = 0.60 = 60%

Use when: You want to avoid showing wrong results
Example: Medical search (precision matters more than completeness)

---

Recall@K
---------
Question: "Did we find EVERYTHING?"
Answer: What fraction of all relevant documents did we find?

If there are 10 relevant documents and you found 7 in top-10:
Recall@10 = 7/10 = 0.70 = 70%

Use when: You want comprehensive coverage
Example: Legal search (need to find all relevant cases)

---

Precision vs Recall Trade-off
-----------------------------
More Precision = Fewer, higher-quality results
More Recall = More results, but some might be irrelevant

Semantic search usually better at:
  ✓ Understanding meaning
  ✓ Handling synonyms/paraphrases
  ✓ Better recall on ambiguous queries

Keyword search better at:
  ✓ Finding exact technical terms
  ✓ Better precision on specific queries
  ✗ Understanding natural language
    """)

    # Example
    print("\nEXAMPLE CALCULATION")
    print("==================")

    retrieved = ["doc_001", "doc_002", "doc_003", "doc_004", "doc_005"]
    relevant = {"doc_001", "doc_003", "doc_005"}

    print(f"Retrieved: {retrieved}")
    print(f"Relevant: {relevant}")
    print()

    EvaluationMetrics.print_results(
        query="test query",
        retrieved=retrieved,
        relevant=relevant
    )
