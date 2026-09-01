"""Tag payloads for Bridge craft action — mirrors the browser userscript."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.api.base import Post


def _cat_list(post: Post, *labels: str) -> list[str]:
    cats = post.tag_categories or {}
    out: list[str] = []
    seen: set[str] = set()
    for label in labels:
        for key in (label, label.lower(), label.capitalize()):
            for tag in cats.get(key) or []:
                t = str(tag).strip().replace(" ", "_").lower()
                if t and t not in seen:
                    seen.add(t)
                    out.append(t)
    return out


def craft_tags_from_post(post: Post) -> dict:
    """Same shape as harem_bridge_send.user.js pageTags()."""
    artists = _cat_list(post, "Artist")
    characters = _cat_list(post, "Character")
    general = _cat_list(post, "General")
    rating = (post.rating or "").strip().lower()
    if rating == "general":
        rating = "g"
    elif rating in ("sensitive", "safe"):
        rating = "s"
    elif rating == "questionable":
        rating = "q"
    elif rating == "explicit":
        rating = "e"
    solo = "solo" in general
    return {
        "artists": artists,
        "characters": characters,
        "general": general,
        "rating": rating,
        "solo": solo,
    }
