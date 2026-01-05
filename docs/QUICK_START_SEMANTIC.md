# Quick Start: Semantic Embeddings

## 🚀 Run in 3 Steps

### Step 1: Train Model

```bash
python examples/train_semantic_embeddings.py
```

This will:
- Tokenize sample text with SanTOK
- Train semantic embeddings
- Save model to `santok_semantic_model.pkl`

### Step 2: Test Embeddings

```bash
python examples/use_semantic_embeddings.py
```

This will:
- Load trained model
- Generate embeddings for test text
- Show similarity comparison

### Step 3: Use in Your Code

```python
from src.embeddings import SanTOKEmbeddingGenerator
from src.core.core_tokenizer import TextTokenizer

# Load trained model
generator = SanTOKEmbeddingGenerator(
    strategy="semantic",
    semantic_model_path="santok_semantic_model.pkl"
)

# Tokenize and embed
tokenizer = TextTokenizer()
streams = tokenizer.build("Hello world")
token = streams["word"].tokens[0]

embedding = generator.generate(token)
print(f"Embedding: {embedding.shape}")  # (768,)
```

## 📝 Train on Your Own Data

Edit `examples/train_semantic_embeddings.py`:

```python
# Replace sample_text with your corpus
your_corpus = """
Your text data here...
Multiple documents work best.
"""

train_semantic_embeddings(
    text_corpus=your_corpus,
    output_model_path="my_model.pkl",
    epochs=20  # More epochs = better results
)
```

## ✅ That's It!

You now have NLP-understandable embeddings trained from SanTOK, **NO pretrained models needed!**

