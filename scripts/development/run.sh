#!/bin/bash
# SanTOK Run Script for Linux/Mac
# Starts the SanTOK API server

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "SanTOK API Server"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Virtual environment not found."
    echo "Running setup.sh first..."
    ./setup.sh
fi

# Activate virtual environment
echo -e "${YELLOW}[INFO]${NC} Activating virtual environment..."
source venv/bin/activate

# Check if Python dependencies are installed
echo -e "${YELLOW}[INFO]${NC} Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null || {
    echo -e "${RED}[ERROR]${NC} Dependencies not installed. Running setup..."
    pip install -r requirements.txt
}

# Get port from environment or use default
PORT=${PORT:-8000}

# Check if port is in use
if command -v lsof &> /dev/null; then
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}[WARNING]${NC} Port $PORT is already in use."
        echo "Use PORT=8001 ./run.sh to use a different port"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

echo -e "${GREEN}[INFO]${NC} Starting SanTOK API Server..."
echo -e "${GREEN}[INFO]${NC} Server will be available at: http://localhost:$PORT"
echo -e "${GREEN}[INFO]${NC} API Documentation at: http://localhost:$PORT/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Export PORT for start.py
export PORT

# Start the server
python start.py

