"""
DOM manipulation and utility helpers.
"""
import uuid
from typing import Union, List, Any
from farbox_bucket.utils import is_str


def get_random_dom_id() -> str:
    """
    Generate a random DOM ID.

    Returns:
        Random DOM ID string starting with 'd'
    """
    return f'd{uuid.uuid1().hex}'


def str_has(obj: Any, to_check: Union[str, List[str]], just_in: bool = False) -> bool:
    """
    Check if a string contains another string or any string from a list.

    Args:
        obj: String to search in
        to_check: String or list of strings to search for
        just_in: If True, use simple substring match; if False, match word boundaries

    Returns:
        True if match found, False otherwise
    """
    if isinstance(to_check, (tuple, list)):
        for sub_to_check in to_check[:100]:  # Max 100 items
            if isinstance(sub_to_check, str) and str_has(obj, sub_to_check, just_in=just_in):
                return True
        return False

    if not isinstance(obj, str) or not isinstance(to_check, str):
        return False

    to_check = to_check.strip().lower()
    obj = obj.strip().lower()

    if just_in:
        return to_check in obj

    to_check_start = to_check.strip() + ' '
    to_check_end = ' ' + to_check.strip()

    if is_str(to_check):
        return obj == to_check or obj.startswith(to_check_start) or obj.endswith(to_check_end)
    else:  # Chinese characters - no spaces
        return to_check in obj
