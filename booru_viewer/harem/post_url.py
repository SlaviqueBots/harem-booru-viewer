"""Build canonical post page URLs for Harem Link Bridge."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.api.base import Post
    from ..core.db import Site


def post_page_url(post: Post, site: Site | None) -> str:
    """Return the browser post URL Bridge expects (Danbooru / Rule34 shapes)."""
    post_id = int(post.id)
    if site is None:
        return f"https://danbooru.donmai.us/posts/{post_id}"

    base = site.url.rstrip("/")
    api = site.api_type
    if api in ("danbooru", "e621"):
        return f"{base}/posts/{post_id}"
    if api == "gelbooru":
        return f"{base}/index.php?page=post&s=view&id={post_id}"
    if api == "moebooru":
        return f"{base}/post/show/{post_id}"
    return f"{base}/posts/{post_id}"
