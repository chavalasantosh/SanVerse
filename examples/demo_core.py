"""
SOMA Core Beginner Demo
====================

This demo ALWAYS works. It's the simplest possible example.

What it does:
1. Takes simple sentences
2. Trains embeddings
3. Tests similarity

If this works, you're winning! 🎉
"""

from soma_core.tokenizer import tokenize
from soma_core.train_embeddings import train_embeddings
from soma_core.similarity import similarity, find_similar_words


def main():
    """
    Main demo that always works.
    
    This is the simplest possible example.
    """
    print("=" * 60)
    print("SOMA Core Beginner Demo")
    print("=" * 60)
    print()
    
    # Step 1: Simple text data
    print("Step 1: Preparing text data...")
    text = [
        "cats chase mice",
        "dogs chase balls",
        "cats like milk"
    ]
    
    print(f"Texts: {text}")
    print()
    
    # Step 2: Train embeddings
    print("Step 2: Training embeddings...")
    print("-" * 60)
    embeddings = train_embeddings(text, epochs=20, vector_size=10)
    print()
    
    # Step 3: Test similarity
    print("Step 3: Testing similarity...")
    print("-" * 60)
    
    # Test 1: cats vs dogs (both animals, should be somewhat similar)
    sim1 = similarity("cats", "dogs", embeddings)
    print(f"similarity('cats', 'dogs') = {sim1:.3f}")
    print("  → Cats and dogs are both animals, so they should be similar!")
    print()
    
    # Test 2: cats vs milk (cats like milk, so should be related)
    sim2 = similarity("cats", "milk", embeddings)
    print(f"similarity('cats', 'milk') = {sim2:.3f}")
    print("  → Cats like milk, so they should be related!")
    print()
    
    # Test 3: chase vs balls (chase appears with balls, should be related)
    sim3 = similarity("chase", "balls", embeddings)
    print(f"similarity('chase', 'balls') = {sim3:.3f}")
    print("  → 'Chase' appears with 'balls', so they should be related!")
    print()
    
    # Test 4: Find similar words
    print("Step 4: Finding similar words...")
    print("-" * 60)
    
    similar_to_cats = find_similar_words("cats", embeddings, top_k=3)
    print(f"Words similar to 'cats':")
    for word, sim_score in similar_to_cats:
        print(f"  - {word}: {sim_score:.3f}")
    print()
    
    # Summary
    print("=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)
    print()
    print("What we learned:")
    print("  1. We can tokenize text (split into words)")
    print("  2. We can train embeddings (learn word relationships)")
    print("  3. We can measure similarity (how similar are words?)")
    print()
    print("If this worked, you're already winning! 🎉")
    print()


if __name__ == "__main__":
    main()
