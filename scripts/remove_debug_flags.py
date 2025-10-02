#!/usr/bin/env python3
"""
Remove DEBUG flags and replace with proper logging.
Converts `if DEBUG:` patterns to proper logger.debug() calls.
"""
import os
import re
from pathlib import Path


def convert_debug_to_logging(filepath: Path) -> bool:
    """
    Convert DEBUG flag usage to proper logging.

    Args:
        filepath: Path to Python file

    Returns:
        True if file was modified, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original_content = content
    changes_made = False

    # Check if file uses DEBUG
    if 'DEBUG' not in content:
        return False

    # Add logging import if needed
    needs_logging = False
    if re.search(r'\bif\s+DEBUG\b', content):
        needs_logging = True

    if needs_logging and 'from farbox_bucket.core.logging import get_logger' not in content:
        # Find the import section
        import_match = re.search(r'^(from|import)\s+', content, re.MULTILINE)
        if import_match:
            insert_pos = import_match.start()
            # Add logging import
            logging_import = 'from farbox_bucket.core.logging import get_logger\n\n'
            content = content[:insert_pos] + logging_import + content[insert_pos:]

            # Add logger instance after imports
            # Find first function or class definition
            func_class_match = re.search(r'^(def|class)\s+', content, re.MULTILINE)
            if func_class_match:
                insert_pos = func_class_match.start()
                logger_line = 'logger = get_logger(__name__)\n\n'
                content = content[:insert_pos] + logger_line + content[insert_pos:]

            changes_made = True

    # Pattern 1: if DEBUG: print(...) -> logger.debug(...)
    pattern1 = r'if\s+DEBUG:\s*\n\s+print\s*\(([^)]+)\)'
    replacement1 = r'logger.debug(\1)'
    new_content = re.sub(pattern1, replacement1, content)
    if new_content != content:
        content = new_content
        changes_made = True

    # Pattern 2: if DEBUG: pass -> logger.debug("...")
    # Only convert simple cases
    pattern2 = r'if\s+DEBUG:\s*\n\s+pass'
    replacement2 = r'# Debug point - converted from DEBUG flag'
    new_content = re.sub(pattern2, replacement2, content)
    if new_content != content:
        content = new_content
        changes_made = True

    # Pattern 3: settings.DEBUG = True -> Remove (use environment instead)
    pattern3 = r'\s*settings\.DEBUG\s*=\s*True\s*'
    new_content = re.sub(pattern3, '\n    # DEBUG mode controlled by environment/logging level\n', content)
    if new_content != content:
        content = new_content
        changes_made = True

    if changes_made:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Converted DEBUG flags in: {filepath}")
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    return False


def main():
    """Convert DEBUG flags to proper logging across all Python files."""
    project_root = Path(__file__).parent.parent
    python_files = list(project_root.glob('farbox_bucket/**/*.py'))

    print(f"Scanning {len(python_files)} Python files for DEBUG flag usage...\n")

    converted_count = 0
    files_with_debug = []

    # First pass: find files using DEBUG
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'DEBUG' in content and 'if DEBUG' in content:
                files_with_debug.append(filepath)
        except Exception:
            pass

    print(f"Found {len(files_with_debug)} files using DEBUG flags\n")

    # Second pass: convert files
    for filepath in files_with_debug:
        if convert_debug_to_logging(filepath):
            converted_count += 1

    print(f"\n{'='*60}")
    print(f"Converted {converted_count} files from DEBUG flags to logging")
    print(f"{'='*60}")

    if files_with_debug and converted_count < len(files_with_debug):
        print(f"\nNote: {len(files_with_debug) - converted_count} files still need manual review")


if __name__ == '__main__':
    main()
