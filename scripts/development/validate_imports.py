#!/usr/bin/env python3
"""
Import Validator for SanTOK
Validates that all imports work correctly
"""

import sys
import ast
from pathlib import Path
from typing import List, Dict, Set, Tuple
import importlib.util

class ImportValidator:
    """Validate imports in Python files"""
    
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = Path(root_dir)
        self.import_errors: List[Tuple[str, str]] = []
        self.successful_imports: Set[str] = set()
        self.failed_imports: Set[str] = set()
    
    def extract_imports(self, file_path: Path) -> List[str]:
        """Extract all imports from a Python file"""
        imports: List[str] = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                        # Also add module.name for from imports
                        for alias in node.names:
                            imports.append(f"{node.module}.{alias.name}")
        
        except SyntaxError as e:
            self.import_errors.append((str(file_path), f"Syntax error: {e}"))
        except Exception as e:
            self.import_errors.append((str(file_path), f"Parse error: {e}"))
        
        return imports
    
    def check_file_imports(self, file_path: Path, base_path: Path = None) -> Dict[str, bool]:
        """Check if imports in a file are valid"""
        if base_path is None:
            base_path = self.root_dir
        
        results: Dict[str, bool] = {}
        imports = self.extract_imports(file_path)
        
        for import_name in imports:
            # Skip relative imports for now
            if import_name.startswith('.'):
                continue
            
            # Try to import
            try:
                # Split to get module name (before first dot)
                module_name = import_name.split('.')[0]
                
                # Check if it's a standard library module
                if module_name in sys.stdlib_module_names:
                    results[import_name] = True
                    self.successful_imports.add(import_name)
                else:
                    # Try to import
                    try:
                        spec = importlib.util.find_spec(module_name)
                        if spec is not None:
                            results[import_name] = True
                            self.successful_imports.add(import_name)
                        else:
                            results[import_name] = False
                            self.failed_imports.add(import_name)
                    except (ImportError, ModuleNotFoundError):
                        # Might be a local module
                        results[import_name] = None  # Unknown/possibly local
            except Exception:
                results[import_name] = False
                self.failed_imports.add(import_name)
        
        return results
    
    def validate_directory(self, directory: Path = None) -> Dict[str, any]:
        """Validate imports in all Python files"""
        if directory is None:
            directory = self.root_dir
        
        directory = Path(directory)
        all_results: Dict[str, Dict[str, bool]] = {}
        
        # Find all Python files
        python_files = list(directory.rglob('*.py'))
        
        # Exclude common directories
        exclude_dirs = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'archive', 'tests'}
        python_files = [
            f for f in python_files
            if not any(excluded in f.parts for excluded in exclude_dirs)
        ]
        
        print(f"Checking imports in {len(python_files)} Python files...")
        
        for file_path in python_files:
            rel_path = file_path.relative_to(self.root_dir)
            results = self.check_file_imports(file_path)
            if results:
                all_results[str(rel_path)] = results
        
        return all_results
    
    def print_report(self, results: Dict[str, Dict[str, bool]]) -> None:
        """Print validation report"""
        print("\n" + "=" * 70)
        print("IMPORT VALIDATION REPORT")
        print("=" * 70)
        
        if self.import_errors:
            print(f"\nParse Errors: {len(self.import_errors)}")
            for file_path, error in self.import_errors[:10]:
                print(f"  - {file_path}: {error}")
        
        print(f"\nSuccessful Imports: {len(self.successful_imports)}")
        print(f"Failed Imports: {len(self.failed_imports)}")
        
        if self.failed_imports:
            print("\nFailed Imports (first 20):")
            for imp in sorted(list(self.failed_imports))[:20]:
                print(f"  - {imp}")
        
        # Show files with import issues
        files_with_issues = {
            path: imports 
            for path, imports in results.items()
            if any(status is False for status in imports.values())
        }
        
        if files_with_issues:
            print(f"\nFiles with Import Issues: {len(files_with_issues)}")
            for file_path, imports in list(files_with_issues.items())[:10]:
                failed = [imp for imp, status in imports.items() if status is False]
                print(f"  - {file_path}: {len(failed)} failed imports")


def main() -> None:
    """Main function"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent.parent
    
    if not root_dir.exists():
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)
    
    validator = ImportValidator(root_dir)
    results = validator.validate_directory()
    validator.print_report(results)
    
    # Exit with error code if there are failures
    if validator.failed_imports or validator.import_errors:
        sys.exit(1)
    else:
        print("\n✓ All imports validated successfully!")


if __name__ == "__main__":
    main()
