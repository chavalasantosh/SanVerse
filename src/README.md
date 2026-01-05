# src/ - Core Source Code

## Overview

This is the core source code for the SOMA tokenization framework.

## Modules

| Module            | Description                                                                   |
| ----------------- | ----------------------------------------------------------------------------- |
| `core/`           | Core tokenization engine - base_tokenizer, core_tokenizer, parallel_tokenizer |
| `embeddings/`     | Embedding generation - embedding_generator, vector_store, semantic_trainer    |
| `servers/`        | API servers - main_server, api_server, lightweight_server                     |
| `training/`       | Training pipelines - vocabulary_builder, language_model_trainer               |
| `structure/`      | Structure analysis - pattern_builder, structure_hierarchy                     |
| `integration/`    | External integrations - source_map_integration, vocabulary_adapter            |
| `compression/`    | Compression algorithms                                                        |
| `cli/`            | Command-line interface                                                        |
| `interpretation/` | Data interpretation                                                           |
| `utils/`          | Utility functions                                                             |

## Key Files

- `core/core_tokenizer.py` - Main tokenization engine (3000+ lines)
- `embeddings/embedding_generator.py` - Embedding generation
- `servers/main_server.py` - FastAPI server
- `training/vocabulary_builder.py` - Vocabulary building
