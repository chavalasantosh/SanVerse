#!/usr/bin/env python3
"""
Package Backend Code for Sharing

This script creates a clean backend-only package for sharing with colleagues.
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_backend_package():
    """Create a backend-only package."""
    
    print("=" * 80)
    print("PACKAGING BACKEND CODE FOR SHARING")
    print("=" * 80)
    print()
    
    # Create package directory
    package_name = "santok_backend"
    package_dir = Path(package_name)
    
    # Remove old package if exists
    if package_dir.exists():
        print(f"[*] Removing old package directory: {package_name}")
        shutil.rmtree(package_dir)
    
    print(f"[*] Creating package directory: {package_name}")
    package_dir.mkdir()
    
    # Files and folders to include
    # Copy from backend/ folder (all backend code is there)
    items_to_copy = [
        ("backend/src", "src"),  # All backend code
        ("backend/santok", "santok"),  # Main package
        ("backend/requirements.txt", "requirements.txt"),  # Dependencies
        ("backend/setup.py", "setup.py"),  # Package setup
        ("backend/README.md", "README.md"),  # README
    ]
    
    # Copy files and folders
    print("\n[*] Copying files...")
    for src, dst in items_to_copy:
        src_path = Path(src)
        dst_path = package_dir / dst
        
        if not src_path.exists():
            print(f"  [WARNING] {src} not found, skipping...")
            continue
        
        try:
            if src_path.is_dir():
                print(f"  [*] Copying directory: {src} -> {dst}")
                shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns(
                    '__pycache__',
                    '*.pyc',
                    '*.pyo',
                    '*.pyd',
                    '.pytest_cache',
                    '.mypy_cache',
                    '*.egg-info',
                    '.git',
                    '.DS_Store',
                    '*.swp',
                    '*.swo',
                    '*~'
                ))
            else:
                print(f"  [*] Copying file: {src} -> {dst}")
                shutil.copy2(src_path, dst_path)
            print(f"  [OK] Copied: {src}")
        except Exception as e:
            print(f"  [ERROR] Error copying {src}: {e}")
    
    # Create README for backend
    readme_content = """# SanTOK Backend

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Backend Server
```bash
python src/servers/main_server.py
```

### 3. Access the API
- **API Server:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 📁 Structure

```
santok_backend/
├── src/              # Backend code
│   ├── servers/     # API servers
│   ├── core/        # Core tokenization
│   ├── embeddings/  # Embeddings & vector stores
│   └── ...
├── santok/          # Main package
├── requirements.txt # Python dependencies
└── setup.py         # Package setup
```

## 🔧 Backend Components

### API Servers (`src/servers/`)
- `main_server.py` - Main FastAPI server (PRIMARY)
- `lightweight_server.py` - Lightweight server
- `api_server.py` - API server
- `simple_server.py` - Simple server

### Core Tokenization (`src/core/`)
- `core_tokenizer.py` - Main tokenization engine
- `base_tokenizer.py` - Base tokenizer class
- `parallel_tokenizer.py` - Parallel processing

### Embeddings (`src/embeddings/`)
- `embedding_generator.py` - Generate embeddings
- `vector_store.py` - Vector database (FAISS, ChromaDB)
- `semantic_trainer.py` - Train semantic embeddings
- `inference_pipeline.py` - Inference pipeline

## 📡 API Endpoints

### Main Server (http://localhost:8000)

- `GET /` - Health check
- `POST /tokenize` - Tokenize text
- `POST /reconstruct` - Reconstruct text from tokens
- `POST /embed` - Generate embeddings
- `GET /docs` - API documentation (Swagger UI)

## 📚 Documentation

See `backend/` folder for detailed documentation:
- `backend/START_HERE.md` - Start here
- `backend/QUICK_START.md` - Quick start guide
- `backend/INDEX.md` - Code index
- `backend/SUMMARY.md` - Summary

## 🎯 Usage Examples

### Tokenize Text
```bash
curl -X POST "http://localhost:8000/tokenize" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Hello world", "tokenizer_type": "space"}'
```

### Generate Embeddings
```bash
curl -X POST "http://localhost:8000/embed" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Hello world", "tokenizer_type": "space"}'
```

## ✅ Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 🆘 Troubleshooting

### Server won't start?
1. Check Python version: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Check if port 8000 is available

### Import errors?
1. Make sure you're in the package directory
2. Check that `src/` directory exists
3. Verify all dependencies are installed

## 📞 Support

For issues or questions, refer to the documentation in `backend/` folder.

---
**SanTOK Backend - Text Tokenization System**
"""
    
    readme_path = package_dir / "README.md"
    print(f"\n[*] Creating README.md...")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  [OK] Created: README.md")
    
    # Create ZIP file
    zip_name = f"{package_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    print(f"\n[*] Creating ZIP file: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            # Skip hidden files and cache
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', '.pytest_cache']]
            
            for file in files:
                if file.endswith(('.pyc', '.pyo', '.pyd', '.swp', '.swo', '~')):
                    continue
                
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"  [OK] Created: {zip_name}")
    
    # Get package size
    package_size = sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file())
    zip_size = os.path.getsize(zip_name)
    
    print(f"\n[*] Package Statistics:")
    print(f"  - Package directory: {package_size / 1024 / 1024:.2f} MB")
    print(f"  - ZIP file: {zip_size / 1024 / 1024:.2f} MB")
    print(f"  - Location: {package_dir.absolute()}")
    print(f"  - ZIP location: {Path(zip_name).absolute()}")
    
    print(f"\n[SUCCESS] Backend package created successfully!")
    print(f"\n[*] Next Steps:")
    print(f"  1. Share the ZIP file: {zip_name}")
    print(f"  2. Or share the folder: {package_name}")
    print(f"  3. Your colleague can extract and run: python src/servers/main_server.py")
    print(f"\n[*] Package includes:")
    print(f"  [OK] Backend code (src/)")
    print(f"  [OK] Main package (santok/)")
    print(f"  [OK] Dependencies (requirements.txt)")
    print(f"  [OK] Setup (setup.py)")
    print(f"  [OK] Documentation (backend/)")
    print(f"  [NO] No frontend")
    print(f"  [NO] No examples")
    print(f"  [NO] No output data")

if __name__ == "__main__":
    create_backend_package()
