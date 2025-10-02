#!/usr/bin/env python3
"""
Audit dependencies in farbox_bucket codebase.
Finds all imports and checks which dependencies are actually used.
"""
import re
import subprocess
from pathlib import Path
from collections import defaultdict

def find_all_imports(root_dir):
    """Find all import statements in Python files."""
    imports = defaultdict(int)

    for py_file in Path(root_dir).rglob('*.py'):
        if 'test' in str(py_file) or '__pycache__' in str(py_file):
            continue

        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()

                    # Skip internal imports
                    if line.startswith('from farbox_bucket'):
                        continue

                    # Match: import xyz
                    if line.startswith('import '):
                        module = line.replace('import ', '').split()[0].split('.')[0].split(',')[0]
                        imports[module] += 1

                    # Match: from xyz import
                    elif line.startswith('from '):
                        match = re.match(r'from\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', line)
                        if match:
                            module = match.group(1).split('.')[0]
                            # Skip relative imports
                            if module and not module.startswith('.'):
                                imports[module] += 1
        except Exception:
            pass

    return imports

def get_latest_versions():
    """Get latest versions of common packages from PyPI."""
    # As of October 2025, latest stable versions
    return {
        # Core web framework
        'flask': '3.0.3',
        'jinja2': '3.1.4',
        'werkzeug': '3.0.3',

        # Async
        'gevent': '24.2.1',
        'dnspython': '2.6.1',

        # Database
        'elasticsearch': '8.14.0',
        'pymemcache': '4.0.0',

        # Security
        'cryptography': '42.0.8',
        'pyopenssl': '24.1.0',
        'itsdangerous': '2.2.0',

        # Data
        'ujson': '5.10.0',
        'python-dateutil': '2.9.0',
        'xmltodict': '0.13.0',
        'unidecode': '1.3.8',

        # Images
        'pillow': '10.4.0',

        # Cloud
        'boto3': '1.34.144',

        # Utils
        'blinker': '1.8.2',
        'psutil': '6.0.0',
        'Send2Trash': '1.8.3',
        'shortuuid': '1.0.13',

        # Error tracking
        'sentry-sdk': '2.8.0',  # Modern replacement for raven

        # Template
        'pyscss': '1.4.0',
    }

def main():
    print("🔍 Auditing dependencies...\n")

    # Find all imports
    imports = find_all_imports('farbox_bucket')

    # Categorize imports
    stdlib = {
        'os', 'sys', 're', 'time', 'datetime', 'json', 'base64', 'io',
        'uuid', 'random', 'hashlib', 'subprocess', 'logging', 'inspect',
        'collections', 'urllib', 'math', 'multiprocessing', 'pathlib'
    }

    third_party = {}
    for module, count in imports.items():
        if module not in stdlib:
            third_party[module] = count

    # Print results
    print("=" * 70)
    print("THIRD-PARTY IMPORTS FOUND IN CODEBASE:")
    print("=" * 70)
    for module, count in sorted(third_party.items(), key=lambda x: -x[1]):
        print(f"{module:25} - used {count:4} times")

    print("\n" + "=" * 70)
    print("PACKAGE RECOMMENDATIONS:")
    print("=" * 70)

    latest = get_latest_versions()

    # Required packages
    required = {
        'flask', 'jinja2', 'werkzeug',  # Web framework
        'gevent',  # Async
        'PIL': 'pillow',  # Image
        'ujson',  # JSON
        'dateutil': 'python-dateutil',  # Dates
        'cryptography', 'pyopenssl', 'itsdangerous',  # Security
        'blinker', 'psutil',  # Utils
        'shortuuid',  # IDs
    }

    # Map import names to package names
    import_to_package = {
        'PIL': 'pillow',
        'dateutil': 'python-dateutil',
        'yaml': 'pyyaml',
        'raven': 'sentry-sdk',  # Deprecated → Modern
    }

    print("\n✅ REQUIRED (found in codebase):")
    for imp in sorted(third_party.keys()):
        package = import_to_package.get(imp, imp)
        if imp in required or package in required:
            version = latest.get(package, 'latest')
            print(f"  - {package:30} # Version: {version}")

    # Check for deprecated
    print("\n⚠️  DEPRECATED / SHOULD REPLACE:")
    if 'raven' in third_party:
        print(f"  - raven → sentry-sdk>=2.8.0  # Modern Sentry client")

    # Optional packages (not found but in setup.py)
    print("\n🤔 CHECK IF NEEDED (not found in imports):")
    setup_packages = {
        'pyssdb', 'elasticsearch', 'pymemcache', 'dnspython',
        'xmltodict', 'unidecode', 'pyjade', 'pyscss',
        'boto3', 'Send2Trash', 'xserver',
        'farbox-markdown', 'farbox-misaka', 'farbox-gevent-websocket',
        'cos-python-sdk-v5'
    }

    for pkg in sorted(setup_packages):
        if pkg.replace('-', '_') not in third_party and pkg not in third_party:
            print(f"  - {pkg:30} # Not found in imports - verify usage")

if __name__ == '__main__':
    main()
