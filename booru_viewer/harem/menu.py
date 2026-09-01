"""Harem Link Bridge entries for viewer context menus."""

from __future__ import annotations

from PySide6.QtWidgets import QMenu

ACTIONS: tuple[tuple[str, str, str], ...] = (
    ("checkres", "checkres", "Send checkres to bot DMs only"),
    ("conjure", "conjure", "Run Conjure Finder only (DM result if from browser)"),
    ("both", "both", "checkres + Conjure Finder"),
    ("craft", "craft", "Add this post to the open OmniCraft card's crafting plan"),
)


def append_bridge_actions(parent: QMenu) -> dict[int, str]:
    """Flat bridge actions at the top of the menu. Returns QAction id → action id."""
    out: dict[int, str] = {}
    for action_id, label, tip in ACTIONS:
        act = parent.addAction(label)
        act.setToolTip(tip)
        out[id(act)] = action_id
    return out
