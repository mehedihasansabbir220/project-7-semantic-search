"""
Evaluation Dataset for Semantic vs Keyword Search

This module contains test queries and their expected relevant documents.
Used to benchmark and compare search approaches.
"""

# Evaluation dataset: (query, expected_relevant_chunks)
EVALUATION_QUERIES = [
    {
        "query": "algorithms for machine learning",
        "category": "exact_match",
        "expected_chunks": ["doc_001_chunk_0004", "doc_001_chunk_0005"],
        "reasoning": "Direct mention of algorithms and machine learning"
    },
    {
        "query": "how do computers learn from data?",
        "category": "paraphrase",
        "expected_chunks": ["doc_001_chunk_0000"],
        "reasoning": "Paraphrases definition of machine learning (systems learning from data)"
    },
    {
        "query": "neural networks and deep architectures",
        "category": "synonym",
        "expected_chunks": ["doc_002_chunk_0001", "doc_002_chunk_0003", "doc_002_chunk_0004"],
        "reasoning": "Neural networks = deep learning architectures (synonymous)"
    },
    {
        "query": "tree-based decision making models",
        "category": "related_concept",
        "expected_chunks": ["doc_001_chunk_0004"],
        "reasoning": "Decision trees are related ML concept, mentioned in algorithms section"
    },
    {
        "query": "text understanding and language models",
        "category": "paraphrase",
        "expected_chunks": ["doc_003_chunk_0001", "doc_003_chunk_0010"],
        "reasoning": "NLP is about text understanding; transformers handle language"
    },
    {
        "query": "transformer attention mechanism",
        "category": "technical_term",
        "expected_chunks": ["doc_003_chunk_0010", "doc_003_chunk_0020"],
        "reasoning": "Technical term; transformers and attention are directly mentioned"
    },
    {
        "query": "overshooting model capacity overfitting",
        "category": "synonym",
        "expected_chunks": ["doc_001_chunk_0011"],
        "reasoning": "Overshooting = overfitting (model learning noise)"
    },
    {
        "query": "SVM kernel trick nonlinear data",
        "category": "technical_term",
        "expected_chunks": ["doc_001_chunk_0004"],
        "reasoning": "Support Vector Machines use kernels for non-linear classification"
    },
    {
        "query": "embeddings vector representations",
        "category": "synonym",
        "expected_chunks": ["doc_003_chunk_0004"],
        "reasoning": "Embeddings ARE vector representations of text"
    },
    {
        "query": "What teaches systems to improve performance",
        "category": "paraphrase",
        "expected_chunks": ["doc_001_chunk_0000"],
        "reasoning": "Definition of learning in ML context"
    },
]

# Document snippets (for reference)
DOCUMENT_SNIPPETS = {
    "doc_001_chunk_0000": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
    "doc_001_chunk_0004": "Key Algorithms: Decision Trees are hierarchical models that make decisions by splitting data based on feature values.",
    "doc_001_chunk_0005": "Support Vector Machines (SVM) find optimal hyperplanes that separate classes with maximum margin.",
    "doc_001_chunk_0011": "Overfitting occurs when models memorize training data and fail on new data.",

    "doc_002_chunk_0001": "An artificial neural network consists of input nodes, hidden layers, and output nodes.",
    "doc_002_chunk_0003": "Convolutional Neural Networks (CNN) are specifically designed for image processing.",
    "doc_002_chunk_0004": "Recurrent Neural Networks (RNN) process sequential data like text and time series.",

    "doc_003_chunk_0001": "Natural Language Processing (NLP) is a branch of artificial intelligence that focuses on enabling computers to understand, interpret, and generate human language.",
    "doc_003_chunk_0004": "Word embeddings represent words as dense vectors where similar words have similar representations.",
    "doc_003_chunk_0010": "Transformer Architecture revolutionized natural language processing by introducing self-attention mechanisms.",
    "doc_003_chunk_0020": "Attention mechanisms allow models to focus on relevant parts of the source text when generating each target word.",
}

def get_evaluation_dataset():
    """Return evaluation dataset"""
    return EVALUATION_QUERIES

def get_expected_documents(query_idx):
    """Get expected relevant documents for a query"""
    return EVALUATION_QUERIES[query_idx]["expected_chunks"]

def get_query_text(query_idx):
    """Get query text"""
    return EVALUATION_QUERIES[query_idx]["query"]

def get_query_category(query_idx):
    """Get query category (for analysis)"""
    return EVALUATION_QUERIES[query_idx]["category"]
