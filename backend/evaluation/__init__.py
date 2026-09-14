"""
Evaluation module for semantic search.

Contains:
- Evaluation datasets
- Keyword search implementation
- Evaluation metrics
- Comparison tools
"""

from evaluation.dataset import EVALUATION_QUERIES, get_evaluation_dataset
from evaluation.keyword_search import KeywordSearcher
from evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    mean_reciprocal_rank,
    EvaluationMetrics,
)
from evaluation.compare import SearchComparison

__all__ = [
    "EVALUATION_QUERIES",
    "get_evaluation_dataset",
    "KeywordSearcher",
    "precision_at_k",
    "recall_at_k",
    "mean_reciprocal_rank",
    "EvaluationMetrics",
    "SearchComparison",
]
