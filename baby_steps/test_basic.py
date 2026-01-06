#!/usr/bin/env python3
"""Basic tokenization test - Run this first after cloning"""

from soma import TextTokenizationEngine

print("=" * 60)
print("BASIC TOKENIZATION TEST")
print("=" * 60)

# Initialize engine
engine = TextTokenizationEngine()

# Test tokenization
text = "Hello World"
result = engine.tokenize(text, tokenization_method="word")

print(f"\nInput: '{text}'")
print(f"Tokens: {result['tokens']}")
print(f"Frontend Digits: {result.get('frontend_digits', 'N/A')}")
print("\n✅ Basic test passed!")
