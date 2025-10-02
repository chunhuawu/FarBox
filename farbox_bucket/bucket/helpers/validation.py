"""
Bucket validation helpers.
"""
from typing import Optional
from farbox_bucket.utils import string_types
from farbox_bucket.utils.ssdb_utils import hexists


def is_valid_bucket_name(bucket: Optional[str]) -> bool:
    """
    Check if a bucket name is valid.

    A valid bucket name must be:
    - Non-empty string
    - Exactly 40 characters long (SHA1 hash length)

    Args:
        bucket: Bucket name to validate

    Returns:
        True if valid, False otherwise
    """
    if not bucket:
        return False
    if not isinstance(bucket, string_types):
        return False

    bucket = bucket.strip()
    return len(bucket) == 40


def has_bucket(bucket: str) -> bool:
    """
    Check if a bucket exists in the database.

    Args:
        bucket: Bucket name

    Returns:
        True if bucket exists, False otherwise
    """
    if not bucket:
        return False

    # Check if bucket has the primary key marker
    return hexists(bucket, "__bucket__")
