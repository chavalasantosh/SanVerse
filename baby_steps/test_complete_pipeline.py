#!/usr/bin/env python3
"""Complete tokenization pipeline test with all properties"""

import sys
import os
# Add parent directory to path (baby_steps is in root)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(parent_dir, 'src'))

from src.core.core_tokenizer import (
    tokenize_word,
    assign_uids,
    neighbor_uids,
    combined_digit,
    compose_backend_number,
    _content_id
)

print("=" * 60)
print("COMPLETE TOKENIZATION PIPELINE TEST")
print("=" * 60)

# Configuration
text = "I love being alone"
seed = 42
embedding_bit = False

print(f"\nInput: '{text}'")
print(f"Seed: {seed}, Embedding Bit: {embedding_bit}\n")

# Step 1: Tokenize
tokens = tokenize_word(text)
print(f"Step 1 - Tokens: {tokens}")

# Step 2: Assign UIDs
with_uids = assign_uids([{"text": t, "index": i} for i, t in enumerate(tokens)], seed)
print(f"Step 2 - UIDs assigned: {len(with_uids)} tokens")

# Step 3: Add neighbor UIDs
with_neighbors = neighbor_uids(with_uids)
print(f"Step 3 - Neighbor UIDs added")

# Step 4: Process each token
print("\n" + "-" * 60)
print("COMPLETE TOKEN RECORDS:")
print("-" * 60)

for i, rec in enumerate(with_neighbors):
    token = rec["text"]
    uid = rec["uid"]
    prev_uid = rec.get("prev_uid")
    next_uid = rec.get("next_uid")
    
    # Calculate all properties
    frontend = combined_digit(token, embedding_bit)
    backend_huge = compose_backend_number(token, i, uid, prev_uid, next_uid, embedding_bit)
    backend_scaled = backend_huge % 100000
    content_id = _content_id(token)
    
    print(f"\nToken {i}: '{token}'")
    print(f"  UID: {uid}")
    print(f"  Frontend: {frontend}")
    print(f"  Backend Scaled: {backend_scaled}")
    print(f"  Content ID: {content_id}")
    print(f"  Prev UID: {prev_uid if prev_uid else 'None'}")
    print(f"  Next UID: {next_uid if next_uid else 'None'}")

print("\n" + "=" * 60)
print("✅ Complete pipeline test passed!")
print("=" * 60)
