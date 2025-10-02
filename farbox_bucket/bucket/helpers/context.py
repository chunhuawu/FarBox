"""
Bucket context management for request handling.
"""
from typing import Optional
from flask import request


def get_bucket_in_request_context() -> Optional[str]:
    """
    Get the bucket associated with the current request.

    Returns:
        Bucket name or None if not set
    """
    try:
        return getattr(request, "bucket", None)
    except Exception:
        return None


def set_bucket_in_request_context(bucket: str) -> None:
    """
    Set the bucket for the current request context.

    Args:
        bucket: Bucket name to set
    """
    try:
        request.bucket = bucket
    except Exception:
        pass
