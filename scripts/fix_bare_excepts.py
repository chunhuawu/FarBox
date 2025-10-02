#!/usr/bin/env python3
"""
Script to fix bare except: clauses throughout the codebase.
Replaces bare except: with except Exception: to avoid catching system exceptions.
"""
import os
import re
from pathlib import Path

def fix_bare_except_in_file(filepath):
    """Fix bare except clauses in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Pattern 1: except: on same line with code (e.g., except: pass)
    # Matches: "except:" not followed by alphanumeric (to avoid except ExceptionClass:)
    pattern1 = r'except:\s+(?=[a-zA-Z_])'
    replacement1 = r'except Exception: '
    content = re.sub(pattern1, replacement1, content)

    # Pattern 2: except: at end of line or with comment
    pattern2 = r'except:\s*($|#)'
    replacement2 = r'except Exception:\1'
    content = re.sub(pattern2, replacement2, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Find and fix all Python files with bare except clauses."""
    root_dir = Path(__file__).parent.parent / 'farbox_bucket'
    files_fixed = 0

    for filepath in root_dir.rglob('*.py'):
        if fix_bare_except_in_file(filepath):
            print(f"Fixed: {filepath}")
            files_fixed += 1

    print(f"\nTotal files fixed: {files_fixed}")

if __name__ == '__main__':
    main()
