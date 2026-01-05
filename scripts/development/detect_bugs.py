#!/usr/bin/env python3
"""
Bug Detector for SOMA
Detects various types of bugs in Python code
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple, Any
from collections import defaultdict

class BugDetector(ast.NodeVisitor):
    """AST visitor to detect bugs"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.bugs: List[Dict[str, Any]] = []
        self.imports: Set[str] = set()
        self.defined_names: Set[str] = set()
        self.used_names: Set[str] = set()
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name.split('.')[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module.split('.')[0])
        self.generic_visit(node)
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        # Check for missing return in non-void functions
        has_return = False
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                has_return = True
                break
        
        # Check for unused parameters
        param_names = {arg.arg for arg in node.args.args if arg.arg != 'self'}
        body_names = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                body_names.add(child.id)
        
        unused_params = param_names - body_names
        if unused_params and not node.name.startswith('_'):
            self.bugs.append({
                'type': 'unused_parameter',
                'line': node.lineno,
                'message': f"Function '{node.name}' has unused parameters: {', '.join(unused_params)}",
                'severity': 'low'
            })
        
        self.generic_visit(node)
    
    def visit_Try(self, node):
        # Check for bare except
        for handler in node.handlers:
            if handler.type is None:
                self.bugs.append({
                    'type': 'bare_except',
                    'line': handler.lineno,
                    'message': 'Bare except clause catches all exceptions including KeyboardInterrupt and SystemExit',
                    'severity': 'medium'
                })
        
        # Check for try without except/finally
        if not node.handlers and not node.finalbody:
            self.bugs.append({
                'type': 'bare_try',
                'line': node.lineno,
                'message': 'Try block without except or finally clause',
                'severity': 'high'
            })
        
        self.generic_visit(node)
    
    def visit_Compare(self, node):
        # Check for comparison with None using == or !=
        for comparator in node.comparators:
            if isinstance(comparator, ast.Constant) and comparator.value is None:
                if isinstance(node.ops[0], (ast.Eq, ast.NotEq)):
                    self.bugs.append({
                        'type': 'none_comparison',
                        'line': node.lineno,
                        'message': 'Use "is None" or "is not None" instead of "is None" or "is not None"',
                        'severity': 'low'
                    })
        self.generic_visit(node)
    
    def visit_Call(self, node):
        # Check for calling len() in boolean context
        if isinstance(node.func, ast.Name) and node.func.id == 'len':
            parent = getattr(node, 'parent', None)
            if parent and isinstance(parent, (ast.If, ast.While, ast.IfExp)):
                self.bugs.append({
                    'type': 'len_in_boolean',
                    'line': node.lineno,
                    'message': 'Use truthiness check instead of len() in boolean context (e.g., use "if items:" instead of "if items:")',
                    'severity': 'low'
                })
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        # Check for potential AttributeError
        if isinstance(node.value, ast.Name):
            if node.value.id not in self.defined_names and node.value.id not in self.imports:
                self.bugs.append({
                    'type': 'potential_attribute_error',
                    'line': node.lineno,
                    'message': f'Potential AttributeError: {node.value.id} may not be defined',
                    'severity': 'medium'
                })
        self.generic_visit(node)


