#!/usr/bin/env python3
"""
SanTOK Installation Script
Automated setup and installation for the SanTOK framework
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found. Please install Node.js 16+")
    return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        sys.exit(1)

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("\n📦 Installing Node.js dependencies...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        os.chdir(frontend_dir)
        subprocess.run(['npm', 'install'], check=True)
        os.chdir("..")
        print("✅ Node.js dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = [
        "logs",
        "temp",
        "data/outputs",
        "data/samples",
        "data/benchmarks",
        "config",
        "build",
        "dist"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")

def create_config_files():
    """Create default configuration files"""
    print("\n⚙️ Creating configuration files...")
    
    # Server config
    server_config = {
        "host": "0.0.0.0",
        "port": 8000,
        "debug": False,
        "workers": 1
    }
    
    with open("config/server.json", "w") as f:
        import json
        json.dump(server_config, f, indent=2)
    
    # Performance config
    performance_config = {
        "chunk_size": 50000,
        "max_memory": 100000000,
        "timeout": 30
    }
    
    with open("config/performance.json", "w") as f:
        import json
        json.dump(performance_config, f, indent=2)
    
    print("✅ Configuration files created")

def run_tests():
    """Run basic tests to verify installation"""
    print("\n🧪 Running tests...")
    try:
        # Test core functionality
        sys.path.insert(0, "src")
        from core.core_tokenizer import tokenize_text, reconstruct_from_tokens
        
        test_text = "Hello, world!"
        tokens = tokenize_text(test_text, "word")
        reconstructed = reconstruct_from_tokens(tokens, "word")
        
        if reconstructed == test_text:
            print("✅ Core functionality test passed")
        else:
            print("❌ Core functionality test failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def main():
    """Main installation function"""
    print("[START] SanTOK Installation Script")
    print("=" * 40)
    
    # Check prerequisites
    check_python_version()
    node_available = check_node_version()
    
    # Install dependencies
    install_python_dependencies()
    if node_available:
        install_node_dependencies()
    
    # Setup directories and config
    create_directories()
    create_config_files()
    
    # Run tests
    if run_tests():
        print("\n🎉 Installation completed successfully!")
        print("\nNext steps:")
        print("1. Run the application: python main.py")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Read the documentation: docs/")
    else:
        print("\n❌ Installation completed with errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
