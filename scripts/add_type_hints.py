#!/usr/bin/env python3
"""
Add type hints and docstrings to critical modules.
This script helps migrate the codebase to modern Python with type annotations.
"""
import os
import re
from pathlib import Path


# Type hint templates for common patterns
TYPE_HINT_PATTERNS = {
    # String parameters
    r'def (\w+)\(([^)]*\bpath\b[^)]*)\)': 'str',
    r'def (\w+)\(([^)]*\bname\b[^)]*)\)': 'str',
    r'def (\w+)\(([^)]*\bkey\b[^)]*)\)': 'str',
    r'def (\w+)\(([^)]*\bvalue\b[^)]*)\)': 'Any',
    r'def (\w+)\(([^)]*\bnamespace\b[^)]*)\)': 'str',

    # Boolean parameters
    r'def (\w+)\(([^)]*\bis_\w+[^)]*)\)': 'bool',
    r'def (\w+)\(([^)]*\bforce_\w+[^)]*)\)': 'bool',

    # Number parameters
    r'def (\w+)\(([^)]*\bcount\b[^)]*)\)': 'int',
    r'def (\w+)\(([^)]*\blimit\b[^)]*)\)': 'int',
    r'def (\w+)\(([^)]*\bmax_\w+[^)]*)\)': 'int',
    r'def (\w+)\(([^)]*\bmin_\w+[^)]*)\)': 'int',
}


def add_type_hints_to_data_py():
    """Add type hints to farbox_bucket/utils/data.py"""
    filepath = Path('/Users/chunhuawu/Library/Mobile Documents/com~apple~CloudDocs/Chunhua Wu/150 Wu Lab/FarBox/farbox_bucket/utils/data.py')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add typing imports
    if 'from typing import' not in content:
        import_line = 'from typing import Any, Optional, Union, Dict, List, Tuple\n'
        # Insert after existing imports
        import_section_end = content.find('\nclass ') if '\nclass ' in content else content.find('\ndef ')
        if import_section_end > 0:
            content = content[:11] + import_line + content[11:]

    # Update json_dumps signature
    content = re.sub(
        r'def json_dumps\(obj, indent=None\):',
        'def json_dumps(obj: Any, indent: Optional[int] = None) -> str:',
        content
    )

    # Update json_loads signature
    content = re.sub(
        r'def json_loads\(raw_content\):',
        'def json_loads(raw_content: str) -> Any:',
        content
    )

    # Update csv_to_list signature
    content = re.sub(
        r'def csv_to_list\(raw_content, max_rows=None, max_columns=None, return_max_length=False, auto_fill=False\):',
        'def csv_to_list(raw_content: Union[str, bytes], max_rows: Optional[int] = None, max_columns: Optional[int] = None, return_max_length: bool = False, auto_fill: bool = False) -> Union[List[List[str]], Tuple[List[List[str]], int]]:',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Added type hints to {filepath.name}")


def add_type_hints_to_path_py():
    """Add type hints to farbox_bucket/utils/path.py"""
    filepath = Path('/Users/chunhuawu/Library/Mobile Documents/com~apple~CloudDocs/Chunhua Wu/150 Wu Lab/FarBox/farbox_bucket/utils/path.py')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add typing imports if not present
    if 'from typing import' not in content:
        import_line = 'from typing import Optional, List\n'
        content = import_line + content

    # Common path function signatures
    replacements = [
        (r'def read_file\(filepath\):', 'def read_file(filepath: str) -> Optional[str]:'),
        (r'def write_file\(filepath, content\):', 'def write_file(filepath: str, content: str) -> bool:'),
        (r'def get_relative_path\(path, base_path\):', 'def get_relative_path(path: str, base_path: str) -> str:'),
        (r'def join_path\(\*paths\):', 'def join_path(*paths: str) -> str:'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Added type hints to {filepath.name}")


def add_docstrings_to_module(filepath: Path, module_description: str):
    """Add module-level docstring if missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if module docstring exists
    if not content.startswith('"""') and not content.startswith("'''"):
        docstring = f'"""\n{module_description}\n"""\n'
        # Find first import or code line
        first_code_line = 0
        for i, line in enumerate(content.split('\n')):
            if line.strip() and not line.strip().startswith('#'):
                first_code_line = content.find(line)
                break

        content = docstring + content[first_code_line:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    return False


def main():
    """Add type hints to critical modules."""
    print("Adding type hints and docstrings to critical modules...\n")

    # Add type hints to specific critical files
    print("Phase 1: Adding type hints to data utilities...")
    add_type_hints_to_data_py()

    print("\nPhase 2: Adding type hints to path utilities...")
    add_type_hints_to_path_py()

    # Add module docstrings
    print("\nPhase 3: Adding module docstrings...")
    modules_to_document = [
        ('farbox_bucket/utils/date.py', 'Date and time utility functions.'),
        ('farbox_bucket/utils/url.py', 'URL manipulation and parsing utilities.'),
        ('farbox_bucket/utils/html.py', 'HTML processing and sanitization utilities.'),
        ('farbox_bucket/utils/cache.py', 'Caching decorators and utilities.'),
        ('farbox_bucket/utils/memcache.py', 'Memcached client wrapper and utilities.'),
    ]

    project_root = Path('/Users/chunhuawu/Library/Mobile Documents/com~apple~CloudDocs/Chunhua Wu/150 Wu Lab/FarBox')
    for module_path, description in modules_to_document:
        full_path = project_root / module_path
        if full_path.exists():
            if add_docstrings_to_module(full_path, description):
                print(f"  ✓ Added docstring to {module_path}")

    print("\n" + "=" * 60)
    print("Type hints and docstrings added successfully!")
    print("Note: Manual review and refinement recommended")
    print("=" * 60)


if __name__ == '__main__':
    main()
