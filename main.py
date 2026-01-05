#!/usr/bin/env python3
"""
Main entry point for Railway deployment
This file exists to satisfy Railway's Railpack auto-detection
Railway tries to run: uvicorn main:app
So we need an 'app' variable here that points to our FastAPI app
"""
import sys
import os

# Add current directory and src to path (same as start.py does)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app from main_server
# This will work because main_server.py adds src to path internally
try:
    from src.servers.main_server import app
    # Now Railway can run: uvicorn main:app
    print("[OK] Successfully imported app from main_server", file=sys.stderr)
except ImportError as e:
    print(f"[ERROR] Failed to import app from main_server: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    # Don't exit - let uvicorn handle the error
    raise