class ComprehensiveBugDetector:
    """Detect bugs across all Python files"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.all_bugs: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.bug_summary: Dict[str, int] = defaultdict(int)
    
    def detect_bugs_in_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Detect bugs in a single file"""
        bugs = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Syntax check
            try:
                tree = ast.parse(content, filename=str(file_path))
            except SyntaxError as e:
                bugs.append({
                    'type': 'syntax_error',
                    'line': e.lineno or 0,
                    'message': f'Syntax error: {e.msg}',
                    'severity': 'critical'
                })
                return bugs
            
            # AST-based bug detection
            detector = BugDetector(file_path)
            
            # Add parent references for better traversal
            for node in ast.walk(tree):
                for child in ast.iter_child_nodes(node):
                    child.parent = node
            
            detector.visit(tree)
            bugs.extend(detector.bugs)
            
            # Check for undefined names (simplified)
            undefined = detector.used_names - detector.defined_names - detector.imports
            undefined = {name for name in undefined if not name.startswith('_') and name not in dir(__builtins__)}
            
            # Common issues checks
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                
                # Check for common issues
                if 'except:' in stripped and 'except Exception:' not in stripped:
                    bugs.append({
                        'type': 'bare_except_string',
                        'line': i,
                        'message': 'Bare except clause (use except Exception:)',
                        'severity': 'medium'
                    })
                
                if 'is None' in stripped or 'is not None' in stripped:
                    bugs.append({
                        'type': 'none_comparison_string',
                        'line': i,
                        'message': 'Use "is None" or "is not None" instead',
                        'severity': 'low'
                    })
                
                if 'print(' in stripped and 'logger' not in content.lower():
                    # Only flag if no logging setup
                    pass  # Commented out - too many false positives
                
                # Check for potential issues
                if 'import *' in stripped:
                    bugs.append({
                        'type': 'wildcard_import',
                        'line': i,
                        'message': 'Wildcard import (*) makes code harder to read and can cause namespace pollution',
                        'severity': 'medium'
                    })
        
        except Exception as e:
            bugs.append({
                'type': 'file_error',
                'line': 0,
                'message': f'Error reading file: {str(e)}',
                'severity': 'high'
            })
        
        return bugs
    
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
        
        print(f"Scanning {len(python_files)} Python files for bugs...")
        
        for file_path in python_files:
            rel_path = str(file_path.relative_to(self.root_dir))
            bugs = self.detect_bugs_in_file(file_path)
            
            if bugs:
                self.all_bugs[rel_path] = bugs
                for bug in bugs:
                    self.bug_summary[bug['type']] += 1
        
        return {
            'bugs': dict(self.all_bugs),
            'summary': dict(self.bug_summary),
            'total_files_with_bugs': len(self.all_bugs),
            'total_bugs': sum(len(bugs) for bugs in self.all_bugs.values())
        }
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate bug report"""
        report = []
        report.append("=" * 70)
        report.append("BUG DETECTION REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"Total Files with Bugs: {results['total_files_with_bugs']}")
        report.append(f"Total Bugs Found: {results['total_bugs']}")
        report.append("")
        
        # Bug type summary
        if results['summary']:
            report.append("BUGS BY TYPE")
            report.append("-" * 70)
            for bug_type, count in sorted(results['summary'].items(), key=lambda x: x[1], reverse=True):
                report.append(f"  {bug_type}: {count}")
            report.append("")
        
        # Critical bugs first
        critical_bugs = []
        high_bugs = []
        medium_bugs = []
        low_bugs = []
        
        for file_path, bugs in results['bugs'].items():
            for bug in bugs:
                bug_entry = (file_path, bug)
                severity = bug.get('severity', 'low')
                if severity == 'critical':
                    critical_bugs.append(bug_entry)
                elif severity == 'high':
                    high_bugs.append(bug_entry)
                elif severity == 'medium':
                    medium_bugs.append(bug_entry)
                else:
                    low_bugs.append(bug_entry)
        
        # Report bugs by severity
        if critical_bugs:
            report.append("CRITICAL BUGS")
            report.append("-" * 70)
            for file_path, bug in critical_bugs[:20]:
                report.append(f"  {file_path}:{bug['line']}")
                report.append(f"    Type: {bug['type']}")
                report.append(f"    Message: {bug['message']}")
                report.append("")
            if len(critical_bugs) > 20:
                report.append(f"  ... and {len(critical_bugs) - 20} more critical bugs")
            report.append("")
        
        if high_bugs:
            report.append("HIGH SEVERITY BUGS")
            report.append("-" * 70)
            for file_path, bug in high_bugs[:20]:
                report.append(f"  {file_path}:{bug['line']}")
                report.append(f"    Type: {bug['type']}")
                report.append(f"    Message: {bug['message']}")
                report.append("")
            if len(high_bugs) > 20:
                report.append(f"  ... and {len(high_bugs) - 20} more high severity bugs")
            report.append("")
        
        if medium_bugs:
            report.append("MEDIUM SEVERITY BUGS (First 30)")
            report.append("-" * 70)
            for file_path, bug in medium_bugs[:30]:
                report.append(f"  {file_path}:{bug['line']} - {bug['type']}: {bug['message']}")
            if len(medium_bugs) > 30:
                report.append(f"  ... and {len(medium_bugs) - 30} more medium severity bugs")
            report.append("")
        
        # Files with most bugs
        files_with_bug_counts = sorted(
            [(path, len(bugs)) for path, bugs in results['bugs'].items()],
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        if files_with_bug_counts:
            report.append("FILES WITH MOST BUGS")
            report.append("-" * 70)
            for file_path, count in files_with_bug_counts:
                report.append(f"  {file_path}: {count} bugs")
            report.append("")
        
        return "\n".join(report)


def main() -> None:
    """Main function"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent.parent
    
    if not root_dir.exists():
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)
    
    detector = ComprehensiveBugDetector(root_dir)
    results = detector.scan_directory()
    
    # Print report
    report = detector.generate_report(results)
    print("\n" + report)
    
    # Save report
    report_file = root_dir / "bug_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nBug report saved to: {report_file}")
    
    # Exit with error code if bugs found
    if results['total_bugs'] > 0:
        sys.exit(1)
    else:
        print("\n✓ No bugs found!")


if __name__ == "__main__":
    main()
