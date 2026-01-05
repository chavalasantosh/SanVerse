# SanTOK - Advanced AI Tokenization Framework

## Overview

SanTOK is a comprehensive text tokenization system with mathematical analysis, semantic embeddings, and AI/ML capabilities. It provides multiple tokenization methods, embedding generation, training pipelines, and a full-featured API server.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py

# Or use CLI
python santok_cli.py --help
```

## Project Structure

| Folder              | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `src/`              | Core tokenization engine, embeddings, servers, training |
| `cognitive/`        | AI/ML: reasoning, SLM models, algorithms, graphs        |
| `santok/`           | High-level wrapper module                               |
| `santek_core/`      | Structure metrics system                                |
| `semantic_trainer/` | Enhanced semantic embeddings                            |
| `examples/`         | Usage examples                                          |
| `docs/`             | Documentation                                           |
| `training_data/`    | Training datasets                                       |
| `tests/`            | Test suite                                              |
| `scripts/`          | Deployment & setup scripts                              |
| `weaviate_codes/`   | Weaviate vector DB integration                          |

## Entry Points

| File                       | Purpose                    |
| -------------------------- | -------------------------- |
| `main.py`                  | Application entry point    |
| `run.py`                   | Start the API server       |
| `start.py`                 | Alternative startup script |
| `santok_cli.py`            | Command-line interface     |
| `train_santok_complete.py` | Train the complete model   |

## Key Features

- **Multiple Tokenization Methods**: Word, character, subword, byte-level, grammar-based
- **Semantic Embeddings**: Feature-based, hash-based, semantic, hybrid strategies
- **RESTful API**: FastAPI-based server with interactive documentation
- **SLM Models**: Small Language Models (SanTOK-GPT, Tiny-SLM)
- **Training Pipelines**: Vocabulary building, language model training
- **Vector Database**: ChromaDB, FAISS, Weaviate integration

## Documentation

See the `docs/` folder and the following guides:

- `SANTOK_TOKENIZATION_GUIDE.md` - Complete tokenization guide
- `SANTOK_EMBEDDINGS_GUIDE.md` - Embeddings documentation
- `RAILWAY_OPERATIONS_GUIDE.md` - Deployment guide
- `QUICK_SUMMARY.md` - Project overview

## Requirements

- Python 3.11+
- See `requirements.txt` for dependencies

## Author

Santosh Chavala

## License

See LICENSE file
