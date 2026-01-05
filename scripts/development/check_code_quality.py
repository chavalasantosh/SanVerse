#!/usr/bin/env python3
"""
Code Quality Checker for SanTOK
Checks for common code quality issues
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict

class CodeQualityChecker:
    """Check code quality metrics"""
    
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = Path(root_dir)
        self.issues: Dict[str, List[str]] = defaultdict(list)
        self.stats: Dict[str, int] = defaultdict(int)
    
    def check_file(self, file_path: Path) -> Dict[str, List[str]]:
        """Check a single Python file"""
        file_issues: Dict[str, List[str]] = defaultdict(list)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(file_path))
            
            # Check for type hints
            self._check_type_hints(tree, file_path, file_issues)
            
            # Check for docstrings
            self._check_docstrings(tree, file_path, file_issues)
            
            # Check for error handling
            self._check_error_handling(tree, file_path, file_issues)
            
            # Count functions and classes
            self._count_entities(tree, file_path)
            
        except SyntaxError as e:
            file_issues['syntax_errors'].append(f"Syntax error: {e}")
        except Exception as e:
            file_issues['other_errors'].append(f"Error parsing file: {e}")
        
        return file_issues
    
    def _check_type_hints(self, tree: ast.AST, file_path: Path, issues: Dict[str, List[str]]) -> None:
        """Check for type hints in function definitions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if function has return type annotation
                if node.returns is None and not node.name.startswith('_'):
                    issues['missing_return_types'].append(
                        f"{file_path}:{node.lineno}: Function '{node.name}' missing return type"
                    )
                
                # Check if parameters have type annotations
                for arg in node.args.args:
                    if arg.annotation is None and not node.name.startswith('_'):
                        issues['missing_param_types'].append(
                            f"{file_path}:{node.lineno}: Parameter '{arg.arg}' in '{node.name}' missing type"
                        )
    
    def _check_docstrings(self, tree: ast.AST, file_path: Path, issues: Dict[str, List[str]]) -> None:
        """Check for docstrings in classes and functions"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node) and not node.name.startswith('_'):
                    issues['missing_docstrings'].append(
                        f"{file_path}:{node.lineno}: {type(node).__name__} '{node.name}' missing docstring"
                    )
    
    def _check_error_handling(self, tree: ast.AST, file_path: Path, issues: Dict[str, List[str]]) -> None:
        """Check for basic error handling patterns"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                # Check if try has except clause
                if not node.handlers:
                    issues['bare_try'].append(
                        f"{file_path}:{node.lineno}: Try block without except clause"
                    )
    
    def _count_entities(self, tree: ast.AST, file_path: Path) -> None:
        """Count functions, classes, and methods"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.stats['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                self.stats['classes'] += 1
    
    def check_directory(self, directory: Path = None) -> Dict[str, List[str]]:
        """Check all Python files in directory"""
        if directory is None:
            directory = self.root_dir
        
        directory = Path(directory)
        all_issues: Dict[str, List[str]] = defaultdict(list)
        
        # Find all Python files
        python_files = list(directory.rglob('*.py'))
        
        # Exclude common directories
        exclude_dirs = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'archive'}
        python_files = [
            f for f in python_files
            if not any(excluded in f.parts for excluded in exclude_dirs)
        ]
        
        print(f"Checking {len(python_files)} Python files...")
        
        for file_path in python_files:
            file_issues = self.check_file(file_path)
            for issue_type, issue_list in file_issues.items():
                all_issues[issue_type].extend(issue_list)
        
        return all_issues
    
    def print_report(self, issues: Dict[str, List[str]]) -> None:
        """Print a report of issues found"""
        print("\n" + "=" * 70)
        print("CODE QUALITY REPORT")
        print("=" * 70)
        
        print(f"\nStatistics:")
        print(f"  Functions: {self.stats['functions']}")
        print(f"  Classes: {self.stats['classes']}")
        
        print(f"\nIssues Found:")
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        print(f"  Total: {total_issues}")
        
        for issue_type, issue_list in sorted(issues.items()):
            if issue_list:
                print(f"\n  {issue_type.replace('_', ' ').title()}: {len(issue_list)}")
                for issue in issue_list[:10]:  # Show first 10
                    print(f"    - {issue}")
                if len(issue_list) > 10:
                    print(f"    ... and {len(issue_list) - 10} more")


def main() -> None:
    """Main function"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent.parent
    
    if not root_dir.exists():
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)
    
    checker = CodeQualityChecker(root_dir)
    issues = checker.check_directory()
    checker.print_report(issues)
    
    # Exit with error code if issues found
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    if total_issues > 0:
        sys.exit(1)
    else:
        print("\n✓ No code quality issues found!")


if __name__ == "__main__":
    main()
