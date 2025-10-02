# Changelog

All notable changes to FarBox Bucket will be documented in this file.

## [1.0.0] - 2025-10-01

### 🎉 Major Modernization Release

This release represents a complete modernization of the codebase to Python 3.8+ standards.

### Added
- **Test Infrastructure**
  - Added pytest with comprehensive configuration (`pytest.ini`)
  - Created `tests/` directory structure
  - Added `tests/test_utils.py` with utility function tests
  - Dev dependencies: pytest, pytest-cov, black, mypy, ruff

### Changed
- **Python Version**
  - **BREAKING**: Dropped Python 2.x support entirely
  - Minimum version now Python 3.8+
  - Removed all `from __future__ import` statements (287 files cleaned)
  - Removed `#coding: utf8` declarations
  - Updated string handling to Python 3 native str/bytes

- **Dependencies (All Upgraded)**
  - Flask: 0.10 → 2.3+
  - Jinja2: 2.9 → 3.1+
  - Werkzeug: Added explicit 2.3+
  - Pillow: 5.4.1 → 10.0+
  - gevent: 1.4.0 → 23.9+
  - Elasticsearch: 7.10.1 → 8.12+
  - cryptography: 2.3.1 → 41.0+
  - PyOpenSSL: 18.0.0 → 23.0+
  - itsdangerous: 1.1.0 → 2.1+
  - ujson: 2.0.3 → 5.8+
  - boto3: 1.17.54 → 1.34+
  - All other packages updated to modern versions

- **Error Handling**
  - Fixed 247 bare `except:` clauses across 114 files
  - Changed to `except Exception:` to avoid catching system exceptions
  - Improves debuggability and prevents masking critical errors

- **Code Quality**
  - Removed deprecated PyCrypto dependency (replaced with cryptography)
  - Updated import statements for Python 3 compatibility
  - Fixed urllib imports to use `urllib.parse`
  - Updated setup.py with modern metadata and classifiers

### Removed
- **BREAKING**: Python 2 compatibility layer entirely removed
- Removed enum34 dependency (built-in to Python 3.4+)
- Removed setuptools version constraint (was for Python 2)

### Fixed
- String/bytes handling now consistent across codebase
- Unicode regex patterns updated from `ur'...'` to `r'...'`
- Import errors from Python 2/3 compatibility fallbacks
- Fixed SyntaxWarning for invalid escape sequences in regex patterns

### Cleanup (5 files removed)
- **Removed `for_dev/` directory** - Development/debugging scripts (4 files)
- **Removed `utils/simple_encrypt.py`** - Unused utility (redundant)
- **Enhanced `.gitignore`** - Comprehensive Python/IDE/test exclusions
- **All cache files cleaned** - __pycache__, *.pyc, .DS_Store

### Migration Guide

#### For Developers
1. **Update Python version**: Ensure Python 3.8 or higher
   ```bash
   python3 --version  # Should be 3.8+
   ```

2. **Install updated dependencies**:
   ```bash
   pip install farbox_bucket==1.0.0
   # Or for development:
   pip install farbox_bucket[dev]==1.0.0
   ```

3. **Run tests**:
   ```bash
   pytest tests/
   ```

#### For Deployment
- Docker images will need to use Python 3.8+ base images
- Update any deployment scripts that assume Python 2
- Review custom extensions for Python 3 compatibility

### Known Issues / TODO
- Encryption modules still use old Crypto.Cipher API (functional but should migrate)
- No type hints yet (added mypy for future use)
- Test coverage incomplete (basic utility tests only)

---

## [0.2020] - 2020 (Legacy)

Last release with Python 2 support. Deprecated.
