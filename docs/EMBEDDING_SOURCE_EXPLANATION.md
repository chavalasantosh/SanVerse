# Embedding Source Explanation

## How to Tell Which Embeddings You're Getting

SanTOK supports **3 different embedding strategies**. Here's how to identify which one is being used:

---

## 1. 🔢 Feature-Based (Default) - **SanTOK Math-Based**

**Source:** Pure SanTOK mathematical features  
**Uses Pretrained Models:** ❌ NO

### How It Works:
1. Extracts features from SanTOK tokens:
   - UIDs (64-bit unique identifiers)
   - Frontend digits (1-9)
   - Backend numbers (64-bit hashes)
   - Content IDs
   - Global IDs
   - Neighbor context (prev/next UIDs)
   - Token index
   - Stream type

2. Projects these features to embedding dimension using a learned projection matrix

3. Normalizes to unit vector

### Characteristics:
- ✅ **Deterministic** - Same token → same embedding
- ✅ **No external dependencies** - Works without any ML libraries
- ✅ **Fast** - ~100K tokens/second
- ✅ **Pure SanTOK** - 100% from SanTOK's math
- ❌ **No semantic meaning** - Purely mathematical

### How to Use:
```python
# Default strategy is feature_based
embedding_gen = SanTOKEmbeddingGenerator(
    strategy="feature_based",  # Default
    embedding_dim=768
)
```

### In Frontend:
- Strategy selector shows: "🔢 Feature-Based (SanTOK Math)"
- Badge shows: "🔢 SanTOK Math-Based"
- Info box says: "No pretrained models used - Pure mathematical transformation"

---

## 2. 🤖 Hybrid - **Pretrained Model + SanTOK**

**Source:** Combines sentence-transformers (pretrained) + SanTOK features  
**Uses Pretrained Models:** ✅ YES (sentence-transformers)

### How It Works:
1. Gets text embedding from sentence-transformers (pretrained model)
2. Gets feature embedding from SanTOK's mathematical features
3. Combines with weights (default: 70% text, 30% features)
4. Normalizes to unit vector

### Characteristics:
- ✅ **Semantic meaning** - From pretrained text embeddings
- ✅ **Preserves SanTOK features** - Still includes mathematical properties
- ⚠️ **Requires dependencies** - Needs sentence-transformers
- ⚠️ **Slower** - ~10K tokens/second
- ⚠️ **Less deterministic** - Depends on pretrained model

### How to Use:
```python
embedding_gen = SanTOKEmbeddingGenerator(
    strategy="hybrid",
    embedding_dim=768,
    text_model="sentence-transformers/all-MiniLM-L6-v2"
)
```

### In Frontend:
- Strategy selector shows: "🤖 Hybrid (Text + Math)"
- Badge shows: "🤖 Hybrid (Text + Math)"
- Info box says: "Uses pretrained model: sentence-transformers"

---

## 3. 🔐 Hash-Based - **Fast Hash**

**Source:** Cryptographic hash of SanTOK features  
**Uses Pretrained Models:** ❌ NO

### How It Works:
1. Creates hash string from all SanTOK features
2. Uses SHA-256 to generate fixed-size hash
3. Converts hash bytes to embedding vector
4. Normalizes to unit vector

### Characteristics:
- ✅ **Extremely fast** - ~200K tokens/second
- ✅ **Deterministic** - Same token → same embedding
- ✅ **No dependencies** - Pure Python
- ❌ **No semantic meaning** - Just hash
- ❌ **Poor similarity properties** - Hash collisions possible

### How to Use:
```python
embedding_gen = SanTOKEmbeddingGenerator(
    strategy="hash",
    embedding_dim=768
)
```

### In Frontend:
- Strategy selector shows: "🔐 Hash-Based"
- Badge shows: "🔐 Hash-Based"
- Info box says: "Fast, deterministic, no pretrained models"

---

## Quick Reference

| Strategy | Source | Pretrained Models? | Speed | Semantic? |
|----------|--------|-------------------|-------|-----------|
| **Feature-Based** | SanTOK Math | ❌ NO | Fast | ❌ No |
| **Hybrid** | Text + Math | ✅ YES | Slow | ✅ Yes |
| **Hash-Based** | Hash | ❌ NO | Very Fast | ❌ No |

---

## Default Behavior

**Default strategy is `feature_based`** - This means:
- ✅ You get **SanTOK's math-based embeddings** by default
- ✅ **No pretrained models** are used
- ✅ Works **without any ML dependencies**

If you want pretrained model embeddings, you must explicitly choose "Hybrid" strategy.

---

## How to Check in Code

```python
# Check which strategy is being used
print(f"Strategy: {embedding_gen.strategy}")

if embedding_gen.strategy == "feature_based":
    print("✅ Using SanTOK math-based logic")
    print("❌ No pretrained models")
elif embedding_gen.strategy == "hybrid":
    print("⚠️ Using pretrained sentence-transformers")
    print("✅ Also includes SanTOK features")
elif embedding_gen.strategy == "hash":
    print("✅ Using hash-based (no pretrained models)")
```

---

## Summary

**By default, embeddings come from SanTOK's math-based logic (feature-based).**

To use pretrained models, you must:
1. Install: `pip install sentence-transformers`
2. Select "Hybrid" strategy in UI or code
3. Then embeddings will combine pretrained text embeddings with SanTOK features

