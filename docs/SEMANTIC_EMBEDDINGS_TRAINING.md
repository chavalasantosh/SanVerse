# Semantic Embeddings Training (NLP-Understandable, NO Pretrained Models)

## Overview

SanTOK can generate **semantic embeddings** that are NLP-understandable by training on your data, **WITHOUT using pretrained models** like BERT or sentence-transformers.

## How It Works

### 1. Self-Supervised Learning from SanTOK Structure

The semantic trainer learns semantic relationships from:
- **Co-occurrence patterns**: Which tokens appear together
- **Neighbor relationships**: `prev_uid`, `next_uid` from SanTOK
- **Content similarity**: Tokens with similar `content_id`
- **Context windows**: Tokens in the same stream/sequence

### 2. Training Process

```python
from src.embeddings.semantic_trainer import SanTOKSemanticTrainer
from src.core.core_tokenizer import TextTokenizer

# 1. Tokenize your text corpus
tokenizer = TextTokenizer()
streams = tokenizer.build("Your text corpus here...")

# 2. Collect all tokens
all_tokens = []
for stream in streams.values():
    all_tokens.extend(stream.tokens)

# 3. Train semantic embeddings
trainer = SanTOKSemanticTrainer(
    embedding_dim=768,
    window_size=5,
    epochs=10
)

# Build vocabulary from tokens
trainer.build_vocab(all_tokens)

# Build co-occurrence matrix from SanTOK's neighbor structure
trainer.build_cooccurrence(all_tokens)

# Train embeddings (learns semantic relationships)
trainer.train(all_tokens)

# 4. Save trained model
trainer.save("santok_semantic_model.pkl")
```

### 3. Using Trained Embeddings

```python
from src.embeddings import SanTOKEmbeddingGenerator

# Load trained semantic model
generator = SanTOKEmbeddingGenerator(
    strategy="semantic",
    embedding_dim=768,
    semantic_model_path="santok_semantic_model.pkl"
)

# Generate semantic embeddings
tokenizer = TextTokenizer()
streams = tokenizer.build("Hello world")
token = streams["word"].tokens[0]

embedding = generator.generate(token)  # NLP-understandable embedding!
```

## Key Features

### ✅ What It Does:
- **Learns semantic relationships** from your data
- **Uses SanTOK's structure** (neighbors, content_id, etc.)
- **NLP-understandable** embeddings
- **NO pretrained models** - trains from scratch
- **Self-supervised** - learns from co-occurrence patterns

### ❌ What It Doesn't Use:
- ❌ BERT
- ❌ sentence-transformers
- ❌ Any pretrained models
- ❌ External training data (uses YOUR data)

## Training on Large Corpus

For best results, train on a large text corpus:

```python
# Train on multiple documents
all_tokens = []

for document in your_documents:
    streams = tokenizer.build(document)
    for stream in streams.values():
        all_tokens.extend(stream.tokens)

# Train once on all tokens
trainer = SanTOKSemanticTrainer(embedding_dim=768, epochs=20)
trainer.build_vocab(all_tokens)
trainer.build_cooccurrence(all_tokens)
trainer.train(all_tokens)
trainer.save("santok_semantic_model.pkl")
```

## Comparison

| Aspect | Feature-Based | Semantic (Trained) | Hybrid |
|--------|---------------|-------------------|--------|
| **Semantic Meaning** | ❌ No | ✅ Yes | ✅ Yes |
| **Pretrained Models** | ❌ No | ❌ No | ✅ Yes |
| **Training Required** | ❌ No | ✅ Yes | ❌ No |
| **NLP-Understandable** | ❌ No | ✅ Yes | ✅ Yes |
| **Uses SanTOK Math** | ✅ Yes | ✅ Yes | ✅ Yes |

## Summary

**Semantic embeddings** = Train on your data using SanTOK's structure → Learn semantic relationships → Generate NLP-understandable embeddings

**NO pretrained models needed!**

