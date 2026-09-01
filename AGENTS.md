# Harem booru-viewer fork — agent instructions

Fork of [pxlwh/booru-viewer](https://github.com/pxlwh/booru-viewer) for Harem Link Bridge users.
Upstream behaviour is preserved; Harem-specific code lives under `booru_viewer/harem/`.

## What this fork adds

1. **Default sites** — Danbooru + Rule34 are inserted on first DB open (and back-filled if missing).
2. **Bridge toolbar** — Preview + popout viewers get `checkres`, `conjure`, `both`, `craft` buttons that POST to `http://127.0.0.1:8767/send` (same contract as `link_bridge/userscript/harem_bridge_send.user.js`).
3. **Separate data dir** — `APPNAME = harem-booru-viewer` so this install does not touch upstream `booru-viewer` data.

The browser userscript is **unchanged**. Users can keep using Tampermonkey only.

## Dev run (Windows)

```powershell
cd harem-booru-viewer
python -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]" 2>$null; .\.venv\Scripts\pip install -e .
.\.venv\Scripts\harem-booru-viewer
```

Requires **mpv** on PATH (same as upstream). Harem Link Bridge must be running for bridge buttons.

Optional: `HAREM_BRIDGE_HOOK_URL=http://127.0.0.1:8767/send`

## Tests

```powershell
cd harem-booru-viewer
.\.venv\Scripts\python -m pytest tests/harem -q
.\.venv\Scripts\python -m pytest tests/core tests/harem -q   # smoke without full GUI suite
```

## Forking a new upstream release

**Read `FORK_GUIDE.md` in this directory** — that is the step-by-step playbook for rebasing onto a new `pxlwh/booru-viewer` tag.

Short version for agents:

1. Note current fork base: `pyproject.toml` → `version` (e.g. `0.3.1+harem` means upstream `0.3.1`).
2. Clone/fetch upstream at the new tag into a temp dir.
3. Copy upstream tree over `harem-booru-viewer/` **except**:
   - `booru_viewer/harem/` (entire package — keep as-is, fix imports only if upstream moved modules)
   - `tests/harem/`
   - `FORK_GUIDE.md`, `AGENTS.md`, `README_HAREM.md`
4. Re-apply **integration markers** — grep `HAREM_FORK` in the current fork and replay each hunk on the new tree:
   - `booru_viewer/core/config.py` — `APPNAME = "harem-booru-viewer"`
   - `booru_viewer/core/db.py` — `ensure_default_sites(self)` after migrate
   - `booru_viewer/gui/preview_pane.py` — bridge RMB submenu + signal
   - `booru_viewer/gui/popout/window.py` — same
   - `booru_viewer/gui/main_window.py` — `HaremBridgeController` + connections + wider preview min width
   - `booru_viewer/gui/popout_controller.py` — popout bridge signal
   - `booru_viewer/main_gui.py` — Windows AppUserModelID
   - `pyproject.toml` — package name/version script entry
5. Run `pytest tests/harem` and fix breakages from upstream API/GUI moves.
6. Bump `version` to `{upstream}-harem.{n}`.
7. Manual smoke: launch app, confirm Danbooru/Rule34 in site list, open a post, click `both` with Bridge running.

Do **not** change upstream files beyond the `HAREM_FORK` touch points unless a merge conflict requires it.
