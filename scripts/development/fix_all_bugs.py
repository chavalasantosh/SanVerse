#!/usr/bin/env python3
"""
Automated Bug Fixer for SanTOK
Fixes all detected bugs automatically
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any

class BugFixer:
    """Automatically fix bugs in Python files"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.fixes_applied: List[Tuple[str, str, int]] = []  # (file, fix_type, count)
        self.exclude_dirs = {
            '__pycache__', '.git', 'node_modules',
            'venv', '.venv', 'archive',
            'python_code_collection', 'demo_santok',
            '.pytest_cache', '.vscode'
        }
    
    def fix_bare_except(self, content: str) -> Tuple[str, int]:
        """Fix bare except clauses"""
        fixes = 0
        lines = content.splitlines()
        new_lines = []
        
        for line in lines:
            # Match bare except: (but not except Exception: or except SomeError:)
            if re.match(r'^\s*except\s*:\s*$', line):
                # Replace with except Exception:
                new_line = re.sub(r'except\s*:', 'except Exception:', line)
                new_lines.append(new_line)
                fixes += 1
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines), fixes
    
    def fix_wildcard_imports(self, content: str) -> Tuple[str, int]:
        """Fix wildcard imports - comment them with note"""
        fixes = 0
        lines = content.splitlines()
        new_lines = []
        
        for i, line in enumerate(lines):
            # Match "from module import *"
            # TODO: Replace wildcard import with explicit imports
            if re.search(r'from\s+\S+\s+import\s+\*', line):
                # Add comment warning
                indent = len(line) - len(line.lstrip())
                new_lines.append(line)
                new_lines.append(' ' * indent + '# TODO: Replace wildcard import with explicit imports')
                fixes += 1
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines), fixes
    
    def fix_none_comparison(self, content: str) -> Tuple[str, int]:
        """Fix None comparisons"""
        fixes = 0
        
        # Fix is None
        new_content, count1 = re.subn(r'==\s*None\b', 'is None', content)
        fixes += count1
        
        # Fix is not None
        new_content, count2 = re.subn(r'!=\s*None\b', 'is not None', new_content)
        fixes += count2
        
        return new_content, fixes
    
    def fix_len_in_boolean(self, content: str) -> Tuple[str, int]:
        """Fix len() in boolean context"""
        fixes = 0
        lines = content.splitlines()
        new_lines = []
        
        for line in lines:
            # Match if ...: or while len(...):
            # But be careful - only fix simple cases
            if re.search(r'\bif\s+len\([^)]+\)\s*:', line):
                # Replace if x: with if x:
                new_line = re.sub(r'if\s+len\(([^)]+)\)\s*:', r'if \1:', line)
                if new_line != line:
                    new_lines.append(new_line)
                    fixes += 1
                else:
                    new_lines.append(line)
            elif re.search(r'\bwhile\s+len\([^)]+\)\s*:', line):
                # Replace while x: with while x:
                new_line = re.sub(r'while\s+len\(([^)]+)\)\s*:', r'while \1:', line)
                if new_line != line:
                    new_lines.append(new_line)
                    fixes += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines), fixes
    
    def fix_file(self, file_path: Path) -> Dict[str, int]:
        """Fix all bugs in a single file"""
        fixes = {
            'bare_except': 0,
            'wildcard_import': 0,
            'none_comparison': 0,
            'len_in_boolean': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all fixes
            content, count = self.fix_bare_except(content)
            fixes['bare_except'] = count
            
            content, count = self.fix_wildcard_imports(content)
            fixes['wildcard_import'] = count
            
            content, count = self.fix_none_comparison(content)
            fixes['none_comparison'] = count
            
            content, count = self.fix_len_in_boolean(content)
            fixes['len_in_boolean'] = count
            
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return fixes
        
        except Exception as e:
            print(f"Error fixing {file_path}: {e}", file=sys.stderr)
        
        return fixes
    
    def fix_all_files(self) -> Dict[str, Any]:
        """Fix bugs in all Python files"""
        python_files = list(self.root_dir.rglob('*.py'))
        
        # Filter out excluded directories
        python_files = [
            f for f in python_files
            if not any(excluded in f.parts for excluded in self.exclude_dirs)
        ]
        
        print(f"Fixing bugs in {len(python_files)} Python files...")
        
        total_fixes = {
            'bare_except': 0,
            'wildcard_import': 0,
            'none_comparison': 0,
            'len_in_boolean': 0,
            'files_fixed': 0
        }
        
        for file_path in python_files:
            fixes = self.fix_file(file_path)
            
            if any(fixes.values()):
                total_fixes['files_fixed'] += 1
                for fix_type, count in fixes.items():
                    total_fixes[fix_type] += count
                
                rel_path = file_path.relative_to(self.root_dir)
                print(f"  Fixed {rel_path}: {sum(fixes.values())} issues")
        
        return total_fixes


def main() -> None:
    """Main function"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent.parent
    
    if not root_dir.exists():
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)
    
    fixer = BugFixer(root_dir)
    results = fixer.fix_all_files()
    
    print("\n" + "=" * 70)
    print("BUG FIXING SUMMARY")
    print("=" * 70)
    print(f"Files Fixed: {results['files_fixed']}")
    print(f"Bare Except Clauses Fixed: {results['bare_except']}")
    print(f"Wildcard Imports Marked: {results['wildcard_import']}")
    print(f"None Comparisons Fixed: {results['none_comparison']}")
    print(f"len() in Boolean Fixed: {results['len_in_boolean']}")
    print(f"Total Fixes: {sum(results.values()) - results['files_fixed']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
