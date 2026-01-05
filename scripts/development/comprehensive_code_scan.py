#!/usr/bin/env python3
"""
Comprehensive Code Scanner for SOMA
Scans all Python files and generates detailed report
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple, Any
from collections import defaultdict
import json

class ComprehensiveCodeScanner:
    """Comprehensive code scanner for Python files"""
    
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = Path(root_dir)
        self.stats: Dict[str, int] = defaultdict(int)
        self.issues: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.file_stats: Dict[str, Dict[str, Any]] = {}
    
    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan a single Python file"""
        file_info: Dict[str, Any] = {
            'path': str(file_path.relative_to(self.root_dir)),
            'lines': 0,
            'functions': 0,
            'classes': 0,
            'imports': 0,
            'type_hints': 0,
            'docstrings': 0,
            'errors': [],
            'warnings': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_info['lines'] = len(content.splitlines())
            
            try:
                tree = ast.parse(content, filename=str(file_path))
                file_info['parsable'] = True
                
                # Count entities
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        file_info['functions'] += 1
                        # Check for type hints
                        if node.returns is not None:
                            file_info['type_hints'] += 1
                        # Check for docstring
                        if ast.get_docstring(node):
                            file_info['docstrings'] += 1
                        # Check parameter types
                        for arg in node.args.args:
                            if arg.annotation is not None:
                                file_info['type_hints'] += 1
                    elif isinstance(node, ast.ClassDef):
                        file_info['classes'] += 1
                        if ast.get_docstring(node):
                            file_info['docstrings'] += 1
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        file_info['imports'] += 1
                
                # Check for common issues
                self._check_issues(tree, file_path, file_info)
                
            except SyntaxError as e:
                file_info['parsable'] = False
                file_info['errors'].append({
                    'type': 'syntax_error',
                    'message': str(e),
                    'line': e.lineno
                })
                self.issues['syntax_errors'].append(file_info)
        
        except Exception as e:
            file_info['errors'].append({
                'type': 'file_error',
                'message': str(e)
            })
        
        return file_info
    
    def _check_issues(self, tree: ast.AST, file_path: Path, file_info: Dict[str, Any]) -> None:
        """Check for common code quality issues"""
        for node in ast.walk(tree):
            # Check for bare try blocks
            if isinstance(node, ast.Try):
                if not node.handlers and not node.finalbody:
                    file_info['warnings'].append({
                        'type': 'bare_try',
                        'line': node.lineno,
                        'message': 'Try block without except or finally'
                    })
    
    def scan_directory(self, directory: Path = None, exclude_dirs: Set[str] = None) -> Dict[str, Any]:
        """Scan all Python files in directory"""
        if directory is None:
            directory = self.root_dir
        
        if exclude_dirs is None:
            exclude_dirs = {
                '__pycache__', '.git', 'node_modules', 
                'venv', '.venv', 'archive', 
                'python_code_collection', 'demo_SOMA',
                '.pytest_cache', '.vscode'
            }
        
        directory = Path(directory)
        python_files = list(directory.rglob('*.py'))
        
        # Filter out excluded directories
        python_files = [
            f for f in python_files
            if not any(excluded in f.parts for excluded in exclude_dirs)
        ]
        
        print(f"Scanning {len(python_files)} Python files...")
        
        for file_path in python_files:
            file_info = self.scan_file(file_path)
            rel_path = file_info['path']
            self.file_stats[rel_path] = file_info
            
            # Update global stats
            self.stats['total_files'] += 1
            self.stats['total_lines'] += file_info['lines']
            self.stats['total_functions'] += file_info['functions']
            self.stats['total_classes'] += file_info['classes']
            self.stats['total_imports'] += file_info['imports']
            self.stats['total_type_hints'] += file_info['type_hints']
            self.stats['total_docstrings'] += file_info['docstrings']
            
            if file_info['errors']:
                self.stats['files_with_errors'] += 1
            if file_info['warnings']:
                self.stats['files_with_warnings'] += 1
            if not file_info['parsable']:
                self.stats['unparsable_files'] += 1
        
        return {
            'stats': dict(self.stats),
            'file_stats': self.file_stats,
            'issues': dict(self.issues)
        }
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive report"""
        stats = results['stats']
        
        report = []
        report.append("=" * 70)
        report.append("COMPREHENSIVE CODE SCAN REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Statistics
        report.append("STATISTICS")
        report.append("-" * 70)
        report.append(f"Total Files Scanned: {stats['total_files']}")
        report.append(f"Total Lines of Code: {stats['total_lines']:,}")
        report.append(f"Total Functions: {stats['total_functions']:,}")
        report.append(f"Total Classes: {stats['total_classes']:,}")
        report.append(f"Total Imports: {stats['total_imports']:,}")
        report.append("")
        
        # Code Quality Metrics
        report.append("CODE QUALITY METRICS")
        report.append("-" * 70)
        if stats['total_functions'] > 0:
            type_hint_coverage = (stats['total_type_hints'] / (stats['total_functions'] * 2)) * 100
            report.append(f"Type Hint Coverage: {type_hint_coverage:.1f}%")
        
        if stats['total_functions'] + stats['total_classes'] > 0:
            docstring_coverage = (stats['total_docstrings'] / (stats['total_functions'] + stats['total_classes'])) * 100
            report.append(f"Docstring Coverage: {docstring_coverage:.1f}%")
        
        report.append(f"Files with Errors: {stats.get('files_with_errors', 0)}")
        report.append(f"Files with Warnings: {stats.get('files_with_warnings', 0)}")
        report.append(f"Unparsable Files: {stats.get('unparsable_files', 0)}")
        report.append("")
        
        # Files with issues
        files_with_errors = [
            (path, info) for path, info in results['file_stats'].items()
            if info.get('errors')
        ]
        
        if files_with_errors:
            report.append("FILES WITH ERRORS")
            report.append("-" * 70)
            for path, info in files_with_errors[:20]:
                report.append(f"  {path}:")
                for error in info['errors']:
                    report.append(f"    - {error['type']}: {error['message']}")
            if len(files_with_errors) > 20:
                report.append(f"  ... and {len(files_with_errors) - 20} more files with errors")
            report.append("")
        
        # Top files by size
        large_files = sorted(
            [(path, info['lines']) for path, info in results['file_stats'].items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        if large_files:
            report.append("LARGEST FILES")
            report.append("-" * 70)
            for path, lines in large_files:
                report.append(f"  {path}: {lines:,} lines")
            report.append("")
        
        return "\n".join(report)
    
    def save_json_report(self, results: Dict[str, Any], output_file: Path) -> None:
        """Save detailed results as JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


def main() -> None:
    """Main function"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent.parent
    
    if not root_dir.exists():
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)
    
    scanner = ComprehensiveCodeScanner(root_dir)
    results = scanner.scan_directory()
    
    # Print report
    report = scanner.generate_report(results)
    print("\n" + report)
    
    # Save JSON report
    json_file = root_dir / "comprehensive_scan_report.json"
    scanner.save_json_report(results, json_file)
    print(f"\nDetailed JSON report saved to: {json_file}")
    
    # Save text report
    text_file = root_dir / "comprehensive_scan_report.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Text report saved to: {text_file}")


if __name__ == "__main__":
    main()
