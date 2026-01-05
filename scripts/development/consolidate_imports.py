#!/usr/bin/env python3
"""
Import Consolidation Helper
Helps identify and consolidate redundant import try/except blocks
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

class ImportConsolidator:
    """Analyze and suggest import consolidation"""
    
    def __init__(self, file_path: Path) -> None:
        self.file_path = Path(file_path)
        self.import_blocks: List[Dict] = []
        self.consolidation_suggestions: List[str] = []
    
    def analyze_file(self) -> Dict[str, any]:
        """Analyze file for import consolidation opportunities"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(self.file_path))
            
            # Find all try/except blocks for imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    if self._is_import_try_block(node):
                        imports = self._extract_imports_from_try(node)
                        if imports:
                            self.import_blocks.append({
                                'line': node.lineno,
                                'imports': imports,
                                'has_fallback': len(node.handlers) > 1
                            })
            
            # Generate suggestions
            self._generate_suggestions()
            
            return {
                'file': str(self.file_path),
                'import_blocks': self.import_blocks,
                'suggestions': self.consolidation_suggestions,
                'total_blocks': len(self.import_blocks)
            }
        
        except Exception as e:
            return {
                'file': str(self.file_path),
                'error': str(e)
            }
    
    def _is_import_try_block(self, node: ast.Try) -> bool:
        """Check if try block is for imports"""
        for stmt in node.body:
            if isinstance(stmt, (ast.Import, ast.ImportFrom)):
                return True
        return False
    
    def _extract_imports_from_try(self, node: ast.Try) -> List[str]:
        """Extract import statements from try block"""
        imports: List[str] = []
        for stmt in node.body:
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(stmt, ast.ImportFrom):
                module = stmt.module or ""
                names = ", ".join(alias.name for alias in stmt.names)
                imports.append(f"from {module} import {names}")
        return imports
    
    def _generate_suggestions(self) -> None:
        """Generate consolidation suggestions"""
        if len(self.import_blocks) > 3:
            self.consolidation_suggestions.append(
                f"Found {len(self.import_blocks)} import try blocks. "
                "Consider consolidating imports with a helper function."
            )
        
        # Group similar imports
        import_counts: Dict[str, int] = {}
        for block in self.import_blocks:
            for imp in block['imports']:
                import_counts[imp] = import_counts.get(imp, 0) + 1
        
        duplicates = {imp: count for imp, count in import_counts.items() if count > 1}
        if duplicates:
            self.consolidation_suggestions.append(
                f"Found {len(duplicates)} duplicate imports across try blocks. "
                "Consider importing once at the top level."
            )


def analyze_file(file_path: Path) -> None:
    """Analyze a single file"""
    consolidator = ImportConsolidator(file_path)
    results = consolidator.analyze_file()
    
    if 'error' in results:
        print(f"Error analyzing {file_path}: {results['error']}")
        return
    
    print(f"\nFile: {results['file']}")
    print(f"Import try blocks: {results['total_blocks']}")
    
    if results['suggestions']:
        print("\nSuggestions:")
        for suggestion in results['suggestions']:
            print(f"  - {suggestion}")
    
    if results['import_blocks']:
        print("\nImport blocks found:")
        for i, block in enumerate(results['import_blocks'][:5], 1):
            print(f"  {i}. Line {block['line']}: {len(block['imports'])} imports")


def main() -> None:
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python consolidate_imports.py <file_path>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    analyze_file(file_path)


if __name__ == "__main__":
    main()
