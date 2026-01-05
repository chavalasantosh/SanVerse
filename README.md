# SOMA: Advanced Intelligence Framework

[![PyPI version](https://badge.fury.io/py/soma.svg)](https://badge.fury.io/py/soma)
[![Python Versions](https://img.shields.io/pypi/pyversions/soma.svg)](https://pypi.org/project/soma/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://github.com/chavalasantosh/SanVerse/actions/workflows/python-tests.yml/badge.svg)](https://github.com/chavalasantosh/SanVerse/actions)

**SOMA** is a next-generation tokenization and intelligence framework designed to bridge the gap between raw text and semantic understanding. Unlike traditional tokenizers that simply split text, SOMA applies mathematical analysis, feature extraction, and cognitive structures to create a richer representation of language.

> _"Intelligence begins with how we perceive the data. SOMA changes the perception."_

---

## 🚀 Why SOMA?

SOMA is built for researchers and developers who need more than just BPE (Byte Pair Encoding). It offers a unified engine for:

- **Universal Tokenization**: Seamlessly switch between whitespace, word, character, subword, and grammar-based strategies.
- **Mathematical Embeddings**: Proprietary "Frontend Digit" calculation for deterministic, low-compute feature extraction.
- **Cognitive Architecture**: Integrated support for Small Language Models (SLMs) and reasoning pipelines.
- **Structure-Aware**: The `soma_core` module understands text hierarchy and structural patterns effectively.

## 📦 Installation

```bash
pip install soma
```

## ⚡ Quick Start

### Python API

```python
from soma import TextTokenizationEngine

# Initialize the engine
engine = TextTokenizationEngine()

# Process text with advanced analysis
text = "The future of AI is structural."
result = engine.tokenize(text, tokenization_method="subword")

print(f"Tokens:   {result['tokens']}")
print(f"Features: {result['features']}")
# Output:
# Tokens:   ['The', 'fut', 'ure', 'of', 'AI', 'is', 'str', 'uct', 'ural', '.']
# Features: {'entropy_index': 7, 'balance_index': 4, ...}
```

### Command Line Interface

Process files directly from your terminal:

```bash
# Tokenize a file
soma tokenize input.txt --method subword --output result.json

# Analyze text structure
soma analyze "Analyze this sentence for structural balance."
```

## 🏗️ Architecture

SOMA is modular by design, allowing you to use only what you need:

| Module                 | Purpose                                                                                                           |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **`soma`**             | The high-level wrapper and entry point for all standard operations.                                               |
| **`soma_core`**        | **Structural Core**: Handles metrics, pattern recognition, and hierarchy detection.                               |
| **`cognitive`**        | **AI Layer**: Contains reasoning engines, SLM (Small Language Model) architectures (`soma_gpt`), and verbalizers. |
| **`src`**              | **Engine Room**: The low-level implementations of parallel tokenizers and embedding generators.                   |
| **`semantic_trainer`** | **Training**: Tools for training custom semantic embeddings on your own corpora.                                  |

## 🔧 modules Overview

### 1. SOMA Core (`soma_core`)

The backbone of the system. It replaces simple regex splitting with structure-aware parsing.

- _Key Class_: `StructureHierarchy`
- _Capabilities_: Pattern building, Similarity metrics via `soma_core_metrics`.

### 2. Cognitive Layer (`cognitive`)

Where text meets reasoning.

- **Reasoning**: `soma_reasoner.py` enables logical deduction chains.
- **SLM**: `soma_gpt.py` provides a lightweight, trainable transformer implementation for specialized tasks.

### 3. Vector Integration

Seamlessly plug into vector databases.

- Built-in support for **Weaviate** and **ChromaDB**.
- Easy export of semantic embeddings to downstream ML tasks.

## 🤝 Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for details.

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add some amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Author**: Santosh Chavala
**Repository**: [https://github.com/chavalasantosh/SanVerse](https://github.com/chavalasantosh/SanVerse)
