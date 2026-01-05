#!/usr/bin/env python3
"""
Execute All Python Files in Current Directory and Subdirectories
Saves all output to a log file
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import traceback

def find_all_python_files(root_dir):
    """Find all Python files recursively"""
    python_files = []
    root_path = Path(root_dir)
    
    for py_file in root_path.rglob("*.py"):
        # Skip certain files
        if any(skip in str(py_file) for skip in [
            "__pycache__",
            ".pyc",
            "run_all_python.py",  # Don't run itself
            "venv",
            "env",
            ".git"
        ]):
            continue
        python_files.append(py_file)
    
    return sorted(python_files)

def execute_python_file(file_path, log_file):
    """Execute a Python file and capture all output"""
    file_path_str = str(file_path)
    relative_path = file_path.relative_to(Path.cwd())
    
    print(f"\n{'='*80}")
    print(f"Executing: {relative_path}")
    print(f"{'='*80}")
    
    log_file.write(f"\n{'='*80}\n")
    log_file.write(f"File: {relative_path}\n")
    log_file.write(f"Full Path: {file_path_str}\n")
    log_file.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write(f"{'='*80}\n\n")
    log_file.flush()
    
    try:
        # Execute the Python file
        result = subprocess.run(
            [sys.executable, file_path_str],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout per file
            cwd=str(file_path.parent)
        )
        
        # Write stdout
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
            log_file.write("=== STDOUT ===\n")
            log_file.write(result.stdout)
            log_file.write("\n")
        
        # Write stderr
        if result.stderr:
            print("STDERR:")
            print(result.stderr, file=sys.stderr)
            log_file.write("=== STDERR ===\n")
            log_file.write(result.stderr)
            log_file.write("\n")
        
        # Write return code
        return_code = result.returncode
        status = "✅ SUCCESS" if return_code == 0 else f"❌ FAILED (exit code: {return_code})"
        print(f"\nStatus: {status}")
        
        log_file.write(f"\n=== EXIT CODE: {return_code} ===\n")
        log_file.write(f"Status: {status}\n")
        log_file.flush()
        
        return return_code == 0
        
    except subprocess.TimeoutExpired:
        error_msg = f"⏱️ TIMEOUT: File took longer than 5 minutes to execute"
        print(f"\n{error_msg}")
        log_file.write(f"\n{error_msg}\n")
        log_file.flush()
        return False
        
    except Exception as e:
        error_msg = f"❌ ERROR executing file: {str(e)}\n{traceback.format_exc()}"
        print(f"\n{error_msg}")
        log_file.write(f"\n=== EXECUTION ERROR ===\n{error_msg}\n")
        log_file.flush()
        return False

def main():
    """Main function"""
    # Get current directory
    current_dir = Path.cwd()
    
    print("="*80)
    print("Python File Executor - Recursive")
    print("="*80)
    print(f"Starting directory: {current_dir}")
    print(f"Python: {sys.executable}")
    print(f"Python version: {sys.version}")
    print("="*80)
    
    # Find all Python files
    print("\n🔍 Searching for Python files...")
    python_files = find_all_python_files(current_dir)
    
    if not python_files:
        print("❌ No Python files found!")
        return
    
    print(f"✅ Found {len(python_files)} Python file(s)")
    
    # Create log file
    log_filename = f"all_python_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_path = current_dir / log_filename
    
    print(f"\n📝 Log file: {log_path}")
    print(f"📊 Executing {len(python_files)} file(s)...\n")
    
    # Statistics
    successful = 0
    failed = 0
    skipped = 0
    
    with open(log_path, 'w', encoding='utf-8') as log_file:
        # Write header
        log_file.write("="*80 + "\n")
        log_file.write("Python File Execution Log\n")
        log_file.write("="*80 + "\n")
        log_file.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Directory: {current_dir}\n")
        log_file.write(f"Python: {sys.executable}\n")
        log_file.write(f"Python Version: {sys.version}\n")
        log_file.write(f"Total Files: {len(python_files)}\n")
        log_file.write("="*80 + "\n\n")
        
        # Execute each file
        for i, py_file in enumerate(python_files, 1):
            print(f"\n[{i}/{len(python_files)}] ", end="")
            
            # Check if file is executable (has if __name__ == "__main__")
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Skip if it's just a module (no main block)
                    if "__main__" not in content and "if __name__" not in content:
                        # Check if it has any executable code
                        if not any(line.strip() and not line.strip().startswith(('#', '"""', "'''")) 
                                 for line in content.split('\n')[:50]):
                            print(f"⏭️  SKIPPED (module only): {py_file.relative_to(current_dir)}")
                            log_file.write(f"\n⏭️  SKIPPED (module only): {py_file.relative_to(current_dir)}\n")
                            skipped += 1
                            continue
            except Exception as e:
                print(f"⚠️  Could not read file: {e}")
                log_file.write(f"\n⚠️  Could not read file {py_file}: {e}\n")
                skipped += 1
                continue
            
            # Execute the file
            if execute_python_file(py_file, log_file):
                successful += 1
            else:
                failed += 1
        
        # Write summary
        log_file.write("\n" + "="*80 + "\n")
        log_file.write("EXECUTION SUMMARY\n")
        log_file.write("="*80 + "\n")
        log_file.write(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Total Files: {len(python_files)}\n")
        log_file.write(f"✅ Successful: {successful}\n")
        log_file.write(f"❌ Failed: {failed}\n")
        log_file.write(f"⏭️  Skipped: {skipped}\n")
        log_file.write("="*80 + "\n")
    
    # Print summary
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"📝 Log saved to: {log_path}")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
