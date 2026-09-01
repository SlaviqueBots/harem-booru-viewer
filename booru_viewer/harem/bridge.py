"""HTTP client for Harem Link Bridge browser hook (127.0.0.1:8767/send)."""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request

log = logging.getLogger("booru.harem")

# Match link_bridge default; override for dev: HAREM_BRIDGE_HOOK_URL=http://127.0.0.1:8767/send
_HOOK_URL = os.environ.get(
    "HAREM_BRIDGE_HOOK_URL",
    "http://127.0.0.1:8767/send",
).rstrip("/")
if not _HOOK_URL.endswith("/send"):
    _HOOK_URL = f"{_HOOK_URL}/send"

_VALID_ACTIONS = frozenset({"checkres", "conjure", "both", "craft"})


def bridge_hook_url() -> str:
    return _HOOK_URL


def send_bridge_action(
    post_url: str,
    action: str,
    *,
    tags: dict | None = None,
) -> tuple[bool, str]:
    """POST to Bridge. Returns (ok, user-facing detail or error)."""
    url = (post_url or "").strip()
    act = (action or "").strip().lower()
    if not url:
        return False, "No post URL"
    if act not in _VALID_ACTIONS:
        act = "both"

    payload: dict = {"url": url, "source": "browser", "action": act}
    if act == "craft" and tags:
        payload["tags"] = tags

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        _HOOK_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read().decode("utf-8", errors="replace")
            data = json.loads(raw or "{}")
            return False, str(data.get("error") or data.get("detail") or f"HTTP {exc.code}")
        except Exception:
            return False, f"Bridge HTTP {exc.code}"
    except urllib.error.URLError as exc:
        log.debug("bridge hook unreachable: %s", exc)
        return False, "Bridge not running? Start Harem Link Bridge on this PC."
    except TimeoutError:
        return False, "Bridge timed out"
    except OSError as exc:
        log.debug("bridge hook failed: %s", exc)
        return False, "Bridge not running? Start Harem Link Bridge on this PC."

    try:
        data = json.loads(raw or "{}")
    except json.JSONDecodeError:
        return False, "Bridge replied unexpectedly"

    if data.get("ok", True):
        return True, str(data.get("detail") or f"Sent to Bridge ({act})")
    return False, str(data.get("error") or "Bridge rejected request")
