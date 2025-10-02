#!/usr/bin/env python3
"""
Pytest configuration and fixtures for FarBox Bucket tests.
"""
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture
def mock_db_client():
    """Mock SSDB database client."""
    client = Mock()
    client.hset = Mock(return_value=True)
    client.hget = Mock(return_value=None)
    client.hexists = Mock(return_value=False)
    client.hdel = Mock(return_value=True)
    client.hgetall = Mock(return_value={})
    return client


@pytest.fixture
def mock_settings():
    """Mock settings module."""
    settings = MagicMock()
    settings.DEBUG = False
    settings.MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    settings.MAX_RECORD_SIZE = 1024 * 1024  # 1MB
    settings.db_client = None
    return settings


@pytest.fixture
def sample_bucket_data():
    """Sample bucket data for testing."""
    return {
        '_id': 'test_bucket_id',
        'bucket': 'testbucket',
        'owner': 'test@example.com',
        'created_at': '2025-01-01T00:00:00',
        'updated_at': '2025-01-01T00:00:00',
        'configs': {
            'title': 'Test Bucket',
            'description': 'A test bucket'
        }
    }


@pytest.fixture
def sample_record_data():
    """Sample record data for testing."""
    return {
        '_id': 'test_record_id',
        'bucket': 'testbucket',
        'path': '/test/file.md',
        'type': 'post',
        'title': 'Test Post',
        'content': 'This is test content.',
        'date': '2025-01-01',
        'status': 'public',
        'tags': ['test', 'sample'],
        'created_at': '2025-01-01T00:00:00',
        'updated_at': '2025-01-01T00:00:00',
    }


@pytest.fixture(autouse=True)
def reset_caches():
    """Reset any module-level caches between tests."""
    # Clear SSDB data cache
    from farbox_bucket.utils import ssdb_utils
    if hasattr(ssdb_utils, 'ssdb_data_to_py_data_cache'):
        ssdb_utils.ssdb_data_to_py_data_cache.clear()

    yield

    # Cleanup after test
    if hasattr(ssdb_utils, 'ssdb_data_to_py_data_cache'):
        ssdb_utils.ssdb_data_to_py_data_cache.clear()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
