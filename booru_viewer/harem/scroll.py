"""Grid scroll speed — auto-scales with thumbnail size (400px ≈ 2× vs 200px baseline)."""

from __future__ import annotations

from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QScrollArea

# Stock booru-viewer default thumb size — scroll feel is tuned for this.
BASELINE_THUMB_SIZE = 200

_MULTIPLIER = 1.0


def set_scroll_multiplier(value: float) -> None:
    global _MULTIPLIER
    _MULTIPLIER = max(0.25, min(10.0, float(value)))


def scroll_multiplier() -> float:
    return _MULTIPLIER


def parse_scroll_multiplier(raw: str | None, *, default: float = 1.0) -> float:
    try:
        return max(0.25, min(10.0, float((raw or "").strip() or default)))
    except (TypeError, ValueError):
        return default


def effective_scroll_multiplier(user_mult: float, thumb_size: int) -> float:
    """User setting × (thumb_size / 200). At 400px + 1× → 2× wheel distance."""
    size = max(1, int(thumb_size))
    return user_mult * (size / BASELINE_THUMB_SIZE)


def _native_wheel_delta(scroll: QScrollArea, event: QWheelEvent) -> int:
    """Match QAbstractScrollArea::wheelEvent distance (scrollbar steps untouched)."""
    px = event.pixelDelta()
    if px.y() != 0:
        return px.y()
    dy = event.angleDelta().y()
    if dy == 0:
        return 0
    num_degrees = dy / 8.0
    num_steps = num_degrees / 15.0
    return int(num_steps * scroll.verticalScrollBar().singleStep())


def apply_wheel_multiplier(
    scroll: QScrollArea, event: QWheelEvent, *, thumb_size: int
) -> bool:
    """Custom scroll when effective speed ≠ 1×. Otherwise caller uses super().wheelEvent()."""
    effective = effective_scroll_multiplier(scroll_multiplier(), thumb_size)
    if abs(effective - 1.0) < 0.001:
        return False

    delta = _native_wheel_delta(scroll, event)
    if delta == 0:
        return False

    sb = scroll.verticalScrollBar()
    sb.setValue(sb.value() - int(delta * effective))
    event.accept()
    return True
