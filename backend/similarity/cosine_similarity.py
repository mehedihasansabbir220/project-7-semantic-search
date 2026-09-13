"""
Understand Cosine Similarity: How the system measures semantic similarity.
We'll implement cosine similarity manually, then compare with library implementation.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
import pandas as pd

# ============================================================================
# PART 1: Generate Embeddings for Test Sentences
# ============================================================================
print("=" * 90)
print("PART 1: Generate Embeddings")
print("=" * 90)

model = SentenceTransformer("all-MiniLM-L6-v2")

# Create test sentences
test_sentences = [
    "I love eating fresh apples.",
    "I enjoy apples very much.",
    "Apple pie is delicious.",
    "The capital of France is Paris.",
    "Python is a programming language.",
    "Dogs are loyal pets.",
]

print(f"Loading model: all-MiniLM-L6-v2")
print(f"Generating embeddings for {len(test_sentences)} sentences...\n")

embeddings = model.encode(test_sentences)

# Display sentences with their indices
for i, sentence in enumerate(test_sentences):
    print(f"[{i}] {sentence}")

print(f"\n✓ Generated embeddings shape: {embeddings.shape}")
print(f"✓ Each embedding: 384 dimensions")
print()

# ============================================================================
# PART 2: Understanding the Mathematics
# ============================================================================
print("=" * 90)
print("PART 2: Mathematics of Cosine Similarity")
print("=" * 90)

math_explanation = """
WHAT IS COSINE SIMILARITY?
It's a mathematical formula that measures how similar two vectors are by looking at the angle
between them.

THE FORMULA:
    cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)

BREAKING IT DOWN:

1. DOT PRODUCT (A · B):
   - Multiply corresponding elements of both vectors and sum them up
   - Example: A = [1, 2, 3], B = [4, 5, 6]
   - A · B = (1×4) + (2×5) + (3×6) = 4 + 10 + 18 = 32
   - This tells us how much vectors "align" in direction

2. MAGNITUDE (||A||):
   - The length of a vector
   - Formula: √(a₁² + a₂² + a₃² + ... + aₙ²)
   - Example: A = [1, 2, 3]
   - ||A|| = √(1² + 2² + 3²) = √14 ≈ 3.74
   - This normalizes for vector length

3. COMBINE THEM:
   - Result is always between -1 and 1
   - 1.0 = identical direction (same meaning)
   - 0.5 = moderately similar
   - 0.0 = perpendicular (unrelated)
   - -1.0 = opposite direction (contradictory)

GEOMETRIC INTUITION:
Imagine two arrows in space:
- If they point the SAME way → small angle → high cosine
- If they point DIFFERENT ways → large angle → low cosine
- Cosine measures this angle relationship mathematically
"""

print(math_explanation)
print()

# ============================================================================
# PART 3: Manual Implementation
# ============================================================================
print("=" * 90)
print("PART 3: Manual Implementation from Scratch")
print("=" * 90)

def manual_cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors manually using NumPy.

    Args:
        vector_a: First embedding (1D array of numbers)
        vector_b: Second embedding (1D array of numbers)

    Returns:
        Similarity score between -1 and 1
    """

    # Step 1: Calculate dot product (A · B)
    # This multiplies corresponding elements and sums them
    dot_product = np.dot(vector_a, vector_b)

    # Step 2: Calculate magnitude of vector A (||A||)
    # This is the length of the vector in space
    magnitude_a = np.linalg.norm(vector_a)

    # Step 3: Calculate magnitude of vector B (||B||)
    magnitude_b = np.linalg.norm(vector_b)

    # Step 4: Divide dot product by product of magnitudes
    # This normalizes by vector length
    similarity = dot_product / (magnitude_a * magnitude_b)

    return similarity


print("✓ Function created: manual_cosine_similarity()\n")
print("How it works:")
print("  1. Calculate dot product (how much vectors align)")
print("  2. Calculate magnitude of each vector (length in space)")
print("  3. Divide: dot_product / (magnitude_a × magnitude_b)")
print("  4. Result: number between -1 and 1")
print()

