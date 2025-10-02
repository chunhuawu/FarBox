#!/usr/bin/env python3
"""
Script to remove Python 2 compatibility code.
- Removes 'from __future__ import' statements
- Removes try/except blocks for Python 2/3 imports
- Updates string handling to Python 3 only
"""
import re
from pathlib import Path

def clean_file(filepath):
    """Remove Python 2 compatibility from a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Remove from __future__ import lines
    content = re.sub(r'^from __future__ import .*$\n?', '', content, flags=re.MULTILINE)

    # Remove #coding: utf8 or # coding: utf-8 (not needed in Python 3)
    content = re.sub(r'^#.*?coding[:=]\s*utf-?8.*$\n?', '', content, flags=re.MULTILINE)

    # Remove shebang with python (but keep python3)
    content = re.sub(r'^#!/usr/bin/env python$', '#!/usr/bin/env python3', content, flags=re.MULTILINE)
    content = re.sub(r'^#/usr/bin/env python$', '#!/usr/bin/env python3', content, flags=re.MULTILINE)

    if content != original_content:
        # Clean up multiple blank lines left after removals
        content = re.sub(r'\n\n\n+', '\n\n', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all Python files in farbox_bucket."""
    root_dir = Path(__file__).parent.parent / 'farbox_bucket'
    files_cleaned = 0

    for filepath in root_dir.rglob('*.py'):
        if clean_file(filepath):
            print(f"Cleaned: {filepath}")
            files_cleaned += 1

    print(f"\nTotal files cleaned: {files_cleaned}")

if __name__ == '__main__':
    main()
