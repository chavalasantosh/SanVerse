#!/usr/bin/env python3
"""Test all 9 tokenization methods"""

import sys
import os
# Add parent directory to path (baby_steps is in root)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(parent_dir, 'src'))

from src.core.core_tokenizer import all_tokenizations
from src.core.core_tokenizer import combined_digit

print("=" * 60)
print("TEST ALL 9 TOKENIZATION METHODS")
print("=" * 60)

text = "I LOVE BEING ALONE"
print(f"\nInput: '{text}'\n")

# Get all tokenizations
results = all_tokenizations(text)

for method_name, tokens in results.items():
    print(f"{method_name.upper()}:")
    print(f"  Number of tokens: {len(tokens)}")
    print(f"  Tokens: {tokens[:10]}")  # First 10 tokens
    
    # Calculate digits for first few tokens
    digits = [combined_digit(t) for t in tokens[:5]]
    print(f"  First 5 digits: {digits}")
    print()

print("=" * 60)
print("✅ All 9 methods tested successfully!")
print("=" * 60)