# ============================================================================
# PART 4: Test Manual Implementation
# ============================================================================
print("=" * 90)
print("PART 4: Testing Manual Implementation")
print("=" * 90)

print("\nEXAMPLE 1: Similar Sentences (Both about apples)")
print("-" * 90)
sentence_a_idx = 0  # "I love eating fresh apples."
sentence_b_idx = 1  # "I enjoy apples very much."

vector_a = embeddings[sentence_a_idx]
vector_b = embeddings[sentence_b_idx]

similarity = manual_cosine_similarity(vector_a, vector_b)

print(f"Sentence A [{sentence_a_idx}]: {test_sentences[sentence_a_idx]}")
print(f"Sentence B [{sentence_b_idx}]: {test_sentences[sentence_b_idx]}")
print(f"\nManual calculation:")
print(f"  Dot product: {np.dot(vector_a, vector_b):.4f}")
print(f"  Magnitude A: {np.linalg.norm(vector_a):.4f}")
print(f"  Magnitude B: {np.linalg.norm(vector_b):.4f}")
print(f"  Cosine Similarity: {similarity:.4f}")
print(f"  ✓ HIGH score → Similar meaning (both about apples)")
print()

print("\nEXAMPLE 2: Unrelated Sentences (Apples vs. Paris)")
print("-" * 90)
sentence_a_idx = 0  # "I love eating fresh apples."
sentence_b_idx = 3  # "The capital of France is Paris."

vector_a = embeddings[sentence_a_idx]
vector_b = embeddings[sentence_b_idx]

similarity = manual_cosine_similarity(vector_a, vector_b)

print(f"Sentence A [{sentence_a_idx}]: {test_sentences[sentence_a_idx]}")
print(f"Sentence B [{sentence_b_idx}]: {test_sentences[sentence_b_idx]}")
print(f"\nManual calculation:")
print(f"  Dot product: {np.dot(vector_a, vector_b):.4f}")
print(f"  Magnitude A: {np.linalg.norm(vector_a):.4f}")
print(f"  Magnitude B: {np.linalg.norm(vector_b):.4f}")
print(f"  Cosine Similarity: {similarity:.4f}")
print(f"  ✓ LOW score → Unrelated meaning (apples vs. geography)")
print()

# ============================================================================
# PART 5: Create Similarity Matrix
# ============================================================================
print("=" * 90)
print("PART 5: Similarity Matrix (All Pairs)")
print("=" * 90)

print("\nCalculating similarity between all sentence pairs using manual implementation...\n")

# Create similarity matrix using manual implementation
n_sentences = len(embeddings)
similarity_matrix_manual = np.zeros((n_sentences, n_sentences))

for i in range(n_sentences):
    for j in range(n_sentences):
        similarity_matrix_manual[i][j] = manual_cosine_similarity(
            embeddings[i], embeddings[j]
        )

# Create a nice DataFrame for display
df_manual = pd.DataFrame(
    similarity_matrix_manual,
    index=[f"[{i}]" for i in range(n_sentences)],
    columns=[f"[{i}]" for i in range(n_sentences)]
)

print("Manual Implementation - Cosine Similarity Matrix:")
print("(Rows = Sentence A, Columns = Sentence B)\n")
print(df_manual.round(4))
print()

# Interpretation
print("INTERPRETATION:")
print("  - Diagonal = 1.0000 (each sentence is identical to itself)")
print("  - [0] & [1] = 0.95+ (similar sentences about apples)")
print("  - [0] & [3] = low (apples vs. Paris - unrelated)")
print("  - [1] & [2] = high (all about apples)")
print()

# ============================================================================
# PART 6: Compare with Library Implementation
# ============================================================================
print("=" * 90)
print("PART 6: Compare with Sklearn Implementation")
print("=" * 90)

print("\nNow let's verify our manual implementation against sklearn...\n")

# Reshape embeddings for sklearn (it expects 2D array)
similarity_matrix_sklearn = sklearn_cosine_similarity(embeddings)

