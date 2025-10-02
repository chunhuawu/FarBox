"""
Navigation helpers for menus, breadcrumbs, etc.
"""
from typing import Any, Dict, Optional, List


class NavigationHelper:
    """
    Handles navigation elements like menus, breadcrumbs, and TOC.
    """

    @staticmethod
    def create_link(
        title: str,
        url: Optional[str] = None,
        dom_id: Optional[str] = None,
        class_name: str = '',
        target: str = '',
        **kwargs: Any
    ) -> str:
        """
        Create an HTML anchor tag.

        Args:
            title: Link text
            url: Link URL
            dom_id: DOM ID for the link
            class_name: CSS class names
            target: Link target (_blank, _self, etc.)
            **kwargs: Additional HTML attributes

        Returns:
            HTML anchor tag string
        """
        if not url:
            url = '#'

        attrs = []
        if dom_id:
            attrs.append(f'id="{dom_id}"')
        if class_name:
            attrs.append(f'class="{class_name}"')
        if target:
            attrs.append(f'target="{target}"')

        for key, value in kwargs.items():
            if value:
                key = key.replace('_', '-')
                attrs.append(f'{key}="{value}"')

        attrs_str = ' ' + ' '.join(attrs) if attrs else ''
        return f'<a href="{url}"{attrs_str}>{title}</a>'

    @staticmethod
    def create_nav_menu(nav_items: List[Dict[str, Any]], **kwargs: Any) -> str:
        """
        Create a navigation menu from items.

        Args:
            nav_items: List of navigation item dicts with 'title' and 'url'
            **kwargs: Additional options for menu rendering

        Returns:
            HTML navigation menu
        """
        if not nav_items:
            return ''

        menu_items = []
        for item in nav_items:
            title = item.get('title', '')
            url = item.get('url', '#')
            active = item.get('active', False)

            class_name = 'nav-item'
            if active:
                class_name += ' active'

            link = NavigationHelper.create_link(title, url, class_name=class_name)
            menu_items.append(f'<li>{link}</li>')

        return f'<ul class="nav-menu">{"".join(menu_items)}</ul>'

    @staticmethod
    def back_to_top(label: str = '△', class_name: str = 'back-to-top') -> str:
        """
        Create a back-to-top button.

        Args:
            label: Button label
            class_name: CSS class

        Returns:
            HTML back-to-top button
        """
        return f'<a href="#" class="{class_name}" onclick="window.scrollTo(0,0);return false;">{label}</a>'

    @staticmethod
    def create_breadcrumbs(items: List[Dict[str, str]]) -> str:
        """
        Create breadcrumb navigation.

        Args:
            items: List of dicts with 'title' and 'url'

        Returns:
            HTML breadcrumb navigation
        """
        if not items:
            return ''

        breadcrumb_items = []
        for i, item in enumerate(items):
            title = item.get('title', '')
            url = item.get('url', '')
            is_last = i == len(items) - 1

            if is_last:
                breadcrumb_items.append(f'<span class="breadcrumb-current">{title}</span>')
            else:
                link = NavigationHelper.create_link(title, url)
                breadcrumb_items.append(link)

        return f'<nav class="breadcrumbs">{" / ".join(breadcrumb_items)}</nav>'
