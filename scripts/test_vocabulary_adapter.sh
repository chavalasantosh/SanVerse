#!/bin/bash
# Quick test script for vocabulary adapter backend

echo "🧪 Testing Vocabulary Adapter Backend"
echo "======================================"
echo ""

# Check if server is running
echo "1. Checking if server is running..."
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Server is running"
else
    echo "❌ Server is not running"
    echo "   Start it with: python src/servers/main_server.py"
    exit 1
fi

echo ""
echo "2. Testing quick endpoint..."
curl -s http://localhost:8000/test/vocabulary-adapter/quick | python -m json.tool

echo ""
echo "3. Testing custom request..."
curl -s -X POST http://localhost:8000/test/vocabulary-adapter \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world! SanTOK is amazing.",
    "model_name": "bert-base-uncased",
    "tokenizer_type": "word"
  }' | python -m json.tool

echo ""
echo "✅ Tests complete!"
echo ""
echo "💡 Tip: Open http://localhost:8000/docs for interactive API testing"

