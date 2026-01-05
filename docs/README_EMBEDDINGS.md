# SanTOK Embeddings - Quick Start Guide

## Overview

SanTOK now supports **embedding generation** and **inference-ready pipelines**! This enables:

- ✅ Generate embeddings from SanTOK tokens
- ✅ Store embeddings in vector databases
- ✅ Perform similarity search
- ✅ Use for ML inference

## Installation

```bash
# Install embedding dependencies
pip install sentence-transformers chromadb
# OR for high-performance option:
pip install sentence-transformers faiss-cpu
```

## Quick Start

### Basic Embedding Generation

```python
from src.core.core_tokenizer import TextTokenizer
from src.embeddings import SanTOKEmbeddingGenerator

# Initialize
tokenizer = TextTokenizer(seed=42, embedding_bit=False)
embedding_gen = SanTOKEmbeddingGenerator(
    strategy="feature_based",  # or "hybrid", "hash"
    embedding_dim=768
)

# Tokenize and generate embeddings
text = "Hello world, this is SanTOK!"
streams = tokenizer.build(text)

for stream_name, token_stream in streams.items():
    for token in token_stream.tokens:
        embedding = embedding_gen.generate(token)
        print(f"Token: {token.text}")
        print(f"Embedding shape: {embedding.shape}")
```

### Vector Database Storage

```python
from src.embeddings import ChromaVectorStore, SanTOKInferencePipeline

# Initialize pipeline
vector_store = ChromaVectorStore(
    collection_name="santok_embeddings",
    persist_directory="./vector_db"
)

pipeline = SanTOKInferencePipeline(
    embedding_generator=embedding_gen,
    vector_store=vector_store,
    tokenizer=tokenizer
)

# Process and store documents
pipeline.process_text("Machine learning is fascinating")
pipeline.process_text("Natural language processing enables AI")

# Search for similar content
results = pipeline.similarity_search("artificial intelligence", top_k=5)
for result in results:
    print(f"Found: {result['text']}")
```

## Embedding Strategies

### 1. Feature-Based (Deterministic)
- Uses SanTOK's mathematical features (UIDs, digits, backend numbers)
- Fast, deterministic, reproducible
- No external dependencies

```python
embedding_gen = SanTOKEmbeddingGenerator(
    strategy="feature_based",
    embedding_dim=768
)
```

### 2. Hybrid (Semantic + Features)
- Combines text embeddings with SanTOK features
- Better semantic understanding
- Requires sentence-transformers

```python
embedding_gen = SanTOKEmbeddingGenerator(
    strategy="hybrid",
    embedding_dim=768,
    text_model="sentence-transformers/all-MiniLM-L6-v2",
    feature_weights={"text": 0.7, "features": 0.3}
)
```

### 3. Hash-Based (Fast)
- Cryptographic hash-based embeddings
- Extremely fast
- Deterministic but no semantic meaning

```python
embedding_gen = SanTOKEmbeddingGenerator(
    strategy="hash",
    embedding_dim=768
)
```

## Vector Database Options

### ChromaDB (Recommended for most users)
- Easy to use
- Built-in persistence
- Metadata filtering

```python
from src.embeddings import ChromaVectorStore

vector_store = ChromaVectorStore(
    collection_name="santok_embeddings",
    persist_directory="./vector_db"
)
```

### FAISS (High Performance)
- Extremely fast
- Memory efficient
- Best for large datasets

```python
from src.embeddings import FAISSVectorStore

vector_store = FAISSVectorStore(
    collection_name="santok_embeddings",
    embedding_dim=768
)
```

## Complete Example

See `examples/embedding_example.py` for full examples including:
- Basic embedding generation
- Vector database storage
- Similarity search
- Document-level embeddings

## Documentation

- **Design Document**: `docs/EMBEDDING_SYSTEM_DESIGN.md`
- **Implementation Plan**: `docs/INFERENCE_READY_PLAN.md`

## What This Solves

**Before**: SanTOK tokens were just IDs - useless for inference
**Now**: SanTOK tokens → embeddings → inference-ready!

The system:
- ✅ Preserves SanTOK's mathematical properties
- ✅ Enables similarity search
- ✅ Supports ML inference
- ✅ Works with vector databases
- ✅ Provides end-to-end pipeline

## Next Steps

1. Try the examples: `python examples/embedding_example.py`
2. Read the design document for details
3. Integrate into your workflow
4. Experiment with different strategies

