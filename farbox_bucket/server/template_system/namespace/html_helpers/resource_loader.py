"""
Static resource loading and management.
"""
from typing import List, Dict, Optional, Any
from farbox_bucket.utils.env import get_env


# Lazy load resource mappings
LAZY_LOAD_MAP: Dict[str, Any] = {
    'font': '/fb_static/lib/fontawesome/css/font-awesome.min.css',
    'jquery': '/fb_static/lib/jquery.js',
    'pure': ['/fb_static/lib/pure.css', '/fb_static/lib/pure_patch.css'],
    'form': '/fb_static/lib/wtf-forms.css',
    'markdown': '/fb_static/lib/markdown/markdown.css',
    'essage': ['/fb_static/lib/essage/essage.css', '/fb_static/lib/essage/essage.js'],
    'opensans': '/fb_static/lib/fonts/open_sans.css',
    'open_sans': '/fb_static/lib/fonts/open_sans.css',
    'merriweather': '/fb_static/lib/fonts/merriweather.css',
    'animate': '/fb_static/lib/animate.3.5.2.min.css',
    'animation': '/fb_static/lib/animate.3.5.2.min.css',
    'donghua': '/fb_static/lib/animate.3.5.2.min.css',
    "post_preview": "/fb_static/basic/post_preview.css",
}


class ResourceLoader:
    """
    Manages loading of static resources (CSS, JS) in templates.
    """

    def __init__(self):
        """Initialize resource loader with configuration."""
        self.static_files_url = (get_env("static_files_url") or "").strip().strip("/")
        self.qcloud_cdn_token = (get_env("qcloud_cdn_token") or "").strip()
        self.loaded_resources: set = set()

    def get_resource_url(self, resource_name: str) -> Optional[str]:
        """
        Get URL for a named resource.

        Args:
            resource_name: Name of the resource (e.g., 'jquery', 'font')

        Returns:
            Resource URL or None if not found
        """
        return LAZY_LOAD_MAP.get(resource_name.lower())

    def load(self, *resources: str, force: bool = False) -> str:
        """
        Load static resources (CSS/JS files).

        Args:
            *resources: Resource names to load
            force: Force reload even if already loaded

        Returns:
            HTML tags for loading resources
        """
        if not resources:
            return ''

        html_parts: List[str] = []

        for resource in resources:
            if not force and resource in self.loaded_resources:
                continue

            resource_url = self.get_resource_url(resource)
            if resource_url:
                if isinstance(resource_url, list):
                    for url in resource_url:
                        html_parts.append(self._create_resource_tag(url))
                else:
                    html_parts.append(self._create_resource_tag(resource_url))

                self.loaded_resources.add(resource)

        return '\n'.join(html_parts)

    def _create_resource_tag(self, url: str) -> str:
        """
        Create HTML tag for a resource based on its extension.

        Args:
            url: Resource URL

        Returns:
            HTML link or script tag
        """
        if url.endswith('.css'):
            return f'<link rel="stylesheet" href="{url}">'
        elif url.endswith('.js'):
            return f'<script src="{url}"></script>'
        return ''

    def is_loaded(self, resource_name: str) -> bool:
        """
        Check if a resource has already been loaded.

        Args:
            resource_name: Resource name

        Returns:
            True if loaded, False otherwise
        """
        return resource_name in self.loaded_resources
