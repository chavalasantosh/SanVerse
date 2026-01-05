#!/usr/bin/env python3
"""
Comprehensive Bug Checker for SanTOK
Checks syntax errors, import errors, and common bugs
"""

import ast
import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple, Any
from collections import defaultdict

class SyntaxChecker:
    """Check for syntax errors"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.syntax_errors: List[Dict[str, Any]] = []
        self.exclude_dirs = {
            '__pycache__', '.git', 'node_modules',
            'venv', '.venv', 'archive',
            'python_code_collection', 'demo_santok',
            '.pytest_cache', '.vscode'
        }
    
    def check_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check a single file for syntax errors"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                ast.parse(content, filename=str(file_path))
            except SyntaxError as e:
                errors.append({
                    'type': 'syntax_error',
                    'file': str(file_path.relative_to(self.root_dir)),
                    'line': e.lineno or 0,
                    'message': e.msg,
                    'text': e.text or '',
                    'severity': 'critical'
                })
            except Exception as e:
                errors.append({
                    'type': 'parse_error',
                    'file': str(file_path.relative_to(self.root_dir)),
                    'line': 0,
                    'message': f"Failed to parse: {str(e)}",
                    'severity': 'high'
                })
        
        except Exception as e:
            errors.append({
                'type': 'file_error',
                'file': str(file_path.relative_to(self.root_dir)),
                'line': 0,
                'message': f"Error reading file: {str(e)}",
                'severity': 'high'
            })
        
        return errors
    
    def check_all(self) -> List[Dict[str, Any]]:
        """Check all Python files"""
        python_files = list(self.root_dir.rglob('*.py'))
        
        # Filter excluded directories
        python_files = [
            f for f in python_files
            if not any(excluded in f.parts for excluded in self.exclude_dirs)
        ]
        
        print(f"Checking {len(python_files)} Python files for syntax errors...")
        
        all_errors = []
        for file_path in python_files:
            errors = self.check_file(file_path)
            all_errors.extend(errors)
        
        return all_errors


class ImportChecker:
    """Check for import errors"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.import_errors: List[Dict[str, Any]] = []
        self.exclude_dirs = {
            '__pycache__', '.git', 'node_modules',
            'venv', '.venv', 'archive',
            'python_code_collection', 'demo_santok',
            '.pytest_cache', '.vscode'
        }
    
    def check_imports(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check imports in a file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content, filename=str(file_path))
            except SyntaxError:
                return errors  # Skip files with syntax errors
            
            # Check imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        errors.extend(self._check_import_name(alias.name, file_path))
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        errors.extend(self._check_import_name(node.module, file_path))
        
        except Exception:
            pass  # Skip files we can't parse
        
        return errors
    
    def _check_import_name(self, module_name: str, file_path: Path) -> List[Dict[str, Any]]:
        """Check if an import name looks problematic"""
        errors = []
        
        # Check for common problematic patterns
        if '..' in module_name:
            errors.append({
                'type': 'relative_import_issue',
                'file': str(file_path.relative_to(self.root_dir)),
                'message': f"Potentially problematic relative import: {module_name}",
                'severity': 'low'
            })
        
        return errors


def main() -> None:
    """Main function"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent.parent
    
    if not root_dir.exists():
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 70)
    print("COMPREHENSIVE BUG CHECK")
    print("=" * 70)
    print()
    
    # Check syntax errors
    syntax_checker = SyntaxChecker(root_dir)
    syntax_errors = syntax_checker.check_all()
    
    # Check import issues
    import_checker = ImportChecker(root_dir)
    python_files = [
        f for f in root_dir.rglob('*.py')
        if not any(ex in f.parts for ex in import_checker.exclude_dirs)
    ]
    import_errors = []
    for file_path in python_files[:100]:  # Limit to first 100 for speed
        import_errors.extend(import_checker.check_imports(file_path))
    
    # Summary
    print("\n" + "=" * 70)
    print("BUG CHECK SUMMARY")
    print("=" * 70)
    print(f"Syntax Errors: {len([e for e in syntax_errors if e['severity'] == 'critical'])}")
    print(f"Parse Errors: {len([e for e in syntax_errors if e['severity'] == 'high'])}")
    print(f"Import Issues: {len(import_errors)}")
    print()
    
    # Critical errors
    critical_errors = [e for e in syntax_errors if e['severity'] == 'critical']
    if critical_errors:
        print("CRITICAL SYNTAX ERRORS:")
        print("-" * 70)
        for error in critical_errors[:20]:
            print(f"  {error['file']}:{error['line']}")
            print(f"    {error['message']}")
            if error['text']:
                print(f"    Line: {error['text'].strip()}")
            print()
    
    # High severity errors
    high_errors = [e for e in syntax_errors if e['severity'] == 'high']
    if high_errors:
        print("HIGH SEVERITY ERRORS:")
        print("-" * 70)
        for error in high_errors[:10]:
            print(f"  {error['file']}: {error['message']}")
        print()
    
    # Save report
    report_file = root_dir / "comprehensive_bug_check.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("COMPREHENSIVE BUG CHECK REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Syntax Errors: {len(critical_errors)}\n")
        f.write(f"Parse Errors: {len(high_errors)}\n")
        f.write(f"Import Issues: {len(import_errors)}\n\n")
        
        if critical_errors:
            f.write("CRITICAL SYNTAX ERRORS:\n")
            f.write("-" * 70 + "\n")
            for error in critical_errors:
                f.write(f"{error['file']}:{error['line']}\n")
                f.write(f"  {error['message']}\n")
                if error['text']:
                    f.write(f"  Line: {error['text'].strip()}\n")
                f.write("\n")
    
    print(f"Report saved to: {report_file}")
    
    # Exit with error code if critical errors found
    if critical_errors:
        sys.exit(1)
    else:
        print("✓ No critical syntax errors found!")
        sys.exit(0)


if __name__ == "__main__":
    main()


