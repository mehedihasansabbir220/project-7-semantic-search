"""
Compare Semantic vs Keyword Search

Evaluates both approaches on test queries and displays results.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluation.dataset import EVALUATION_QUERIES, DOCUMENT_SNIPPETS
from evaluation.keyword_search import KeywordSearcher
from evaluation.metrics import EvaluationMetrics, precision_at_k, recall_at_k
from services.search_service import SearchService, get_search_service


class SearchComparison:
    """Compare semantic and keyword search approaches"""

    def __init__(self, semantic_service: SearchService):
        """
        Initialize comparison.

        Args:
            semantic_service: Initialized semantic search service
        """
        self.semantic_service = semantic_service
        self.keyword_searcher = KeywordSearcher(DOCUMENT_SNIPPETS)
        self.results = []

    def compare_query(self, query_idx: int) -> dict:
        """
        Compare both approaches for a single query.

        Args:
            query_idx: Index in EVALUATION_QUERIES

        Returns:
            Results dict with both approaches
        """
        query_data = EVALUATION_QUERIES[query_idx]
        query_text = query_data["query"]
        expected = set(query_data["expected_chunks"])

        print(f"\n{'='*70}")
        print(f"Query {query_idx + 1}: \"{query_text}\"")
        print(f"Category: {query_data['category']}")
        print(f"Expected relevant: {', '.join(expected)}")
        print(f"{'='*70}")

        # KEYWORD SEARCH
        print(f"\n📝 KEYWORD SEARCH")
        print(f"{'-'*70}")

        keyword_results = self.keyword_searcher.search(query_text, top_k=5)
        keyword_ids = [r["chunk_id"] for r in keyword_results]

        for i, result in enumerate(keyword_results, 1):
            is_relevant = "✓" if result["chunk_id"] in expected else "✗"
            print(f"  {i}. {result['chunk_id']} (score: {result['score']:.2f}) {is_relevant}")
            print(f"     {DOCUMENT_SNIPPETS.get(result['chunk_id'], '')[:60]}...")
            explain = self.keyword_searcher.explain_score(query_text, result["chunk_id"])
            print(f"     Matched: {explain['matching_words']}")

        keyword_metrics = EvaluationMetrics.calculate_all(keyword_ids, expected)
        print(f"  Precision@5: {keyword_metrics['precision@5']:.2f}")
        print(f"  Recall@5: {keyword_metrics['recall@5']:.2f}")

        # SEMANTIC SEARCH
        print(f"\n🧠 SEMANTIC SEARCH")
        print(f"{'-'*70}")

        semantic_results = self.semantic_service.search(query_text, top_k=5)
        semantic_ids = [r["chunk_id"] for r in semantic_results]

        for i, result in enumerate(semantic_results, 1):
            is_relevant = "✓" if result["chunk_id"] in expected else "✗"
            print(f"  {i}. {result['chunk_id']} (score: {result['score']:.3f}) {is_relevant}")
            print(f"     {DOCUMENT_SNIPPETS.get(result['chunk_id'], '')[:60]}...")

        semantic_metrics = EvaluationMetrics.calculate_all(semantic_ids, expected)
        print(f"  Precision@5: {semantic_metrics['precision@5']:.2f}")
        print(f"  Recall@5: {semantic_metrics['recall@5']:.2f}")

        # COMPARISON
        print(f"\n⚖️  COMPARISON")
        print(f"{'-'*70}")

        if keyword_metrics['precision@5'] > semantic_metrics['precision@5']:
            print(f"  🎯 KEYWORD SEARCH is more precise")
            print(f"     (Keyword: {keyword_metrics['precision@5']:.2f} vs Semantic: {semantic_metrics['precision@5']:.2f})")
        elif semantic_metrics['precision@5'] > keyword_metrics['precision@5']:
            print(f"  🎯 SEMANTIC SEARCH is more precise")
            print(f"     (Semantic: {semantic_metrics['precision@5']:.2f} vs Keyword: {keyword_metrics['precision@5']:.2f})")
        else:
            print(f"  ➖ Both equally precise")

        if keyword_metrics['recall@5'] > semantic_metrics['recall@5']:
            print(f"  🔍 KEYWORD SEARCH finds more relevant docs")
        elif semantic_metrics['recall@5'] > keyword_metrics['recall@5']:
            print(f"  🔍 SEMANTIC SEARCH finds more relevant docs")
        else:
            print(f"  ➖ Both find same relevant docs")

        result_dict = {
            "query_idx": query_idx,
            "query": query_text,
            "category": query_data["category"],
            "expected": expected,
            "keyword_results": keyword_ids,
            "semantic_results": semantic_ids,
            "keyword_metrics": keyword_metrics,
            "semantic_metrics": semantic_metrics,
        }

        self.results.append(result_dict)
        return result_dict

    def run_all(self):
        """Run comparison for all queries"""
        for i in range(len(EVALUATION_QUERIES)):
            self.compare_query(i)

        self.print_summary()

    def print_summary(self):
        """Print overall summary"""
        print(f"\n\n{'='*70}")
        print(f"OVERALL SUMMARY")
        print(f"{'='*70}\n")

        # Calculate averages
        keyword_p5_avg = sum(r["keyword_metrics"]["precision@5"] for r in self.results) / len(self.results)
        semantic_p5_avg = sum(r["semantic_metrics"]["precision@5"] for r in self.results) / len(self.results)

        keyword_r5_avg = sum(r["keyword_metrics"]["recall@5"] for r in self.results) / len(self.results)
        semantic_r5_avg = sum(r["semantic_metrics"]["recall@5"] for r in self.results) / len(self.results)

        print(f"Queries evaluated: {len(self.results)}")
        print(f"\nAverage Precision@5:")
        print(f"  Keyword: {keyword_p5_avg:.2f}")
        print(f"  Semantic: {semantic_p5_avg:.2f}")

        print(f"\nAverage Recall@5:")
        print(f"  Keyword: {keyword_r5_avg:.2f}")
        print(f"  Semantic: {semantic_r5_avg:.2f}")

        # Analysis by category
        print(f"\n{'-'*70}")
        print(f"Analysis by Query Category:")
        print(f"{'-'*70}")

        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"keyword_wins": 0, "semantic_wins": 0, "ties": 0}

            k_prec = result["keyword_metrics"]["precision@5"]
            s_prec = result["semantic_metrics"]["precision@5"]

            if k_prec > s_prec:
                categories[cat]["keyword_wins"] += 1
            elif s_prec > k_prec:
                categories[cat]["semantic_wins"] += 1
            else:
                categories[cat]["ties"] += 1

        for cat, stats in sorted(categories.items()):
            print(f"\n  {cat.upper()}")
            print(f"    Semantic wins: {stats['semantic_wins']}")
            print(f"    Keyword wins: {stats['keyword_wins']}")
            print(f"    Ties: {stats['ties']}")

        print(f"\n{'='*70}")
        print(f"KEY INSIGHTS")
        print(f"{'='*70}\n")

        print("✓ SEMANTIC SEARCH EXCELS AT:")
        print("  • Paraphrases: 'how do computers learn' ≈ 'machine learning'")
        print("  • Synonyms: 'neural networks' ≈ 'deep learning architectures'")
        print("  • Related concepts: Understanding that SVM and decision trees are ML")
        print("  • Meaning: Grasping intent beyond exact words")

        print("\n✓ KEYWORD SEARCH EXCELS AT:")
        print("  • Technical terms: 'SVM' must appear for SVM results")
        print("  • Exact matches: Precise scientific terminology")
        print("  • Speed: Very fast, no model inference needed")
        print("  • Interpretability: You know why a result matched")

        print("\n🔄 HYBRID SEARCH COMBINES BENEFITS:")
        print("  • Use semantic for ranking (better recall)")
        print("  • Filter with keywords (better precision)")
        print("  • Rerank by term frequency (both signals)")
        print("  • Example: Elastic's hybrid search features")

        print(f"\n{'='*70}\n")


def main():
    """Run evaluation"""
    print("Initializing semantic search service...")

    service = get_search_service()

    # Check if we need to build index
    if service.get_stats()['chunks_indexed'] == 0:
        print("Building index...")
        from pathlib import Path
        docs_dir = Path(__file__).parent.parent / "data" / "sample_documents"
        service.build_index(str(docs_dir))

    # Run comparison
    comparison = SearchComparison(service)
    comparison.run_all()


if __name__ == "__main__":
    main()
