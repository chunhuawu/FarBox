"""
Modular bucket helpers split from the monolithic bucket/utils.py.
Each module handles a specific aspect of bucket management.
"""
from .validation import is_valid_bucket_name, has_bucket
from .keys import (
    get_bucket_by_public_key,
    get_bucket_by_private_key,
    get_public_key_from_bucket
)
from .context import (
    get_bucket_in_request_context,
    set_bucket_in_request_context
)
from .config import (
    get_bucket_configs,
    get_bucket_init_configs,
    get_bucket_user_configs,
    get_bucket_site_configs,
    set_bucket_configs
)
from .info import (
    get_bucket_files_info,
    get_bucket_posts_info,
    get_buckets_size
)

__all__ = [
    # Validation
    'is_valid_bucket_name',
    'has_bucket',
    # Keys
    'get_bucket_by_public_key',
    'get_bucket_by_private_key',
    'get_public_key_from_bucket',
    # Context
    'get_bucket_in_request_context',
    'set_bucket_in_request_context',
    # Config
    'get_bucket_configs',
    'get_bucket_init_configs',
    'get_bucket_user_configs',
    'get_bucket_site_configs',
    'set_bucket_configs',
    # Info
    'get_bucket_files_info',
    'get_bucket_posts_info',
    'get_buckets_size',
]
