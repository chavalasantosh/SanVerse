#!/bin/bash
# SanTOK Automated Setup Script for Linux/Mac
# This script sets up the development environment and installs all dependencies

set -e  # Exit on error

echo "=========================================="
echo "SanTOK Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}→${NC} $1"
}

# Check if Python is installed
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    print_error "Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_info "Found Python version: $PYTHON_VERSION"

# Check if version is 3.11 or higher
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    print_error "Python 3.11 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

print_success "Python version is compatible"

# Check if pip is installed
print_info "Checking pip installation..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    print_error "pip is not installed. Installing pip..."
    $PYTHON_CMD -m ensurepip --upgrade
fi

print_success "pip is available"

# Upgrade pip
print_info "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip --quiet
print_success "pip upgraded"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip in virtual environment
print_info "Upgrading pip in virtual environment..."
pip install --upgrade pip --quiet

# Install dependencies
print_info "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies installed"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Check if Node.js is needed (optional, for frontend)
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    print_info "Frontend directory detected. Node.js dependencies are optional."
    if command -v npm &> /dev/null; then
        read -p "Install Node.js dependencies? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installing Node.js dependencies..."
            cd frontend
            npm install
            cd ..
            print_success "Node.js dependencies installed"
        fi
    fi
fi

# Verify installation
print_info "Verifying installation..."
if [ -f "verify_installation.py" ]; then
    $PYTHON_CMD verify_installation.py
else
    print_info "Running basic verification..."
    $PYTHON_CMD -c "import sys; print(f'Python: {sys.version}')"
    $PYTHON_CMD -c "import fastapi; print('FastAPI: OK')" 2>/dev/null || print_error "FastAPI not installed"
    $PYTHON_CMD -c "import uvicorn; print('Uvicorn: OK')" 2>/dev/null || print_error "Uvicorn not installed"
fi

echo ""
echo "=========================================="
print_success "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the server: ./run.sh"
echo "  3. Or manually: python start.py"
echo ""
echo "The server will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""

