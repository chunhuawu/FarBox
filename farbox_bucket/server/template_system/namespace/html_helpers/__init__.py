"""
Modular HTML helpers split from the monolithic html.py.
Each submodule handles a specific concern.
"""
from .dom_helpers import get_random_dom_id, str_has
from .resource_loader import ResourceLoader
from .navigation import NavigationHelper
from .forms import FormHelper
from .seo import SEOHelper

__all__ = [
    'get_random_dom_id',
    'str_has',
    'ResourceLoader',
    'NavigationHelper',
    'FormHelper',
    'SEOHelper',
]
