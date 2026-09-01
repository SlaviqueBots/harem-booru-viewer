"""Browser-like back/forward history for browse/search states."""

from __future__ import annotations

from dataclasses import dataclass, field

from .search_state import SearchState


def page_is_at_end(*, api_exhausted: bool, result_count: int, page_size: int) -> bool:
    """Whether paged mode should hide the Next button.

    Trust the API exhaustion flag from fetch_site_page. Display count can be
    below page_size after blacklist/dedup/interleave even when more pages exist.
    """
    del result_count, page_size  # kept for call-site clarity / future use
    return api_exhausted


def copy_search_state(state: SearchState) -> SearchState:
    """Deep-enough copy so restoring one snapshot cannot mutate another."""
    return SearchState(
        shown_post_ids=set(state.shown_post_ids),
        page_cache={page: list(posts) for page, posts in state.page_cache.items()},
        page_api_exhausted=dict(state.page_api_exhausted),
        infinite_exhausted=state.infinite_exhausted,
        infinite_last_page=state.infinite_last_page,
        infinite_api_exhausted=state.infinite_api_exhausted,
        nav_page_turn=None,
        append_queue=list(state.append_queue),
    )


@dataclass
class BrowseSnapshot:
    """Frozen browse context — posts list is shallow-copied; SearchState is copied."""

    search_state: SearchState
    current_page: int
    current_tags: str
    current_rating: str
    min_score: int
    media_filter: str
    search_bar_text: str
    posts: list
    scroll_value: int
    selected_index: int
    infinite_scroll: bool


@dataclass
class BrowseHistory:
    """Back/forward stacks of browse snapshots (browser semantics)."""

    max_entries: int = 20
    _back: list[BrowseSnapshot] = field(default_factory=list)
    _forward: list[BrowseSnapshot] = field(default_factory=list)

    def can_go_back(self) -> bool:
        return bool(self._back)

    def can_go_forward(self) -> bool:
        return bool(self._forward)

    def push_back(self, snapshot: BrowseSnapshot) -> None:
        """New navigation — save current state and clear forward stack."""
        self._back.append(snapshot)
        if len(self._back) > self.max_entries:
            self._back.pop(0)
        self._forward.clear()

    def go_back(self, current: BrowseSnapshot) -> BrowseSnapshot | None:
        if not self._back:
            return None
        self._forward.append(current)
        if len(self._forward) > self.max_entries:
            self._forward.pop(0)
        return self._back.pop()

    def go_forward(self, current: BrowseSnapshot) -> BrowseSnapshot | None:
        if not self._forward:
            return None
        self._back.append(current)
        if len(self._back) > self.max_entries:
            self._back.pop(0)
        return self._forward.pop()

    def pop_back(self) -> BrowseSnapshot:
        return self._back.pop()

    def push_forward(self, snapshot: BrowseSnapshot) -> None:
        self._forward.append(snapshot)

    def pop_forward(self) -> BrowseSnapshot:
        return self._forward.pop()

    def clear_forward(self) -> None:
        self._forward.clear()
