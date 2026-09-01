"""Tests for Harem fork helpers."""

from __future__ import annotations

from booru_viewer.core.api.base import Post
from booru_viewer.core.db import Database
from booru_viewer.harem.defaults import ensure_default_sites, HAREM_DEFAULT_SITES
from booru_viewer.harem.post_url import post_page_url
from booru_viewer.harem.scroll import (
    effective_scroll_multiplier,
    parse_scroll_multiplier,
    set_scroll_multiplier,
)
from booru_viewer.harem.tags import craft_tags_from_post


def test_ensure_default_sites_seeds_danbooru_and_rule34(tmp_path):
    db = Database(tmp_path / "booru.db")
    _ = db.conn
    ensure_default_sites(db)
    names = {s.name for s in db.get_sites(enabled_only=False)}
    urls = {s.url.rstrip("/") for s in db.get_sites(enabled_only=False)}
    assert "Danbooru" in names
    assert "Rule34" in names
    assert "https://danbooru.donmai.us" in urls
    assert "https://rule34.xxx" in urls
    assert db.get_setting_int("default_site_id") > 0
    db.close()


def test_ensure_default_sites_idempotent(tmp_path):
    db = Database(tmp_path / "booru.db")
    _ = db.conn
    ensure_default_sites(db)
    count_first = len(db.get_sites(enabled_only=False))
    ensure_default_sites(db)
    assert len(db.get_sites(enabled_only=False)) == count_first == len(HAREM_DEFAULT_SITES)
    db.close()


def test_post_page_url_danbooru_and_rule34():
    post = Post(
        id=12345,
        file_url="https://example.test/a.jpg",
        preview_url=None,
        tags="solo",
        score=1,
        rating="s",
        source=None,
    )
    from booru_viewer.core.db import Site

    dan = Site(1, "Danbooru", "https://danbooru.donmai.us", "danbooru", None, None, True)
    r34 = Site(2, "Rule34", "https://rule34.xxx", "gelbooru", None, None, True)
    assert post_page_url(post, dan) == "https://danbooru.donmai.us/posts/12345"
    assert (
        post_page_url(post, r34)
        == "https://rule34.xxx/index.php?page=post&s=view&id=12345"
    )


def test_scroll_speed_multiplier():
    set_scroll_multiplier(1.0)
    assert parse_scroll_multiplier(None) == 1.0
    assert effective_scroll_multiplier(1.0, 200) == 1.0
    assert effective_scroll_multiplier(1.0, 400) == 2.0
    assert effective_scroll_multiplier(2.0, 400) == 4.0
    set_scroll_multiplier(1.0)


def test_craft_tags_from_post():
    post = Post(
        id=1,
        file_url="https://example.test/a.jpg",
        preview_url=None,
        tags="solo blue_hair",
        score=0,
        rating="explicit",
        source=None,
        tag_categories={
            "Artist": ["artist_one"],
            "Character": ["miku"],
            "General": ["solo", "blue_hair"],
        },
    )
    tags = craft_tags_from_post(post)
    assert tags["artists"] == ["artist_one"]
    assert tags["characters"] == ["miku"]
    assert "solo" in tags["general"]
    assert tags["rating"] == "e"
    assert tags["solo"] is True
