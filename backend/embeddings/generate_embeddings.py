"""
Generate text embeddings using Sentence Transformers.
Learn how text is converted to numerical vectors.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================================
# STEP 1: Load the pretrained model
# ============================================================================
print("=" * 80)
print("STEP 1: Loading Pretrained Model")
print("=" * 80)

model = SentenceTransformer("all-MiniLM-L6-v2")
print(f"✓ Model loaded: all-MiniLM-L6-v2")
print(f"✓ This model outputs 384-dimensional embeddings")
print()

# ============================================================================
# STEP 2: Create example sentences
# ============================================================================
print("=" * 80)
print("STEP 2: Example Sentences")
print("=" * 80)

example_sentences = [
    "The cat sat on the mat.",
    "I enjoy eating fresh fruit.",
    "Machine learning is a powerful technology.",
    "The weather is beautiful today.",
    "Python is used for data science.",
]

for i, sentence in enumerate(example_sentences, 1):
    print(f"{i}. {sentence}")
print()

# ============================================================================
# STEP 3: Generate embeddings
# ============================================================================
print("=" * 80)
print("STEP 3: Generate Embeddings")
print("=" * 80)

embeddings = model.encode(example_sentences)

print(f"✓ Generated {len(embeddings)} embeddings")
print(f"✓ Shape: {embeddings.shape} (5 sentences × 384 dimensions)")
print()

# ============================================================================
# STEP 4: Analyze each embedding
# ============================================================================
print("=" * 80)
print("STEP 4: Detailed Analysis of Each Embedding")
print("=" * 80)

for i, (sentence, embedding) in enumerate(zip(example_sentences, embeddings), 1):
    print(f"\nSentence {i}: {sentence}")
    print(f"  Embedding shape: {embedding.shape}")
    print(f"  First 10 values: {embedding[:10]}")
    print(f"  Min value: {embedding.min():.4f}")
    print(f"  Max value: {embedding.max():.4f}")
    print(f"  Mean value: {embedding.mean():.4f}")
    print(f"  Std dev: {embedding.std():.4f}")

print()

# ============================================================================
# STEP 5: Why fixed-size vectors?
# ============================================================================
print("=" * 80)
print("STEP 5: Why Every Sentence Produces a Fixed-Size Vector")
print("=" * 80)

explanation = """
REASON: The neural network architecture is designed with a fixed output size.

HOW IT WORKS:
1. Sentences can be different lengths (5 words, 50 words, 100 words)
2. The tokenizer converts words to token IDs (variable length)
3. The transformer processes each token independently
4. A POOLING operation aggregates all tokens into ONE vector
5. This pooled vector always has the same size (384 dimensions)

ANALOGY:
Think of a coffee shop that blends different ingredients:
- Tall frappe (100 ml) + Short coffee (30 ml) → Both get BLENDED
- Result: Always 384ml cup (the embedding size)
- The blending captures the essence of all ingredients

TECHNICAL DETAIL:
The pooling operation (mean pooling in MiniLM) takes the average of all
token representations, which creates a single fixed-size vector regardless
of input length.
"""

print(explanation)

# ============================================================================
# STEP 6: What do vector dimensions represent?
# ============================================================================
print("=" * 80)
print("STEP 6: What Do Vector Dimensions Represent?")
print("=" * 80)

dimension_explanation = """
SHORT ANSWER: We DON'T know, and we CAN'T interpret individual dimensions.

WHAT THE DIMENSIONS ARE:
- Each dimension is a latent feature learned by the neural network
- The network learned these patterns from billions of sentences
- They capture semantic information, but NOT in human-readable form

WHAT THEY ARE NOT:
✗ NOT: "Dimension 1 = sentiment"
✗ NOT: "Dimension 2 = word count"
✗ NOT: "Dimension 5 = 'action' features"
✗ NOT: "Each dimension = one word or concept"

WHY WE CAN'T INTERPRET THEM:
- The 384 dimensions work TOGETHER as a holistic representation
- A single dimension alone means nothing
- Meaning emerges from the COMBINATION of all 384 values
- This is the "black box" aspect of neural networks

WHAT WE CAN DO:
✓ Compare distances between vectors (cosine similarity)
✓ Use vectors in downstream tasks (search, classification)
✓ Observe that semantically similar texts have similar embeddings
✓ Trust that the pretrained model captured useful information

