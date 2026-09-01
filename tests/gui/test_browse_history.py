"""Tests for browse history and pagination end detection."""

from __future__ import annotations

from typing import NamedTuple

from booru_viewer.gui.browse_history import (
    BrowseHistory,
    BrowseSnapshot,
    copy_search_state,
    page_is_at_end,
)
from booru_viewer.gui.search_state import SearchState


class _Post(NamedTuple):
    id: int
    site_id: int = 1


def _snap(tags: str, posts: list | None = None, page: int = 1, scroll: int = 120) -> BrowseSnapshot:
    ss = SearchState()
    if posts:
        ss.page_cache[page] = list(posts)
        ss.shown_post_ids = {(p.site_id, p.id) for p in posts}
    return BrowseSnapshot(
        search_state=ss,
        current_page=page,
        current_tags=tags,
        current_rating="all",
        min_score=0,
        media_filter="All",
        search_bar_text=tags,
        posts=list(posts or []),
        scroll_value=scroll,
        selected_index=2,
        infinite_scroll=False,
    )


def test_page_at_end_uses_api_exhausted_not_short_page():
    assert page_is_at_end(api_exhausted=False, result_count=10, page_size=40) is False
    assert page_is_at_end(api_exhausted=True, result_count=10, page_size=40) is True
    assert page_is_at_end(api_exhausted=False, result_count=40, page_size=40) is False
    assert page_is_at_end(api_exhausted=True, result_count=40, page_size=40) is True


def test_search_a_to_b_back_restores_a():
    hist = BrowseHistory()
    a = _snap("artist:a", [_Post(1), _Post(2)])
    b = _snap("artist:b", [_Post(3)])
    hist.push_back(a)
    restored = hist.go_back(b)
    assert restored is not None
    assert restored.current_tags == "artist:a"
    assert len(restored.posts) == 2


def test_search_a_to_b_back_forward_restores_b():
    hist = BrowseHistory()
    a = _snap("artist:a")
    b = _snap("artist:b")
    hist.push_back(a)
    hist.go_back(b)
    restored = hist.go_forward(a)
    assert restored is not None
    assert restored.current_tags == "artist:b"


def test_multi_page_cache_preserved_in_snapshot():
    ss = SearchState()
    ss.page_cache = {1: [_Post(1)], 2: [_Post(2)], 3: [_Post(3)]}
    ss.page_api_exhausted = {1: False, 2: False, 3: True}
    snap = BrowseSnapshot(
        search_state=copy_search_state(ss),
        current_page=3,
        current_tags="a b",
        current_rating="all",
        min_score=0,
        media_filter="All",
        search_bar_text="a b",
        posts=[_Post(3)],
        scroll_value=500,
        selected_index=0,
        infinite_scroll=True,
    )
    assert len(snap.search_state.page_cache) == 3
    assert snap.search_state.page_api_exhausted[3] is True


def test_back_then_new_search_clears_forward():
    hist = BrowseHistory()
    a = _snap("artist:a")
    b = _snap("artist:b")
    c = _snap("artist:c")
    hist.push_back(a)
    hist.go_back(b)
    assert hist.can_go_forward()
    hist.push_back(c)
    assert not hist.can_go_forward()


def test_empty_back_forward_are_no_ops():
    hist = BrowseHistory()
    current = _snap("x")
    assert hist.go_back(current) is None
    assert hist.go_forward(current) is None


def test_copy_search_state_does_not_alias_mutable_fields():
    ss = SearchState()
    ss.page_cache[1] = [_Post(1)]
    ss.shown_post_ids.add((1, 1))
    copy = copy_search_state(ss)
    ss.page_cache[1].append(_Post(2))
    ss.shown_post_ids.add((1, 99))
    assert len(copy.page_cache[1]) == 1
    assert (1, 99) not in copy.shown_post_ids


def test_tag_navigation_creates_history_entry():
    hist = BrowseHistory()
    before = _snap("artist:a", [_Post(i) for i in range(5)])
    hist.push_back(before)
    assert hist.can_go_back()
    after = hist.go_back(_snap("artist:b", [_Post(99)]))
    assert after.current_tags == "artist:a"
    assert len(after.posts) == 5


def test_scroll_position_preserved_in_snapshot():
    snap = _snap("tags", scroll=999)
    assert snap.scroll_value == 999


def test_consecutive_tag_navigations_stack():
    hist = BrowseHistory()
    hist.push_back(_snap("a"))
    hist.push_back(_snap("a b"))
    hist.push_back(_snap("a b c"))
    assert len(hist._back) == 3