df_sklearn = pd.DataFrame(
    similarity_matrix_sklearn,
    index=[f"[{i}]" for i in range(n_sentences)],
    columns=[f"[{i}]" for i in range(n_sentences)]
)

print("Sklearn Implementation - Cosine Similarity Matrix:\n")
print(df_sklearn.round(4))
print()

# Compare the two implementations
print("VERIFICATION: Comparing manual vs sklearn")
print("-" * 90)
difference = np.abs(similarity_matrix_manual - similarity_matrix_sklearn)
max_difference = np.max(difference)
print(f"Maximum difference between manual and sklearn: {max_difference:.10f}")
print(f"✓ Difference is essentially 0 (rounding error only)")
print(f"✓ Our manual implementation is correct!")
print()

# ============================================================================
# PART 7: Why Cosine Similarity for Embeddings?
# ============================================================================
print("=" * 90)
print("PART 7: Why Cosine Similarity is Used for Embeddings")
print("=" * 90)

why_cosine = """
1. DIRECTION MATTERS, NOT MAGNITUDE:
   - Cosine similarity only cares about the angle between vectors
   - It ignores the length of the vectors
   - This is important because embeddings are normalized
   - Two vectors pointing the same way (similar meaning) get high score

2. FAST TO COMPUTE:
   - Simple formula: dot product / (magnitude × magnitude)
   - Can be computed very quickly
   - Essential when searching millions of documents

3. NORMALIZED RESULT (-1 to 1):
   - Easy to interpret: 1.0 = identical, 0.0 = unrelated, -1.0 = opposite
   - Can compare across different embedding sets
   - Natural threshold: 0.5 often means "somewhat similar"

4. GEOMETRICALLY INTUITIVE:
   - Cosine = angle between vectors
   - 0° angle (same direction) → cosine = 1.0
   - 90° angle (perpendicular) → cosine = 0.0
   - Visual understanding helps with debugging

5. WORKS WELL WITH NEURAL NETWORKS:
   - Embeddings from deep learning are designed to work with cosine similarity
   - The model was trained with this metric in mind
   - Results align with human intuition

ALTERNATIVE METRICS (and why we don't use them):
- Euclidean Distance: Cares about magnitude, not just direction
- Manhattan Distance: Slower, less intuitive for embeddings
- Dot Product alone: Unbounded, hard to interpret
"""

print(why_cosine)
print()

# ============================================================================
# PART 8: What Does High Similarity Mean?
# ============================================================================
print("=" * 90)
print("PART 8: Understanding Similarity Scores")
print("=" * 90)

score_explanation = """
SIMILARITY SCORE RANGES:

Score Range          | Interpretation                    | Example
─────────────────────┼───────────────────────────────────┼──────────────────────────
0.95 - 1.00         | Nearly identical meaning           | "I love apples" vs "I enjoy apples"
0.80 - 0.95         | Very similar                       | "Apple pie" vs "I love apples"
0.60 - 0.80         | Somewhat related                   | "Apple" vs "Fruit"
0.40 - 0.60         | Loosely related                    | "Food" vs "Restaurant"
0.20 - 0.40         | Weakly related                     | "Apple" vs "Computer"
0.00 - 0.20         | Unrelated or very different        | "Apple" vs "Paris"
-0.20 - 0.00        | Contradictory or opposite          | "Happy" vs "Sad"

IMPORTANT THRESHOLDS:
- Search results: typically show scores > 0.5
- Duplicate detection: typically use threshold > 0.95
- Related documents: typically threshold > 0.7
"""

print(score_explanation)
print()

# ============================================================================
# PART 9: Critical Limitation - Similarity ≠ Factual Correctness
# ============================================================================
print("=" * 90)
print("PART 9: Important Limitation!")
print("=" * 90)

