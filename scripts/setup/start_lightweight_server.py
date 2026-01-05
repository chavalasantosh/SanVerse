#!/usr/bin/env python3
"""
Start the Simple SOMA Tokenizer Backend Server
Uses only standard library - no external dependencies
"""

import subprocess
import sys
import os

def check_backend_files():
    """Check if required backend files exist"""
    required_files = [
        "core_tokenizer.py",
        "lightweight_server.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"[ERROR] Missing required files: {', '.join(missing_files)}")
        print("Please run this script from the project root directory.")
        return False
    
    return True

def start_server():
    """Start the simple HTTP server"""
    print("[START] Starting Simple SOMA Tokenizer Backend Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "lightweight_server.py"])
    except KeyboardInterrupt:
        print("\n[STOP] Server stopped by user")
    except Exception as e:
        print(f"[ERROR] Error starting server: {e}")

if __name__ == "__main__":
    print("[START] SOMA Tokenizer Simple Backend Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not check_backend_files():
        sys.exit(1)
    
    # Start server
    start_server()
