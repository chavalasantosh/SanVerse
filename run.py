#!/usr/bin/env python3
"""
Cross-platform SOMA Run Script
Starts the SOMA API server with automatic environment detection
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Optional, NoReturn

# import soma config utilities
try:
    from soma.utils.config import Config
    from soma.utils.logging_config import setup_logging
    SOMA_UTILS_AVAILABLE = True
except ImportError:
    SOMA_UTILS_AVAILABLE = False

def print_colored(text: str, color: str = 'white') -> None:
    """Print colored text (works on most terminals)"""
    colors = {
        'green': '\033[0;32m',
        'yellow': '\033[1;33m',
        'red': '\033[0;31m',
        'blue': '\033[0;34m',
        'reset': '\033[0m'
    }
    if color in colors and sys.stdout.isatty():
        print(f"{colors[color]}{text}{colors['reset']}")
    else:
        print(text)

def check_python_version() -> None:
    """Check if Python version is 3.11 or higher"""
    if sys.version_info < (3, 11):
        print_colored(f"[ERROR] Python 3.11 or higher is required. Found: {sys.version}", 'red')
        sys.exit(1)
    print_colored(f"[INFO] Python version: {sys.version.split()[0]}", 'green')

def find_venv() -> str:
    """Find and activate virtual environment"""
    venv_paths = [
        Path('venv'),
        Path('.venv'),
        Path('env'),
    ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            if platform.system() == 'Windows':
                activate_script = venv_path / 'Scripts' / 'activate.bat'
                python_exe = venv_path / 'Scripts' / 'python.exe'
            else:
                activate_script = venv_path / 'bin' / 'activate'
                python_exe = venv_path / 'bin' / 'python'
            
            if python_exe.exists():
                print_colored(f"[INFO] Found virtual environment: {venv_path}", 'green')
                return str(python_exe)
    
    print_colored("[WARNING] No virtual environment found. Using system Python.", 'yellow')
    return sys.executable

def check_dependencies(python_exe: str) -> bool:
    """Check if required dependencies are installed"""
    if not isinstance(python_exe, str):
        raise TypeError(f"python_exe must be str, got {type(python_exe).__name__}")
    
    try:
        subprocess.run(
            [python_exe, '-c', 'import fastapi, uvicorn'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print_colored("[INFO] Dependencies are installed", 'green')
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print_colored("[ERROR] Dependencies not installed. Please run setup script first.", 'red')
        print_colored("  Linux/Mac: ./setup.sh", 'yellow')
        print_colored("  Windows: setup.bat", 'yellow')
        if isinstance(e, FileNotFoundError):
            print_colored(f"  Python executable not found: {python_exe}", 'red')
        return False

def check_port(port: int) -> None:
    """Check if port is available (basic check)"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            if result == 0:
                print_colored(f"[WARNING] Port {port} appears to be in use.", 'yellow')
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    sys.exit(1)
    except Exception:
        pass  # Port check failed, continue anyway

def main() -> None:
    """Main function"""
    print("=" * 50)
    print("SOMA API Server")
    print("=" * 50)
    print()
    
    # Check Python version
    check_python_version()
    
    # Find virtual environment
    python_exe = find_venv()
    
    # Check dependencies
    if not check_dependencies(python_exe):
        sys.exit(1)
    
    # Get port from environment using config utility
    try:
        if SOMA_UTILS_AVAILABLE:
            from soma.utils.validation import validate_port
            port_str = os.environ.get('PORT', '8000')
            port = validate_port(int(port_str), param_name='PORT')
        else:
            port = int(os.environ.get('PORT', 8000))
            if port < 1 or port > 65535:
                raise ValueError(f"Port must be between 1 and 65535, got {port}")
    except (ValueError, TypeError) as e:
        print_colored(f"[ERROR] Invalid PORT environment variable: {e}", 'red')
        sys.exit(1)
    
    check_port(port)
    
    # Print server info
    print()
    print_colored(f"[INFO] Starting SOMA API Server on port {port}...", 'green')
    print_colored(f"[INFO] Server will be available at: http://localhost:{port}", 'green')
    print_colored(f"[INFO] API Documentation at: http://localhost:{port}/docs", 'green')
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    # Set PORT environment variable
    os.environ['PORT'] = str(port)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Start the server
    try:
        # Run start.py as a script
        start_script = script_dir / 'start.py'
        if not start_script.exists():
            print_colored("[ERROR] start.py not found", 'red')
            sys.exit(1)
        
        # Execute start.py
        exec(open(start_script).read())
    except KeyboardInterrupt:
        print_colored("\n[INFO] Server stopped by user", 'yellow')
    except Exception as e:
        print_colored(f"[ERROR] Failed to start server: {e}", 'red')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
