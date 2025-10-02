#!/usr/bin/env python3
"""
Core utility functions for FarBox Bucket.
Refactored for Python 3.8+ with type hints and improved clarity.
"""
import sys
import re
import os
import hashlib
import datetime
from typing import Any, Union, Optional, List, Callable
from urllib.parse import urlparse, parse_qs, urlencode
import urllib.parse as urllib_parse

import ujson as json
from collections import OrderedDict
from dateutil.parser import parse as parse_date

# Type aliases
StringLike = Union[str, bytes]
Numeric = Union[int, float]

# Legacy compatibility (for existing code)
string_types = (str, bytes)
unicode = str
unicode_type = str
str_type = bytes


class UnicodeWithAttrs(str):
    """String subclass that can have attributes attached."""
    pass


# ============================================================================
# String/Bytes Conversion
# ============================================================================

def to_bytes(s: Any) -> bytes:
    """Convert any value to bytes using UTF-8."""
    if isinstance(s, bytes):
        return s
    if isinstance(s, str):
        return s.encode('utf-8')
    return str(s).encode('utf-8')


def to_unicode(s: Any) -> str:
    """Convert any value to unicode string."""
    if isinstance(s, str):
        return s
    if isinstance(s, bytes):
        for encoding in ("utf-8", "gb18030", "latin1", "ascii"):
            try:
                return s.decode(encoding)
            except (UnicodeDecodeError, AttributeError):
                continue
        return s.decode('utf-8', errors='replace')
    return str(s)


# Aliases for backwards compatibility
smart_str = to_bytes
smart_unicode = to_unicode


# ============================================================================
# Hashing Functions
# ============================================================================

def to_md5(text: Any) -> str:
    """Calculate MD5 hash of text."""
    return hashlib.md5(to_bytes(text)).hexdigest()


def to_sha1(content: Any) -> str:
    """Calculate SHA1 hash of content."""
    return hashlib.sha1(to_bytes(content)).hexdigest()


def hash_password(password: str) -> str:
    """Hash password using MD5→SHA1."""
    return to_sha1(to_md5(password))


def get_md5_for_file(file_path: str, block_size: int = 1024 * 1024) -> str:
    """Calculate MD5 hash of file contents."""
    if os.path.isdir(file_path):
        return 'folder'
    if not os.path.exists(file_path):
        return ''

    md5_obj = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(block_size):
            md5_obj.update(chunk)
    return md5_obj.hexdigest()


# Aliases
md5 = get_md5 = to_md5
get_sha1 = to_sha1
md5_for_file = get_md5_for_file


# ============================================================================
# Type Conversion
# ============================================================================

def to_number(
    value: Any,
    default_if_fail: Optional[Numeric] = None,
    max_value: Optional[Numeric] = None,
    min_value: Optional[Numeric] = None,
    number_type_func: Optional[Callable] = None
) -> Optional[Numeric]:
    """Convert value to number with optional constraints."""
    if isinstance(value, str):
        value = value.strip()

    if not value and not isinstance(value, int):
        return default_if_fail

    try:
        result = float(value)
        if number_type_func:
            result = number_type_func(result)
    except (ValueError, TypeError):
        return default_if_fail

    if max_value is not None and result > max_value:
        result = max_value
    if min_value is not None and result < min_value:
        result = min_value

    return result


def to_int(
    value: Any,
    default_if_fail: Optional[int] = None,
    max_value: Optional[int] = None,
    min_value: Optional[int] = None
) -> Optional[int]:
    """Convert value to integer."""
    return to_number(value, default_if_fail, max_value, min_value, int)


def to_float(
    value: Any,
    default_if_fail: Optional[float] = None,
    max_value: Optional[float] = None,
    min_value: Optional[float] = None
) -> Optional[float]:
    """Convert value to float, supporting fractions like '1/2'."""
    if isinstance(value, str) and '/' in value and value.count('/') == 1:
        numerator, denominator = value.split('/', 1)
        num = to_float(numerator)
        den = to_float(denominator)
        if num is not None and den is not None and den != 0:
            value = num / den
    return to_number(value, default_if_fail, max_value, min_value, float)


def to_date(value: Any) -> Optional[datetime.datetime]:
    """Convert value to datetime object."""
    if not value:
        return None
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(getattr(value, 'core', None), datetime.datetime):
        return value.core
    try:
        return parse_date(value)
    except Exception:
        return None


def auto_type(value: Any) -> Any:
    """Auto-convert string to appropriate type (int/float/bool)."""
    if not isinstance(value, str):
        return value

    value = value.strip()

    # Integer
    if re.match(r'^\d+$', value):
        return int(value)

    # Float
    if re.match(r'^\d+\.(\d+)?$', value):
        return float(value)

    # Fraction
    if re.match(r'^\d+/\d+$', value):
        result = to_float(value)
        if result is not None:
            return result

    # Boolean
    if value in ('True', 'true', 'yes'):
        return True
    if value in ('False', 'false', 'no'):
        return False

    return value


def string_to_int(value: Any) -> Optional[int]:
    """Extract first integer found in string."""
    if not value:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        match = re.search(r'\d+', value)
        if match:
            return int(match.group())
    return to_int(value)


# ============================================================================
# Validation
# ============================================================================

def is_str(text: Any, includes: str = '') -> bool:
    """Check if text is valid alphanumeric string."""
    if not isinstance(text, (str, bytes)):
        return False

    text = to_unicode(text).strip()

    if includes:
        for char in includes:
            text = text.replace(char, '')

    return bool(text and re.match(r'[a-z0-9_\-]+$', text, re.I))


