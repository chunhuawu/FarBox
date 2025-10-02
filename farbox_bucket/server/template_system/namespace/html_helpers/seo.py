"""
SEO and meta tag helpers.
"""
from typing import Optional, Dict, Any
from flask import request


class SEOHelper:
    """
    Helpers for SEO meta tags and optimization.
    """

    def __init__(self):
        """Initialize SEO helper."""
        self.meta_tags: Dict[str, str] = {}

    def set_meta(self, key: str, value: str) -> None:
        """
        Set a meta tag value.

        Args:
            key: Meta tag name or property
            value: Meta tag content
        """
        self.meta_tags[key] = value

    def set_metas(self, **kwargs: str) -> None:
        """
        Set multiple meta tags.

        Args:
            **kwargs: Meta tag key-value pairs
        """
        self.meta_tags.update(kwargs)

    def set_seo(self, keywords: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Set SEO meta tags (keywords and description).

        Args:
            keywords: Meta keywords
            description: Meta description
        """
        if keywords:
            self.set_meta('keywords', keywords)
        if description:
            self.set_meta('description', description)

    def render_meta_tags(self) -> str:
        """
        Render all meta tags as HTML.

        Returns:
            HTML meta tags
        """
        tags = []
        for key, value in self.meta_tags.items():
            if key in ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']:
                tags.append(f'<meta property="{key}" content="{value}">')
            elif key in ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']:
                tags.append(f'<meta name="{key}" content="{value}">')
            else:
                tags.append(f'<meta name="{key}" content="{value}">')
        return '\n'.join(tags)

    def mobile_metas(self) -> str:
        """
        Generate mobile-friendly meta tags.

        Returns:
            HTML mobile meta tags
        """
        return '''
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
        '''.strip()

    def create_open_graph_tags(
        self,
        title: str,
        description: Optional[str] = None,
        image: Optional[str] = None,
        url: Optional[str] = None,
        type_: str = 'website'
    ) -> str:
        """
        Create Open Graph meta tags for social sharing.

        Args:
            title: Page title
            description: Page description
            image: Image URL
            url: Page URL
            type_: OG type (website, article, etc.)

        Returns:
            HTML Open Graph meta tags
        """
        if not url and hasattr(request, 'url'):
            url = request.url

        self.set_meta('og:title', title)
        self.set_meta('og:type', type_)

        if description:
            self.set_meta('og:description', description)
        if image:
            self.set_meta('og:image', image)
        if url:
            self.set_meta('og:url', url)

        return self.render_meta_tags()

    def create_twitter_card(
        self,
        title: str,
        description: Optional[str] = None,
        image: Optional[str] = None,
        card_type: str = 'summary'
    ) -> str:
        """
        Create Twitter Card meta tags.

        Args:
            title: Card title
            description: Card description
            image: Card image URL
            card_type: Card type (summary, summary_large_image, etc.)

        Returns:
            HTML Twitter Card meta tags
        """
        self.set_meta('twitter:card', card_type)
        self.set_meta('twitter:title', title)

        if description:
            self.set_meta('twitter:description', description)
        if image:
            self.set_meta('twitter:image', image)

        return self.render_meta_tags()
