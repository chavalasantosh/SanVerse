# Reconstruction Test Suite

This directory contains comprehensive tests for verifying perfect reconstruction across all SOMA algorithms.

## Overview

The test suite verifies that all 9 SOMA tokenization algorithms achieve 100% perfect reconstruction - meaning that for any input text, the tokenized output can be perfectly reconstructed to recover the original text.

## Test Files

- `test_perfect_reconstruction.py`: Main test suite with comprehensive coverage

## Running Tests

### Basic Usage

```bash
# Run all reconstruction tests
pytest tests/reconstruction/test_perfect_reconstruction.py -v

# Run specific test
pytest tests/reconstruction/test_perfect_reconstruction.py::TestPerfectReconstruction::test_reconstruction_basic -v

# Run with output
pytest tests/reconstruction/test_perfect_reconstruction.py -v -s
```

### Test Coverage

The test suite includes:

1. **Basic Reconstruction Tests**: Standard text cases for all algorithms
2. **Unicode Tests**: Multilingual text including CJK, Arabic, Cyrillic, Hebrew, Thai, Devanagari
3. **Edge Case Tests**: Empty strings, single characters, long strings, special characters
4. **Corpus Tests**: Large-scale testing on generated corpus (1000 texts by default)
5. **Determinism Tests**: Verifies reconstruction is deterministic across multiple runs

### Test Algorithms

All 9 SOMA algorithms are tested:
- Space tokenization
- Word tokenization
- Character tokenization
- Grammar tokenization
- Subword tokenization (4 strategies: fixed, BPE, syllable, frequency)
- Byte tokenization

## Test Corpus

The test corpus is generated deterministically using seed=42 for reproducibility. It includes:

- Base test cases: Standard English text, numbers, punctuation, whitespace
- Unicode test cases: Multilingual text, emojis, complex Unicode sequences
- Generated cases: Random text for large-scale testing

## Reproducibility

All tests use:
- **Deterministic seed**: seed=42 for corpus generation
- **Deterministic tokenization**: SOMA algorithms are deterministic
- **Exact comparison**: Byte-by-byte comparison of original vs reconstructed

## Expected Results

All tests should pass with 100% success rate. The test suite reports:
- Total texts tested
- Successful reconstructions
- Failed reconstructions (should be 0)
- Success rate (should be 100%)
- Total characters processed
- Total tokens generated
- Average tokens per character

## Failure Reporting

If a test fails, the output includes:
- Algorithm name
- Original text
- Reconstructed text
- Token sequence
- Position of first difference (if applicable)

## Adding New Tests

To add new test cases:

1. Add text cases to `generate_test_corpus()` function
2. Add specific test cases to test methods
3. Ensure test cases cover edge cases and Unicode

## Requirements

- Python 3.8+
- pytest
- SOMA core tokenizer module

## CI Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run reconstruction tests
  run: pytest tests/reconstruction/test_perfect_reconstruction.py -v --tb=short
```

## Notes

- Tests are designed to be fast (< 1 minute for full suite)
- Large corpus tests can be skipped with `--skip-large` flag
- Unicode tests require proper terminal/encoding support

