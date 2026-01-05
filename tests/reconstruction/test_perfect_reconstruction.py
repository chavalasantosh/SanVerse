"""
Comprehensive Reconstruction Test Suite for SanTOK

This test suite verifies 100% perfect reconstruction across all 9 SanTOK algorithms.
Tests are designed to be reproducible with deterministic seeds and comprehensive coverage.

Usage:
    pytest tests/reconstruction/test_perfect_reconstruction.py -v
    pytest tests/reconstruction/test_perfect_reconstruction.py::test_reconstruction_corpus -v --csv-output results.csv

Test Corpus:
    - Small corpus: 1,000 texts
    - Medium corpus: 10,000 texts  
    - Large corpus: 100,000 texts
    - Edge cases: Unicode, emojis, special characters
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.core_tokenizer import (
    tokenize_space,
    tokenize_word,
    tokenize_char,
    tokenize_grammar,
    tokenize_subword,
    tokenize_bytes,
    reconstruct_from_tokens,
    validate_reversibility,
)

# Test corpus generator
def generate_test_corpus(size="small", seed=42):
    """
    Generate reproducible test corpus.
    
    Args:
        size: "small" (1000), "medium" (10000), "large" (100000)
        seed: Random seed for reproducibility
    
    Returns:
        List of test strings
    """
    import random
    random.seed(seed)
    
    sizes = {"small": 1000, "medium": 10000, "large": 100000}
    count = sizes.get(size, 1000)
    
    # Base test cases
    base_cases = [
        "Hello world!",
        "The quick brown fox jumps over the lazy dog.",
        "1234567890",
        "!@#$%^&*()",
        "   multiple   spaces   ",
        "newline\ntest",
        "tab\ttest",
        "mixed123abc!@#",
        "",
        "a",
        "a" * 1000,  # Long string
    ]
    
    # Unicode test cases
    unicode_cases = [
        "Hello 世界",
        "مرحبا بالعالم",
        "Привет мир",
        "שלום עולם",
        "こんにちは世界",
        "안녕하세요 세계",
        "สวัสดีชาวโลก",
        "नमस्ते दुनिया",
        "🎉🎊🎈",
        "🔥💯✅",
        "👨‍👩‍👧‍👦",
        "🏳️‍🌈",
        "Z͑ͫ̓ͪ̂ͫ̽͏̴̙̤̞͉͚̯̞̠͍A̴̵̜̰͔ͫ͗͢L̶̤ͨͧͩ͆G̴̻͈͍͔̹̑͗̎̅͛́Ǫ̵̹̻̝̳͂̌̌͘!͖̬̰̙̗̿̋ͥͥ̂ͣ̐́́͜͞",
    ]
    
    # Combine all cases
    all_cases = base_cases + unicode_cases
    
    # Generate corpus
    corpus = []
    for i in range(count):
        if i < len(all_cases):
            corpus.append(all_cases[i])
        else:
            # Generate random text
            length = random.randint(10, 500)
            text = ''.join(random.choices(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%^&*()\n\t',
                k=length
            ))
            corpus.append(text)
    
    return corpus


# Test cases for each algorithm
ALGORITHMS = {
    "space": (tokenize_space, "space"),
    "word": (tokenize_word, "word"),
    "char": (tokenize_char, "char"),
    "grammar": (tokenize_grammar, "grammar"),
    "subword_fixed": (lambda t: tokenize_subword(t, chunk_len=3, strategy="fixed"), "subword"),
    "subword_bpe": (lambda t: tokenize_subword(t, chunk_len=3, strategy="bpe"), "subword"),
    "subword_syllable": (lambda t: tokenize_subword(t, chunk_len=3, strategy="syllable"), "subword"),
    "subword_frequency": (lambda t: tokenize_subword(t, chunk_len=3, strategy="frequency"), "subword"),
    "byte": (tokenize_bytes, "byte"),
}


class TestPerfectReconstruction:
    """Test suite for perfect reconstruction verification."""
    
    @pytest.mark.parametrize("algorithm_name,algorithm_func,recon_type", [
        (name, func, recon_type) for name, (func, recon_type) in ALGORITHMS.items()
    ])
    def test_reconstruction_basic(self, algorithm_name, algorithm_func, recon_type):
        """Test basic reconstruction for each algorithm."""
        test_cases = [
            "Hello world!",
            "The quick brown fox",
            "123 abc 456",
            "   spaces   ",
            "newline\ntest",
            "tab\ttest",
        ]
        
        for text in test_cases:
            tokens = algorithm_func(text)
            reconstructed = reconstruct_from_tokens(tokens, recon_type)
            assert reconstructed == text, (
                f"Algorithm {algorithm_name} failed reconstruction for text: {repr(text)}\n"
                f"Original length: {len(text)}, Reconstructed length: {len(reconstructed)}\n"
                f"Original: {repr(text)}\n"
                f"Reconstructed: {repr(reconstructed)}\n"
                f"Tokens: {tokens[:5]}..."
            )
    
    @pytest.mark.parametrize("algorithm_name,algorithm_func,recon_type", [
        (name, func, recon_type) for name, (func, recon_type) in ALGORITHMS.items()
    ])
    def test_reconstruction_unicode(self, algorithm_name, algorithm_func, recon_type):
        """Test Unicode reconstruction."""
        unicode_cases = [
            "Hello 世界",
            "مرحبا بالعالم",
            "Привет мир",
            "🎉🎊🎈",
            "👨‍👩‍👧‍👦",
            "Z͑ͫ̓ͪ̂ͫ̽͏̴̙̤̞͉͚̯̞̠͍A̴̵̜̰͔ͫ͗͢L̶̤ͨͧͩ͆",
        ]
        
        for text in unicode_cases:
            tokens = algorithm_func(text)
            reconstructed = reconstruct_from_tokens(tokens, recon_type)
            assert reconstructed == text, (
                f"Algorithm {algorithm_name} failed Unicode reconstruction for: {repr(text)}\n"
                f"Original: {repr(text)}\n"
                f"Reconstructed: {repr(reconstructed)}\n"
                f"Difference at position: {self._find_diff_position(text, reconstructed)}"
            )
    
    @pytest.mark.parametrize("algorithm_name,algorithm_func,recon_type", [
        (name, func, recon_type) for name, (func, recon_type) in ALGORITHMS.items()
    ])
    def test_reconstruction_edge_cases(self, algorithm_name, algorithm_func, recon_type):
        """Test edge cases."""
        edge_cases = [
            "",  # Empty string
            "a",  # Single character
            " " * 100,  # Only spaces
            "a" * 1000,  # Long string
            "\n" * 10,  # Only newlines
            "\t" * 10,  # Only tabs
        ]
        
        for text in edge_cases:
            tokens = algorithm_func(text)
            reconstructed = reconstruct_from_tokens(tokens, recon_type)
            assert reconstructed == text, (
                f"Algorithm {algorithm_name} failed edge case: {repr(text)}\n"
                f"Original: {repr(text)}\n"
                f"Reconstructed: {repr(reconstructed)}"
            )
    
    @pytest.mark.parametrize("algorithm_name,algorithm_func,recon_type", [
        (name, func, recon_type) for name, (func, recon_type) in ALGORITHMS.items()
    ])
    def test_reconstruction_corpus(self, algorithm_name, algorithm_func, recon_type):
        """Test reconstruction on generated corpus."""
        corpus = generate_test_corpus(size="small", seed=42)
        
        failed_cases = []
        total_chars = 0
        total_tokens = 0
        
        for i, text in enumerate(corpus):
            try:
                tokens = algorithm_func(text)
                reconstructed = reconstruct_from_tokens(tokens, recon_type)
                
                total_chars += len(text)
                total_tokens += len(tokens)
                
                if reconstructed != text:
                    failed_cases.append({
                        "index": i,
                        "original": text,
                        "reconstructed": reconstructed,
                        "tokens": tokens[:10],  # First 10 tokens
                    })
            except Exception as e:
                failed_cases.append({
                    "index": i,
                    "original": text,
                    "error": str(e),
                })
        
        # Report results
        success_rate = (len(corpus) - len(failed_cases)) / len(corpus) * 100
        
        print(f"\n{algorithm_name} Results:")
        print(f"  Total texts: {len(corpus)}")
        print(f"  Successful: {len(corpus) - len(failed_cases)}")
        print(f"  Failed: {len(failed_cases)}")
        print(f"  Success rate: {success_rate:.2f}%")
        print(f"  Total characters: {total_chars:,}")
        print(f"  Total tokens: {total_tokens:,}")
        print(f"  Avg tokens/char: {total_tokens/total_chars if total_chars > 0 else 0:.3f}")
        
        if failed_cases:
            print(f"\n  Failed cases (first 5):")
            for case in failed_cases[:5]:
                print(f"    Index {case['index']}: {repr(case.get('original', 'N/A'))[:50]}")
                if 'error' in case:
                    print(f"      Error: {case['error']}")
        
        # Assert 100% success
        assert len(failed_cases) == 0, (
            f"Algorithm {algorithm_name} failed {len(failed_cases)}/{len(corpus)} cases "
            f"({100 - success_rate:.2f}% failure rate). "
            f"First failure: {failed_cases[0] if failed_cases else 'N/A'}"
        )
    
    def test_reconstruction_deterministic(self):
        """Test that reconstruction is deterministic."""
        text = "Hello world! This is a test."
        algorithm_func = tokenize_word
        recon_type = "word"
        
        # Run multiple times
        results = []
        for _ in range(100):
            tokens = algorithm_func(text)
            reconstructed = reconstruct_from_tokens(tokens, recon_type)
            results.append(reconstructed)
        
        # All results should be identical
        assert all(r == text for r in results), "Reconstruction is not deterministic"
    
    def test_validate_reversibility_function(self):
        """Test the validate_reversibility helper function."""
        test_cases = [
            ("Hello world!", "word"),
            ("Hello world!", "char"),
            ("Hello world!", "space"),
            ("Hello 世界", "byte"),
        ]
        
        for text, algo_type in test_cases:
            result = validate_reversibility(text, algo_type)
            assert result is True, f"validate_reversibility failed for {algo_type} on {repr(text)}"
    
    @staticmethod
    def _find_diff_position(original, reconstructed):
        """Find the first position where strings differ."""
        min_len = min(len(original), len(reconstructed))
        for i in range(min_len):
            if original[i] != reconstructed[i]:
                return i
        if len(original) != len(reconstructed):
            return min_len
        return -1


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"])
