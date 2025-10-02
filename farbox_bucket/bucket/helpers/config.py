"""
Bucket configuration management.
"""
from typing import Dict, Any, Optional
from flask import request
from farbox_bucket.utils.ssdb_utils import hset, hget
from farbox_bucket.bucket.defaults import bucket_config_doc_id_names
from farbox_bucket.bucket.token.simple_encrypt_token import get_normal_data_by_simple_token
from .validation import has_bucket


# Default site configurations
DEFAULT_SITE_CONFIGS: Dict[str, Any] = {
    'title': '',
    'description': '',
    'keywords': '',
    'author': '',
    'language': 'en',
}


def get_bucket_configs(bucket: str, config_type: str = 'init') -> Dict[str, Any]:
    """
    Get configuration for a bucket.

    Args:
        bucket: Bucket name
        config_type: Type of config ('init', 'user', 'pages', 'site', 'secret')

    Returns:
        Configuration dictionary
    """
    if not bucket:
        return {}

    config_doc_id = bucket_config_doc_id_names.get(config_type)
    if not config_doc_id:
        return {}

    # Check request-level cache
    request_var_name = f'bucket_{bucket}_cached_{config_type}_value'
    if hasattr(request, request_var_name):
        return getattr(request, request_var_name)

    # Fetch from database
    info = hget(bucket, config_doc_id)
    if not info or not isinstance(info, dict):
        info = {}

    # Decrypt if needed
    if config_type in ['user', 'secret'] and info:
        raw_data = info.get('data')
        real_info = get_normal_data_by_simple_token(bucket, raw_data, force_py_data=True)
        if not isinstance(real_info, dict):
            real_info = {}
        info = real_info

    # Apply defaults for site config
    if config_type == "site" and has_bucket(bucket):
        site_configs = DEFAULT_SITE_CONFIGS.copy()
        site_configs.update(info)
        info = site_configs

    # Cache in request context
    try:
        setattr(request, request_var_name, info)
    except Exception:
        pass

    return info


def get_bucket_init_configs(bucket: str) -> Dict[str, Any]:
    """Get initialization configs for a bucket."""
    return get_bucket_configs(bucket, config_type='init')


def get_bucket_user_configs(bucket: str) -> Dict[str, Any]:
    """Get user configs for a bucket."""
    return get_bucket_configs(bucket, config_type='user')


def get_bucket_pages_configs(bucket: str) -> Dict[str, Any]:
    """Get pages configs for a bucket."""
    return get_bucket_configs(bucket, config_type='pages')


def get_bucket_site_configs(bucket: Optional[str] = None) -> Dict[str, Any]:
    """Get site configs for a bucket."""
    if not bucket:
        from .context import get_bucket_in_request_context
        bucket = get_bucket_in_request_context()

    return get_bucket_configs(bucket, config_type='site') if bucket else {}


def get_bucket_secret_site_configs(bucket: Optional[str] = None) -> Dict[str, Any]:
    """Get secret site configs for a bucket."""
    if not bucket:
        from .context import get_bucket_in_request_context
        bucket = get_bucket_in_request_context()

    return get_bucket_configs(bucket, config_type='secret') if bucket else {}


def set_bucket_configs(
    bucket: str,
    configs: Dict[str, Any],
    config_type: str = 'site',
    by_system: bool = False
) -> bool:
    """
    Set configuration for a bucket.

    Args:
        bucket: Bucket name
        configs: Configuration dictionary to set
        config_type: Type of config to set
        by_system: Whether this is a system-initiated change

    Returns:
        True if successful, False otherwise
    """
    if not bucket:
        return False

    config_doc_id = bucket_config_doc_id_names.get(config_type)
    if not config_doc_id:
        return False

    # Merge with existing config
    existing_config = get_bucket_configs(bucket, config_type)
    existing_config.update(configs)

    # Save to database
    hset(bucket, config_doc_id, existing_config)

    # Invalidate request cache
    request_var_name = f'bucket_{bucket}_cached_{config_type}_value'
    if hasattr(request, request_var_name):
        delattr(request, request_var_name)

    return True