def are_letters(s: Any) -> bool:
    """Check if string contains only letters."""
    return isinstance(s, str) and bool(re.match(r'[a-z]+$', s, re.I))


def is_public(value: Any) -> bool:
    """Check if value indicates 'public/open' state."""
    return value in (True, 'public', 'open', 'on', 'published', 'true', 'yes')


def is_closed(value: Any) -> bool:
    """Check if value indicates 'closed/off' state."""
    return value in ('no', 'false', False, 'off', 'close')


is_on = is_public  # Alias


_EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$',
    re.I
)


def is_email_address(email: Any) -> bool:
    """Validate email address format."""
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_RE.match(email.strip()))


_DOMAIN_RE = re.compile(
    r'^([a-z0-9][a-z0-9-_]+[a-z0-9]\.|[a-z0-9]+\.)+([a-z]{2,3}\.)?[a-z]{2,9}$',
    re.I
)


# ============================================================================
# List/Collection Utilities
# ============================================================================

def unique_list(data: List[Any]) -> List[Any]:
    """Remove duplicates while preserving order."""
    seen = set()
    result = []
    for item in data:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def string_to_list(value: Any) -> List[str]:
    """Convert string/list to list, splitting on comma/space."""
    if not value:
        return []

    if isinstance(value, (list, tuple)):
        return [to_unicode(item).strip() for item in unique_list(value) if item]

    if not isinstance(value, str):
        return [to_bytes(value)]

    value = value.strip()

    # Remove surrounding brackets/parentheses
    if value.startswith('[') and value.endswith(']'):
        value = value[1:-1].strip()
    elif value.startswith('(') and value.endswith(')'):
        value = value[1:-1].strip()

    # Split on comma (English or Chinese) or space
    if ',' in value:
        items = value.split(',')
    elif '，' in value:
        items = value.split('，')
    else:
        items = value.split()

    return unique_list([item.strip() for item in items if item.strip()])


def split_list(ls: List[Any], size_per_part: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    for i in range(0, len(ls), size_per_part):
        yield ls[i:i + size_per_part]


def sort_objects_by(objects: List[Any], attr: str) -> List[Any]:
    """Sort list of objects by attribute, '-' prefix for reverse."""
    if not isinstance(objects, (list, tuple)):
        return objects

    reverse = attr.startswith('-')
    attr = attr.lstrip('-')

    if attr:
        from farbox_bucket.utils.data import get_value_from_data
        sorted_objs = sorted(objects, key=lambda o: get_value_from_data(o, attr) or '')
    else:
        sorted_objs = list(objects)

    return list(reversed(sorted_objs)) if reverse else sorted_objs


# ============================================================================
# String Processing
# ============================================================================

def count_words(content: str) -> int:
    """Count words including CJK characters (Chinese/Japanese/Korean)."""
    content = to_unicode(content)
    return len(re.findall(r'[\w\-_/]+|[\u1100-\ufde8]', content))


def make_content_clean(content: str) -> str:
    """Remove control characters and normalize whitespace."""
    content = to_unicode(content).replace('\xa0', ' ')
    return re.sub(r'[\x07-\x1f]', '', content)


MARKDOWN_EXTS = ('.txt', '.md', '.markdown', '.mk')


def is_a_markdown_file(path: Optional[str]) -> bool:
    """Check if file path has markdown extension."""
    if not path:
        return False
    return os.path.splitext(path)[1].lower() in MARKDOWN_EXTS


# ============================================================================
# Misc Utilities
# ============================================================================

def get_uuid() -> str:
    """Generate UUID hex string."""
    import uuid
    return uuid.uuid1().hex


def get_random_html_dom_id() -> str:
    """Generate random DOM ID with 'd_' prefix."""
    return f'd_{get_uuid()}'


def bytes2human(num: Optional[int]) -> str:
    """Convert bytes to human-readable format."""
    if not num:
        return '0'

    for unit in ('bytes', 'KB', 'MB', 'GB', 'PB'):
        if num < 1024.0:
            return f"{num:3.1f}{unit}"
        num /= 1024.0

    return f"{num:3.1f}TB"


def get_kwargs_from_console() -> dict:
    """Parse key=value arguments from command line."""
    kwargs = {}
    for arg in sys.argv:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key.strip()] = value.strip()
    return kwargs


def force_to_json(data: Any) -> dict:
    """Convert string to JSON dict, return empty dict on failure."""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except Exception:
            return {}
    return data if isinstance(data, dict) else {}


def get_dict_from_dict(data: dict, key: str) -> dict:
    """Safely extract dict value from dict, return empty dict if missing/wrong type."""
    if not isinstance(data, dict):
        return {}
    value = data.get(key, {})
    return value if isinstance(value, dict) else {}


def get_value_from_data(data: Any, attr: str, default: Any = None) -> Any:
    """
    Get nested attribute/key from data using dot notation.
    Examples: get_value_from_data(obj, 'user.name.first')
    Max depth: 25 levels
    """
    if not isinstance(attr, str):
        return default

    # Direct key access for dicts
    if isinstance(data, dict) and attr in data:
        return data[attr]

    try:
        # Traverse nested attributes/keys
        attrs = attr.split('.')[:25]  # Max 25 levels deep
        for attr_name in attrs:
            if isinstance(data, (dict, OrderedDict)):
                data = data.get(attr_name)
            else:
                try:
                    data = getattr(data, attr_name, None)
                except Exception:  # Jinja Undefined triggers error
                    return data

            if data is None:
                return default
    except RuntimeError:  # External g/request calls can fail
        return None

    return data
