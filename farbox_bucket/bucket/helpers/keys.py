"""
Bucket key management helpers.
"""
from typing import Optional
from farbox_bucket.utils import to_sha1
from farbox_bucket.utils.encrypt.key_encrypt import (
    is_valid_public_key,
    to_clean_key,
    get_public_key_from_private_key,
)
from farbox_bucket.utils.ssdb_utils import hget


def get_bucket_by_public_key(public_key: str, verify: bool = True) -> Optional[str]:
    """
    Get bucket name from public key.

    The bucket name is derived from the SHA1 hash of the public key.

    Args:
        public_key: RSA public key
        verify: Whether to verify the public key is valid

    Returns:
        Bucket name (40-char SHA1 hash) or None if invalid
    """
    if not public_key:
        return None

    if verify and not is_valid_public_key(public_key):
        return None

    public_key = to_clean_key(public_key)
    public_key_id = to_sha1(public_key)
    return public_key_id


def get_bucket_by_private_key(private_key: str) -> Optional[str]:
    """
    Get bucket name from private key.

    Extracts the public key from the private key, then derives the bucket name.

    Args:
        private_key: RSA private key

    Returns:
        Bucket name or None if invalid
    """
    if not private_key:
        return None

    public_key = get_public_key_from_private_key(private_key)
    return get_bucket_by_public_key(public_key, verify=False)


def get_public_key_from_bucket(bucket: str) -> Optional[str]:
    """
    Get the public key associated with a bucket.

    Args:
        bucket: Bucket name

    Returns:
        Public key or None if not found
    """
    if not bucket:
        return None

    return hget(bucket, "public_key")
