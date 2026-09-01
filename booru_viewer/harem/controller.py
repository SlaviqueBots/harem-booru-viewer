"""Wire Harem Bridge actions from the image viewer toolbars."""

from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING

from PySide6.QtCore import QTimer

from .bridge import send_bridge_action
from .post_url import post_page_url
from .tags import craft_tags_from_post
from ..gui.site_selection import effective_site_id

if TYPE_CHECKING:
    from ..gui.main_window import BooruApp

log = logging.getLogger("booru.harem")


class HaremBridgeController:
    def __init__(self, app: BooruApp) -> None:
        self._app = app

    def send_action(self, action: str) -> None:
        post = self._app._preview._current_post
        if post is None:
            self._app._status.showMessage("No post selected")
            return

        site_id = effective_site_id(
            post,
            self._app._preview._current_site_id or self._app._site_combo.currentData(),
        )
        site = None
        if site_id:
            site = next(
                (s for s in self._app._db.get_sites(enabled_only=False) if s.id == site_id),
                None,
            )
        page_url = post_page_url(post, site)
        tags = craft_tags_from_post(post) if action == "craft" else None
        self._app._status.showMessage(f"Bridge [{action}]…")

        def _work() -> None:
            ok, msg = send_bridge_action(page_url, action, tags=tags)
            detail = msg if ok else f"Bridge failed: {msg}"
            if not ok:
                log.info("bridge %s: %s", action, msg)
            QTimer.singleShot(0, lambda: self._app._status.showMessage(detail))

        threading.Thread(target=_work, daemon=True).start()