limitation = """
⚠️  CRITICAL UNDERSTANDING:

HIGH SIMILARITY DOES NOT MEAN FACTUALLY CORRECT!

EXAMPLE 1: Similar but Both False
Query: "Apples are toxic to humans"
Match: "Eating apples will poison you" (similarity: 0.92)
Reality: BOTH statements are false! Apples are healthy.

EXAMPLE 2: Low Similarity but One Is True
Query: "Water boils at 100 Celsius"
Match: "The boiling point of water is 212 Fahrenheit" (similarity: 0.45)
Reality: Both are TRUE, but similarity is low because words are different

EXAMPLE 3: Perfect Similarity but Misleading
Query: "Albert Einstein was the smartest person ever"
Match: "Albert Einstein was intellectually gifted" (similarity: 0.89)
Accuracy: First is unverifiable opinion, second is more accurate

WHY THIS HAPPENS:
- Cosine similarity measures SEMANTIC SIMILARITY
- It does NOT verify factual accuracy
- It does NOT check if information is current/outdated
- It does NOT understand context, time, or domain specifics

PRACTICAL IMPLICATIONS:
✓ USE semantic search for: Finding related documents, recommendations, grouping
✗ DON'T USE for: Fact-checking, medical/legal decisions, critical information

SOLUTION:
Always combine semantic search with:
1. Fact-checking systems
2. Domain expert review
3. Source verification
4. Temporal context (is this current?)
5. Confidence scoring from other models

EXAMPLE WORKFLOW:
Step 1: Use semantic search to find candidate documents (fast)
Step 2: Rank by relevance using semantic similarity
Step 3: Verify facts with external sources (slow but accurate)
Step 4: Return checked results to user
"""

print(limitation)
print()

# ============================================================================
# PART 10: Detailed Examples
# ============================================================================
print("=" * 90)
print("PART 10: Detailed Examples and Insights")
print("=" * 90)

print("\nTop 5 Most Similar Pairs (excluding self-matches):\n")

# Find top similar pairs
pairs = []
for i in range(n_sentences):
    for j in range(i + 1, n_sentences):
        score = similarity_matrix_sklearn[i][j]
        pairs.append((i, j, score))

pairs_sorted = sorted(pairs, key=lambda x: x[2], reverse=True)

for rank, (i, j, score) in enumerate(pairs_sorted[:5], 1):
    print(f"{rank}. Similarity: {score:.4f}")
    print(f"   [{i}] {test_sentences[i]}")
    print(f"   [{j}] {test_sentences[j]}")
    print()

print("\nTop 5 Most Different Pairs:\n")

for rank, (i, j, score) in enumerate(sorted(pairs, key=lambda x: x[2])[:5], 1):
    print(f"{rank}. Similarity: {score:.4f}")
    print(f"   [{i}] {test_sentences[i]}")
    print(f"   [{j}] {test_sentences[j]}")
    print()

# ============================================================================
# PART 11: Summary
# ============================================================================
print("=" * 90)
print("SUMMARY")
print("=" * 90)

summary = """
KEY LEARNINGS:

1. COSINE SIMILARITY FORMULA:
   similarity = (A · B) / (||A|| × ||B||)

   Components:
   - Dot product: measures alignment
   - Magnitudes: normalize for vector length
   - Result: number between -1 and 1

2. WHY IT WORKS:
   - Measures angle between vectors
   - Small angle = similar direction = high score
   - Only needs 3 operations (dot, norm, divide)

3. PROPERTIES:
   - Fast: O(n) where n = embedding dimensions (384)
   - Intuitive: 1.0 = identical, 0.0 = unrelated
   - Normalized: comparable across different pairs

4. LIMITATIONS:
   - Measures similarity, NOT factual correctness
   - Can be fooled by false statements that sound similar
   - Doesn't understand time, context, or domain

5. REAL-WORLD USE:
   - Search engines: find relevant documents
   - Recommendation systems: find similar products
   - Duplicate detection: find identical content
   - But always combine with fact-checking!

NEXT STEP:
Now we understand how to measure similarity between embeddings.
In Task 04, we'll build actual vector search using this knowledge!
"""

print(summary)
print("=" * 90)
