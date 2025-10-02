#!/usr/bin/env python3
"""
Fix invalid regex escape sequences across the codebase.
Converts patterns like '\\s' to r'\\s' where appropriate.
"""
import os
import re
from pathlib import Path


def fix_regex_escapes_in_file(filepath):
    """Fix regex escape sequences in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original_content = content
    changes_made = False

    # Pattern 1: re.match/search/findall/sub with string literals containing escape sequences
    # Match patterns like: re.match('\s', ...) -> re.match(r'\s', ...)
    patterns_to_fix = [
        # re.match('\pattern', ...) -> re.match(r'\pattern', ...)
        (r"(re\.(match|search|findall|sub|split|compile|fullmatch|finditer))\s*\(\s*'([^']*\\[sdwSDWbBnrtfv\[\](){}\\.+*?^$|][^']*)'", r"\1(r'\3'"),
        # re.match("\pattern", ...) -> re.match(r"\pattern", ...)
        (r'(re\.(match|search|findall|sub|split|compile|fullmatch|finditer))\s*\(\s*"([^"]*\\[sdwSDWbBnrtfv\[\](){}\\.+*?^$|][^"]*)"', r'\1(r"\3"'),
    ]

    for pattern, replacement in patterns_to_fix:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            changes_made = True

    # Pattern 2: Direct string patterns that look like regexes (more conservative)
    # Only fix if in re context or assigned to variable with 'pattern' in name
    if 'pattern' in content.lower() or 're.' in content:
        # Fix string literals that are clearly regex patterns
        suspicious_patterns = [
            (r"pattern\s*=\s*'([^']*\\[sdw][^']*)'", r"pattern = r'\1'"),
            (r'pattern\s*=\s*"([^"]*\\[sdw][^"]*)"', r'pattern = r"\1"'),
        ]

        for pattern, replacement in suspicious_patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                content = new_content
                changes_made = True

    if changes_made:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    return False


def main():
    """Fix regex escapes across all Python files."""
    project_root = Path(__file__).parent.parent
    python_files = list(project_root.glob('farbox_bucket/**/*.py'))

    print(f"Scanning {len(python_files)} Python files for regex escape issues...\n")

    fixed_count = 0
    for filepath in python_files:
        if fix_regex_escapes_in_file(filepath):
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"Fixed {fixed_count} files with regex escape sequence issues")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
