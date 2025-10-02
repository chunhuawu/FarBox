# Upgrade Guide: v0.2020 → v1.0.0

## Quick Start

```bash
# 1. Ensure Python 3.8+
python3 --version  # Must be 3.8 or higher

# 2. Upgrade package
pip install --upgrade farbox_bucket

# 3. Verify installation
python3 -c "import farbox_bucket; print(farbox_bucket.version)"
# Should print: 1.0.0

# 4. Run tests (optional)
pip install farbox_bucket[test]
pytest
```

## What You Need to Know

### ✅ Safe to Upgrade If:
- You're running Python 3.8 or higher
- You're using standard deployment methods
- You're not using custom Python 2-specific code

### ⚠️ Action Required If:
- Still on Python 2.x → **Must upgrade to Python 3.8+**
- Custom extensions using `from __future__` → Remove those imports
- Custom encryption code using PyCrypto → Migrate to `cryptography`

## Breaking Changes

### 1. Python Version
**Before:** Python 2.7 or Python 3.x
**After:** Python 3.8+ only

**Action:** Update your environment
```bash
# Using pyenv
pyenv install 3.11.0
pyenv local 3.11.0

# Or Docker
FROM python:3.11-slim
```

### 2. Dependencies
Several major version bumps:
- **Flask:** 0.10 → 2.3+
- **Jinja2:** 2.9 → 3.1+
- **Elasticsearch:** 7.x → 8.x

**Action:** Review custom code using these libraries. Most usage remains compatible, but check:
- Flask blueprints (minor API changes)
- Jinja2 templates (should work as-is)
- Elasticsearch queries (API v8 has changes)

### 3. Removed PyCrypto
**Before:** Used `from Crypto.Cipher import DES, AES`
**After:** Uses `cryptography` library

**Action:** If you have custom encryption code:
```python
# Old (PyCrypto)
from Crypto.Cipher import AES

# New (cryptography)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
```

## Non-Breaking Changes

✅ These require no action:

- Error handling improvements (bare `except:` → `except Exception:`)
- Import statement modernization
- String handling updates
- Removed `#coding: utf8` declarations

## Testing Your Upgrade

### 1. Basic Smoke Test
```bash
# Start server
deploy_farbox_bucket memcache=200mb

# Check health
curl http://localhost:8000/
```

### 2. Run Test Suite
```bash
pip install farbox_bucket[dev]
pytest tests/ -v
```

### 3. Check Logs
```bash
tail -f /data/log/farbox/web.log
# Should see no errors about missing modules
```

## Rollback Plan

If issues arise:

```bash
# Rollback to old version
pip install farbox_bucket==0.2020

# Restore Python 2.7 environment if needed
pyenv local 2.7.18
```

## Common Issues

### Issue: `ImportError: No module named 'Crypto'`
**Cause:** Custom code still using PyCrypto
**Fix:** Install temporarily: `pip install pycryptodome` OR migrate to `cryptography`

### Issue: Flask templates not rendering
**Cause:** Jinja2 3.x stricter about undefined variables
**Fix:** Use `{% if variable is defined %}` in templates

### Issue: Elasticsearch connection errors
**Cause:** API v8 authentication requirements
**Fix:** Update connection code:
```python
# Old
from elasticsearch import Elasticsearch
es = Elasticsearch(['localhost:9200'])

# New
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
```

## Performance Notes

**Expected improvements:**
- 10-60% faster execution (Python 3.11 vs Python 2.7)
- Lower memory usage (modern gevent)
- Faster image processing (Pillow 10.x)

**No regressions expected** - report any performance issues to GitHub.

## Need Help?

- **Bug reports:** https://github.com/farbox/farbox_bucket/issues
- **Documentation:** See CLAUDE.md, MODERNIZATION.md
- **Migration questions:** Open a discussion

## Summary

This is a **major modernization release** that removes 5 years of technical debt. The upgrade is straightforward for most users:

1. Ensure Python 3.8+
2. `pip install --upgrade farbox_bucket`
3. Test your deployment
4. Enjoy improved security, performance, and maintainability

**Estimated downtime:** <5 minutes for typical deployment
**Risk level:** Low (for Python 3.x users), Medium (if upgrading from Python 2.x)
