# SOMA - Advanced Tokenization & Intelligence Framework

## Overview

**SOMA** is a comprehensive text tokenization system with mathematical analysis, semantic embeddings, and Small Language Models (SLMs). It provides multiple tokenization methods, embedding generation, training pipelines, and a full-featured API server.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py

# Or use CLI
python soma_cli.py --help
```

## Project Structure

| Folder              | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `src/`              | Core tokenization engine, embeddings, servers, training |
| `cognitive/`        | Architecture reasoning, SLM models, algorithms, graphs  |
| `soma/`             | High-level wrapper module                               |
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
| `soma_cli.py`              | Command-line interface     |
| `train_santok_complete.py` | Train the complete model   |

## Key Features

- **Multiple Tokenization Methods**: Word, character, subword, byte-level, grammar-based
- **Semantic Embeddings**: Feature-based, hash-based, semantic, hybrid strategies
- **SOMA-GPT**: Small Language Models for efficient inference
- **RESTful API**: FastAPI-based server with interactive documentation
- **Vector Database**: Integration with Weaviate and others

## Documentation

See the `docs/` folder for detailed guides.

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Author

Santosh Chavala

## License

MIT License
