#!/bin/bash
# Test setup script for Linux/Mac
# Runs verification and basic server test

set -e

echo "=========================================="
echo "SanTOK Setup Test"
echo "=========================================="
echo ""

# Run verification
echo "Running installation verification..."
python3 verify_installation.py
VERIFY_EXIT=$?

if [ $VERIFY_EXIT -ne 0 ]; then
    echo ""
    echo "Verification failed. Please fix issues before testing server."
    exit 1
fi

echo ""
echo "=========================================="
echo "Testing server startup..."
echo "=========================================="
echo ""

# Check if server can start (quick test)
timeout 10 python3 start.py &
SERVER_PID=$!

sleep 3

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo "✓ Server started successfully"
    kill $SERVER_PID 2>/dev/null || true
    echo "✓ Server stopped successfully"
    echo ""
    echo "Setup test PASSED!"
    exit 0
else
    echo "✗ Server failed to start"
    exit 1
fi