ANALOGY:
A painting's colors can't be understood by looking at individual pixel values.
The meaning comes from how all pixels work together as a whole.
Same with embeddings: meaning comes from the whole vector, not individual dimensions.
"""

print(dimension_explanation)

# ============================================================================
# STEP 7: Why use pretrained models?
# ============================================================================
print("=" * 80)
print("STEP 7: Why Use Pretrained Models Instead of Training Our Own?")
print("=" * 80)

pretrained_explanation = """
TRAINING A MODEL FROM SCRATCH:
⏱️  Time: 100+ GPU hours
💾 Data: Billions of sentences needed
💰 Cost: $10,000+ in compute
🎓 Expertise: Deep ML knowledge required
⚠️  Result: Likely to be worse than existing models

USING A PRETRAINED MODEL:
⚡ Time: Seconds to load and use
💾 Data: Already trained on billions of sentences
💰 Cost: Free (open source)
🎓 Expertise: Just Python knowledge needed
✅ Result: Production-quality embeddings

WHY PRETRAINED WORKS:
1. Transfer Learning: The model learned patterns from billions of sentences
2. General Knowledge: Understands language patterns, synonyms, concepts
3. Ready to Use: Already optimized for semantic similarity
4. Fast: Only need to encode text, not train anything

OUR USE CASE:
We load all-MiniLM-L6-v2 (384 dimensions, fast, accurate).
It was trained on 215M sentence pairs.
It took researchers months to train.
We get it in 2 lines of code.
"""

print(pretrained_explanation)

# ============================================================================
# STEP 8: Experiment - Similar vs. Unrelated Sentences
# ============================================================================
print("=" * 80)
print("STEP 8: Experiment - Semantic Similarity")
print("=" * 80)

# Create test sentences
similar_sentences = [
    "I love eating apples.",
    "I enjoy eating apples.",
]

unrelated_sentences = [
    "I love eating apples.",
    "The capital of France is Paris.",
]

print("\nEXPERIMENT 1: Similar Sentences")
print(f"  Sentence 1: \"{similar_sentences[0]}\"")
print(f"  Sentence 2: \"{similar_sentences[1]}\"")

similar_embeddings = model.encode(similar_sentences)
similar_score = cosine_similarity([similar_embeddings[0]], [similar_embeddings[1]])[0][0]
print(f"  Cosine Similarity: {similar_score:.4f}")
print(f"  ✓ HIGH score (close to 1.0) = Very similar meaning")

print("\nEXPERIMENT 2: Unrelated Sentences")
print(f"  Sentence 1: \"{unrelated_sentences[0]}\"")
print(f"  Sentence 2: \"{unrelated_sentences[1]}\"")

unrelated_embeddings = model.encode(unrelated_sentences)
unrelated_score = cosine_similarity([unrelated_embeddings[0]], [unrelated_embeddings[1]])[0][0]
print(f"  Cosine Similarity: {unrelated_score:.4f}")
print(f"  ✓ LOW score (close to 0.0) = Different meanings")

print("\nKEY INSIGHT:")
print(f"  Similarity difference: {abs(similar_score - unrelated_score):.4f}")
print(f"  The embeddings captured semantic meaning!")
print(f"  Similar sentences have closer embeddings (higher cosine similarity).")
print(f"  Unrelated sentences have distant embeddings (lower cosine similarity).")

print()

# ============================================================================
# STEP 9: Summary
# ============================================================================
print("=" * 80)
print("SUMMARY: What We Learned")
print("=" * 80)

summary = """
1. TEXT → EMBEDDING PROCESS:
   Text (variable length) → Tokenization → Neural Network → Pooling → 384 numbers

2. FIXED-SIZE OUTPUT:
   Regardless of input length, we always get 384 dimensions because of pooling.

3. DIMENSIONS ARE LATENT FEATURES:
   We can't interpret individual dimensions, but together they represent meaning.

4. PRETRAINED MODELS:
   Using existing models is efficient, practical, and gives better results.

5. SEMANTIC INFORMATION:
   Embeddings capture meaning: similar texts have similar embeddings.

6. HOW SEARCH WORKS:
   We compare embedding vectors using cosine similarity.
   Documents most similar to the query embedding are returned as results.

NEXT STEP:
Now that you understand embeddings, we'll build vector search in Task 03!
"""

print(summary)
print("=" * 80)
