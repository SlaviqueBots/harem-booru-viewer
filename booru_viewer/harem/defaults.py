"""Pre-configured booru sites for Harem users."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.db import Database

# (display name, base URL, api_type)
HAREM_DEFAULT_SITES: tuple[tuple[str, str, str], ...] = (
    ("Danbooru", "https://danbooru.donmai.us", "danbooru"),
    ("Rule34", "https://rule34.xxx", "gelbooru"),
)

_DANBOORU_URL = "https://danbooru.donmai.us"


def ensure_default_sites(db: Database) -> None:
    """Add Danbooru + Rule34 when missing. Safe on every DB open."""
    existing = {
        s.url.rstrip("/").lower()
        for s in db.get_sites(enabled_only=False)
    }
    for name, url, api_type in HAREM_DEFAULT_SITES:
        key = url.rstrip("/").lower()
        if key not in existing:
            db.add_site(name, url, api_type)
            existing.add(key)

    if not db.get_setting_int("default_site_id"):
        for site in db.get_sites(enabled_only=False):
            if site.url.rstrip("/").lower() == _DANBOORU_URL.lower():
                db.set_setting("default_site_id", str(site.id))
                break
