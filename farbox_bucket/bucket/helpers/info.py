"""
Bucket information and statistics helpers.
"""
from typing import Dict, Any
from farbox_bucket.utils.ssdb_utils import hget, hsize


def get_bucket_files_info(bucket: str) -> Dict[str, Any]:
    """
    Get files information for a bucket.

    Args:
        bucket: Bucket name

    Returns:
        Dictionary with files information
    """
    if not bucket:
        return {}

    return hget(bucket, "__files_info__", force_dict=True)


def get_bucket_posts_info(bucket: str) -> Dict[str, Any]:
    """
    Get posts information for a bucket.

    Args:
        bucket: Bucket name

    Returns:
        Dictionary with posts information
    """
    if not bucket:
        return {}

    return hget(bucket, "__posts_info__", force_dict=True)


def get_bucket_files_configs(bucket: str) -> Dict[str, Any]:
    """
    Get files configuration for a bucket.

    Args:
        bucket: Bucket name

    Returns:
        Dictionary with files configuration
    """
    if not bucket:
        return {}

    return hget(bucket, "__files__", force_dict=True)


def get_buckets_size() -> int:
    """
    Get the total number of buckets in the system.

    Returns:
        Total number of buckets
    """
    try:
        return hsize("__buckets__")
    except Exception:
        return 0
