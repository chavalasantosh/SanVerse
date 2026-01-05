# 🚀 SanVerse: New Laptop Setup Guide

## Phase 1: Cloning & Installation

**1. Clone the Repository**
Open your terminal (PowerShell or Command Prompt) and run:

```bash
# Clone the repo
git clone https://github.com/chavalasantosh/SanVerse.git

# Enter the directory
cd SanVerse
```

**2. Create a Virtual Environment (Recommended)**
Isolate your dependencies to avoid conflicts:

```bash
# Create virtual environment named 'venv'
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate
# Activate it (Mac/Linux)
# source venv/bin/activate
```

**3. Install Dependencies**
Install the package in "editable" mode so you can code and test immediately:

```bash
# Install SOMA and all dependencies
pip install -e .

# Verify installation
python -c "import soma; print(f'SOMA v{soma.__version__} installed successfully!')"
```

---

## Phase 2: Verification (Do this first)

Verify that your environment is healthy and the code is working:

**1. Run the SanTEK Core Demos**
These confirm that the core logic we migrated is functioning correctly.

```bash
# Test Core Tokenizer & Structure
python examples/demo_core.py

# Test Hierarchical Structure
python examples/demo_structure.py
```

**2. Verify Training Data Access**
Check if the restored data is visible:

```bash
# List the restored datasets
ls data/manga_anime_data
ls data/user_datasets
```

_(You should see `combined_manga_anime.txt` and `all_user_datasets.txt`)_

---

## Phase 3: Execution Points (Start Working)

Here are the specific commands to run the major components of SOMA:

### 1. 🧠 Train Your LLM (The Big Task)

You have the complete training script and data ready.

**Option A: Train on User Datasets (Bengaluru Companies etc.)**

```bash
python train_soma_complete.py --data data/user_datasets/all_user_datasets.txt --epochs 10 --output models/user_model_v1
```

**Option B: Train on Manga/Anime Data**

```bash
python train_soma_complete.py --data data/manga_anime_data/combined_manga_anime.txt --epochs 5 --output models/manga_model_v1
```

**Option C: Auto-Detect Data**

```bash
# Will check data/ folders automatically
python train_soma_complete.py
```

### 2. 📦 Publish to PyPI (If you start a new version)

If you make changes and want to release v1.0.6:

1.  Update version in `setup.py` and `soma/__init__.py`.
2.  Push to GitHub (The action will fail if you don't tag, but you can upload manually).
3.  **Manual Upload** (Reliable method):

    ```bash
    # Build
    python setup.py sdist bdist_wheel

    # Upload
    twine upload dist/*
    # Username: __token__
    # Password: <Your-PyPI-API-Token>
    ```

---

## Phase 4: Critical Documentation

When you need to understand the Deep Logic, open these files in the root directory:

1.  **`SANTOK_TOKENIZATION_GUIDE.md`** (Root)

    - **What it is:** The "Bible" of your tokenization logic (2,440 lines).
    - **Use for:** Understanding the 9 tokenization methods, UID generation, and math.

2.  **`SANTOK_EMBEDDINGS_GUIDE.md`** (Root)

    - **What it is:** Guide to how SOMA handles vector embeddings.

3.  **`docs/guides/`** (Folder)
    - Contains copies of all other specialized guides (Railway, Metrics, etc.).

---

## Phase 5: Troubleshooting (Common Issues)

- **"Module not found: soma"**:
  - _Fix:_ Make sure you activated your venv (`.\venv\Scripts\activate`) and ran `pip install -e .`
- **"File not found: combined_manga_anime.txt"**:
  - _Fix:_ Ensure you are running the command from the root `SanVerse` directory.
- **"Out of Memory (OOM)"**:
  - _Fix:_ Reduce batch size in training: `python train_soma_complete.py --batch_size 4 ...`
