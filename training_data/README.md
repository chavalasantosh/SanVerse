# training_data/ - Training Datasets

## Overview

Training datasets for the SOMA tokenization and language models.

## Contents

| Folder       | Description             |
| ------------ | ----------------------- |
| `arxiv/`     | Academic papers dataset |
| `books/`     | Book corpus             |
| `wikipedia/` | Wikipedia dataset       |
| `code/`      | Code samples            |
| `news/`      | News articles           |
| `custom/`    | Custom datasets         |

## Usage

Training data is used by:

- `train_soma_complete.py` - Complete model training
- `src/training/vocabulary_builder.py` - Vocabulary building
- `src/training/language_model_trainer.py` - Language model training
