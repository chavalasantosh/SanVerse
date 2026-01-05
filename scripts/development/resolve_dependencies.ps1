# PowerShell script to resolve Python dependency conflicts
# This script installs packages in the correct order to minimize conflicts

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Resolving Python Dependency Conflicts" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Upgrade pip and setuptools
Write-Host "[1/8] Upgrading pip and setuptools..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Step 2: Install core dependencies first (foundation)
Write-Host "[2/8] Installing core dependencies..." -ForegroundColor Yellow
pip install "numpy>=1.24.3,<2.3.0" "pandas>=2.1.3,<=2.3.1" "certifi>=2017.4.17,<2025.4.26"
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Step 3: Install pydantic (compatible version for most packages)
Write-Host "[3/8] Installing pydantic (compatible version)..." -ForegroundColor Yellow
pip install "pydantic>=2.5.0,<2.10.0" "pydantic-core>=2.33.0,<2.34.0"
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Step 4: Install HTTP clients
Write-Host "[4/8] Installing HTTP clients..." -ForegroundColor Yellow
pip install "httpx>=0.28.1,<1.0.0" "requests>=2.31.0" "fsspec>=2023.5.0,<=2025.9.0"
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Step 5: Install PyTorch ecosystem (specific version for compatibility)
Write-Host "[5/8] Installing PyTorch ecosystem..." -ForegroundColor Yellow
pip install "torch==2.7.1" "torchvision==0.22.1" "torchaudio==2.7.1"
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Step 6: Install transformers ecosystem
Write-Host "[6/8] Installing transformers ecosystem..." -ForegroundColor Yellow
pip install "transformers==4.51.3" "tokenizers>=0.21.0,<0.22.0" "sentence-transformers>=2.2.0,<6.0.0"
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Step 7: Install langchain ecosystem (compatible versions)
Write-Host "[7/8] Installing langchain ecosystem..." -ForegroundColor Yellow
pip install "langchain-core>=0.3.68,<1.0.0" "langchain>=0.3.0,<1.0.0" "langchain-community>=0.3.0,<1.0.0"
pip install "langchain-google-genai>=2.0.10" "langchain-groq>=0.3.6" "langchain-huggingface>=0.3.0" "langchain-openai>=0.3.28"
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Step 8: Install remaining dependencies
Write-Host "[8/8] Installing remaining dependencies..." -ForegroundColor Yellow
pip install "pillow>=8.0.0,<12.0.0" "pyarrow>=4.0.0,<21.0.0" "aiofiles>=22.0,<25.0"
pip install "python-multipart>=0.0.18" "click>=7.1.0,<8.2.0"
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

# Final: Install from requirements_resolved.txt
Write-Host "Installing from requirements_resolved.txt..." -ForegroundColor Yellow
pip install -r requirements_resolved.txt
Write-Host "✓ Done" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dependency Resolution Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Checking for remaining conflicts..." -ForegroundColor Yellow
pip check
Write-Host ""
Write-Host "Note: Some packages may still show conflicts if they have" -ForegroundColor Yellow
Write-Host "incompatible requirements. Check the output above." -ForegroundColor Yellow

