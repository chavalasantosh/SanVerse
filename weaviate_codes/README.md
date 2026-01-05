# weaviate_codes/ - Weaviate Vector DB Integration

## Overview

Integration code for Weaviate vector database.

## Files

| File                       | Description                          |
| -------------------------- | ------------------------------------ |
| `weaviate_vector_store.py` | Weaviate vector store implementation |
| `example_usage.py`         | Usage examples                       |
| `test_connection.py`       | Connection testing                   |

## Usage

```python
from weaviate_codes import WeaviateVectorStore

store = WeaviateVectorStore(url="http://localhost:8080")
store.add_embeddings(embeddings, texts)
results = store.search(query_embedding, top_k=5)
```
