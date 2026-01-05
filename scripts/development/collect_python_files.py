#!/usr/bin/env python3
"""
Script to collect all Python files from the codebase into a clean directory structure
for sharing with teammates.
"""

import os
import shutil
from pathlib import Path

def collect_python_files(source_dir=".", dest_dir="python_code_collection"):
    """Collect all Python files while preserving directory structure."""
    
    source_path = Path(source_dir).resolve()
    dest_path = Path(dest_dir).resolve()
    
    # Create destination directory
    dest_path.mkdir(exist_ok=True)
    
    # Find all Python files
    python_files = []
    excluded_dirs = {'node_modules', '__pycache__', '.git', '.venv', 'venv', 'env', 
                     'python_code_collection', '.pytest_cache', '.mypy_cache'}
    
    for root, dirs, files in os.walk(source_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if file.endswith('.py'):
                full_path = Path(root) / file
                python_files.append(full_path)
    
    # Copy files preserving structure
    copied_count = 0
    for py_file in python_files:
        try:
            # Get relative path from source
            rel_path = py_file.relative_to(source_path)
            
            # Create destination path
            dest_file = dest_path / rel_path
            
            # Create parent directories
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(py_file, dest_file)
            copied_count += 1
            print(f"Copied: {rel_path}")
        except Exception as e:
            print(f"Error copying {py_file}: {e}")
    
    # Create index file
    index_file = dest_path / "INDEX.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# Python Code Collection - Complete Index\n\n")
        f.write(f"Total Python files collected: {copied_count}\n\n")
        f.write("## Directory Structure\n\n")
        
        # Group files by directory
        files_by_dir = {}
        for py_file in sorted(python_files):
            rel_path = py_file.relative_to(source_path)
            dir_name = str(rel_path.parent) if rel_path.parent != Path('.') else 'root'
            if dir_name not in files_by_dir:
                files_by_dir[dir_name] = []
            files_by_dir[dir_name].append(rel_path.name)
        
        for dir_name in sorted(files_by_dir.keys()):
            f.write(f"### {dir_name}\n\n")
            for filename in sorted(files_by_dir[dir_name]):
                f.write(f"- `{filename}`\n")
            f.write("\n")
    
    print(f"\n[SUCCESS] Successfully copied {copied_count} Python files to '{dest_dir}'")
    print(f"[INFO] Index file created: {index_file}")
    return copied_count

if __name__ == "__main__":
    count = collect_python_files()
    print(f"\n[COMPLETE] Collection complete! Ready to share with your teammate.")
