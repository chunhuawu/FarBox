# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FarBox Bucket is a content management and synchronization system built on Flask. It provides a Docker-deployable web platform that syncs content from client applications, stores data in SSDB and Elasticsearch, and renders websites using a custom template system.

**Version:** 1.0.0 (Modernized for Python 3.8+)

## 🎉 Recent Modernization (v1.0.0)

This codebase underwent major modernization. All Python 2 support removed, dependencies upgraded, error handling fixed.

### ✅ Completed
- **Python 3.8+ only** - Removed 287 files with `__future__` imports
- **Fixed 247 bare `except:` → `except Exception:`** across 114 files
- **Upgraded all dependencies** - Flask 2.3+, Jinja2 3.1+, Pillow 10+, etc.
- **Test suite added** - pytest infrastructure with basic tests
- **Development tools** - black, mypy, ruff in extras

### ⚠️ TODO
- Add type hints to core modules
- Migrate encryption from PyCrypto to cryptography library
- Expand test coverage (integration + unit tests)

## Key Commands

### Installation & Deployment
```bash
# Install from PyPI
pip install farbox_bucket

# Deploy FarBox Bucket (creates Docker container)
deploy_farbox_bucket memcache=2g project=farbox_bucket start_project=true

# Deploy with remote sync backup
deploy_farbox_bucket memcache=5g remote_node=xxx.com

# Update deployment configuration
update_deploy_farbox_bucket [project_name]

# Upgrade to latest version
farbox_bucket_upgrade

# Upgrade to specific version
farbox_bucket_upgrade 0.2020
```

### Service Management
```bash
# Restart web server (sends HUP signal)
farbox_bucket_restart_web

# Restart memcache
farbox_bucket_restart_cache

# Build Docker image
build_farbox_bucket
```

### Client Management
```bash
# List all projects
farbox_bucket projects

# Show project details
farbox_bucket project <project_name>

# Set remote node for a project
farbox_bucket set_<project> --node=<node_url>

# Register domain
farbox_bucket set_<project> --domain=<domain>

# Unregister domain (prefix with -)
farbox_bucket set_<project> --domain=-<domain>
```

### Development
```bash
# Check version
deploy_farbox_bucket version
```

## Architecture

### Core Components

**Server Layer** ([farbox_bucket/server/](farbox_bucket/server/))
- **web_app.py**: Flask application initialization with custom `FarBoxBucketFlask` class
  - Before/after request handlers for caching, statistics, authentication
  - Custom static file serving with different cache TTLs (10 min for templates, 3 hours for static, 10 days for system)
  - Sentry integration for error tracking
- **template_system/**: Jinja2-based template rendering with custom namespaces (post, bucket, request, response, html)
- **es/**: Elasticsearch integration for full-text search
- **backend/**: Background job processing
- **realtime/**: WebSocket support via farbox-gevent-websocket
- **statistics/**: Usage tracking and post visit analytics

**Bucket Layer** ([farbox_bucket/bucket/](farbox_bucket/bucket/))
- **record/**: Core data models and SSDB database operations
- **storage/**: Storage abstraction supporting local filesystem ([local_file_system.py](farbox_bucket/bucket/storage/local_file_system.py)), Tencent Cloud ([qcloud_storage.py](farbox_bucket/bucket/storage/qcloud_storage.py))
- **sync/**: Server-side sync protocol handlers
- **clouds/**: Third-party integrations (currently only WeChat)
- **domain/**: Custom domain management
- **token/**: Authentication token handling
- **web_api/**: REST API endpoints

**Client Layer** ([farbox_bucket/client/](farbox_bucket/client/))
- **sync/**: Client-side file synchronization
  - [sync.py](farbox_bucket/client/sync/sync.py): `FarBoxBucketSyncWorker` class handles file detection, encryption, IPFS integration
  - **compiler/**: Pre-processing files before sync (Markdown, images, etc.)
- **sync_from/**: Pull sync from remote servers
- Python API for programmatic sync:
  ```python
  from farbox_bucket.client.sync import sync_to_farbox
  sync_to_farbox(node="<server>", root="<path>", private_key="<key>")
  ```

**Utilities** ([farbox_bucket/utils/](farbox_bucket/utils/))
- **encrypt/**: DES and AES encryption ([des_encrypt.py](farbox_bucket/utils/encrypt/des_encrypt.py), [aes_encrypt.py](farbox_bucket/utils/encrypt/aes_encrypt.py))
- **client_sync/**: File system monitoring and change detection
- **image/**: Image processing with Pillow
- **md_related/**: Markdown processing (uses farbox-markdown and farbox-misaka)
- **convert/**: File format conversions
- **mail/**: Email utilities
- **pay/**: Payment integration

**Deployment** ([farbox_bucket/deploy/](farbox_bucket/deploy/))
- **build/**: Docker image building ([build_image.py](farbox_bucket/deploy/build/build_image.py))
- **run/**: Runtime configuration (gunicorn, supervisord, memcached)
- **run/configs/**: Server configuration files for gunicorn, backend jobs

### Data Storage

- **SSDB**: Primary key-value database (port varies by deployment)
- **Elasticsearch 7.10.1**: Full-text search indexes
- **Memcached**: Response caching (configurable memory, default 2GB)
- **Local/Cloud Storage**: File storage via abstraction layer

### Request Flow

1. **Before Request**: `basic_before_request` → `site_visitor_password_before_request` → `time_cost_handler`
2. **Request Processing**: Routes defined in [farbox_bucket/server/views/](farbox_bucket/server/views/)
3. **After Request**: `time_cost_handler` → `cache_response_into_memcache` → `default_response_handler` → `after_request_func_for_statistics`

### View Loading Order (Important)

Views are loaded in this specific order in [web_app.py](farbox_bucket/server/web_app.py:76-99):
1. Custom views from `my_farbox_bucket` (if exists)
2. System views (authentication, SSL)
3. API views
4. Admin views
5. User views
6. File manager
7. Avatar views
8. WeChat integration
9. Wiki link fallback
10. Bucket views (catch-all, must be last)

### File Synchronization Protocol

- Client detects file changes and computes MD5 hashes
- Files can be encrypted before upload (DES/AES)
- Optional IPFS integration for distributed storage
- `.files_info.json` tracks sync state locally
- Server validates via private_key authentication

## Key Dependencies

- **Flask 0.10**: Web framework
- **Jinja2 2.9**: Template engine (also supports PyJade)
- **gevent 1.4.0**: Async I/O
- **pyssdb 0.4.1**: SSDB client
- **elasticsearch 7.10.1**: Search
- **Pillow 5.4.1+**: Image processing
- **pycrypto 2.6.1**: Encryption
- **xserver**: Deployment orchestration

## File Organization

- Configuration lives in `/home/run/farbox/` when deployed
- Data directories: `/data/farbox_ssdb`, `/data/farbox_es`, `/data/farbox`, `/data/log/farbox`
- Static assets: [farbox_bucket/server/static/](farbox_bucket/server/static/)
- Themes: [farbox_bucket/themes/](farbox_bucket/themes/) (Cais, Classify, Esta, Fexo, Puti, Sollrei, Wiki)

## Development Notes

- The codebase uses Python 2/3 compatibility (`from __future__ import absolute_import`)
- Version is defined in [farbox_bucket/__init__.py](farbox_bucket/__init__.py:4)
- Custom Flask subclass overrides `send_static_file` and `get_send_file_max_age` for security and caching
- Template system is patched via `patch_context()` before app initialization
- No formal test suite exists; testing appears to be done manually via deployment
