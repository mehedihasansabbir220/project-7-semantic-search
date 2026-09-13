"""
Semantic Search Engine - Main CLI Interface
Run this file to start the interactive search engine.
"""

import sys
import os

# Add backend to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.documents import DOCUMENTS
from search.semantic_search import SemanticSearchEngine, print_search_results


def print_welcome():
    """Print welcome message and instructions."""
    print("\n" + "=" * 100)
    print(" " * 30 + "SEMANTIC SEARCH ENGINE")
    print("=" * 100)
    print("\nWelcome! This is a semantic search engine that finds documents by meaning.")
    print("\nHow it works:")
    print("  1. Your query is converted to a 384-dimensional embedding")
    print("  2. This embedding is compared with all 20 document embeddings")
    print("  3. Documents are ranked by semantic similarity")
    print("  4. Top 5 most relevant documents are displayed")
    print("\nThis is LOCAL - everything runs on your machine, no external APIs needed.")
    print("\n" + "=" * 100)
    print("AVAILABLE CATEGORIES:")
    categories = set(doc["category"] for doc in DOCUMENTS)
    for category in sorted(categories):
        count = sum(1 for doc in DOCUMENTS if doc["category"] == category)
        print(f"  • {category}: {count} documents")
    print("\n" + "=" * 100 + "\n")


def print_commands():
    """Print available commands."""
    print("\nCOMMANDS:")
    print("  Type your search query and press Enter")
    print("  'help'     - Show example queries")
    print("  'stats'    - Show engine statistics")
    print("  'list'     - List all documents")
    print("  'quit'     - Exit the search engine")
    print()


def print_example_queries():
    """Print example queries users can try."""
    examples = [
        "machine learning algorithms",
        "deep learning",
        "natural language processing",
        "python programming",
        "neural networks",
        "embeddings and vectors",
        "supervised learning",
        "image recognition",
        "transformers BERT",
        "sentiment analysis",
    ]

    print("\n" + "=" * 100)
    print("EXAMPLE QUERIES TO TRY:")
    print("=" * 100)
    for i, query in enumerate(examples, 1):
        print(f"  {i:2d}. {query}")
    print("=" * 100 + "\n")


def list_all_documents():
    """List all indexed documents."""
    print("\n" + "=" * 100)
    print("ALL INDEXED DOCUMENTS")
    print("=" * 100)

    for doc in DOCUMENTS:
        print(f"\n[{doc['id']:2d}] {doc['title']}")
        print(f"      Category: {doc['category']}")
        print(f"      {doc['text'][:80]}...")

    print("\n" + "=" * 100 + "\n")


def print_statistics(engine):
    """Print engine statistics."""
    stats = engine.get_stats()

    print("\n" + "=" * 100)
    print("SEARCH ENGINE STATISTICS")
    print("=" * 100)
    print(f"Indexed Documents: {stats['num_documents']}")
    print(f"Embedding Dimensions: {stats['embedding_dimensions']}")
    print(f"Model: all-MiniLM-L6-v2")
    print(f"Categories: {', '.join(stats['categories'])}")
    print("\nHow it works:")
    print("  • Each document is embedded as 384 numbers")
    print("  • Your query is also converted to 384 numbers")
    print("  • Cosine similarity measures angle between vectors")
    print("  • Results ranked by similarity (0 = unrelated, 1 = identical)")
    print("=" * 100 + "\n")


def main():
    """Main function - run the semantic search engine."""

    print_welcome()

    # Initialize the semantic search engine
    print("Initializing semantic search engine...")
    engine = SemanticSearchEngine(model_name="all-MiniLM-L6-v2")

    # Index all documents (create embeddings)
    print("Indexing documents (computing embeddings)...")
    engine.index_documents(DOCUMENTS)

    print_commands()

    # Main search loop
    while True:
        try:
            # Get user input
            user_input = input("🔍 Search: ").strip()

            # Handle empty input
            if not user_input:
                print("Please enter a search query.")
                continue

            # Handle special commands
            if user_input.lower() == "quit":
                print("\n👋 Goodbye!\n")
                break

            elif user_input.lower() == "help":
                print_example_queries()
                continue

            elif user_input.lower() == "stats":
                print_statistics(engine)
                continue

            elif user_input.lower() == "list":
                list_all_documents()
                continue

            # Perform search
            results = engine.search(query=user_input, top_k=5)
            print_search_results(query=user_input, results=results, top_k=5)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


if __name__ == "__main__":
    main()
