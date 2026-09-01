# Fork guide — rebasing Harem booru-viewer onto upstream

This document is the **source of truth** for agents (and humans) updating
`harem-booru-viewer/` when [pxlwh/booru-viewer](https://github.com/pxlwh/booru-viewer)
ships a new release.

## Repositories and paths

| Item | Value |
|------|--------|
| Upstream | `https://github.com/pxlwh/booru-viewer` |
| Harem fork (this tree) | `slavique-harem-bot/harem-booru-viewer/` |
| Harem-only package | `booru_viewer/harem/` |
| Browser userscript (do not modify for viewer work) | `link_bridge/userscript/harem_bridge_send.user.js` |
| Bridge hook server | `link_bridge/browser_hook.py` (port **8767**, path `/send`) |

## Design rules (do not break)

1. **Upstream parity** — Default experience must match stock booru-viewer except for the two Harem features below.
2. **Isolated Harem code** — New logic goes in `booru_viewer/harem/`. Upstream files get only small `HAREM_FORK` hunks.
3. **Separate data directory** — `APPNAME` must stay `harem-booru-viewer` (not `booru-viewer`).
4. **Bridge contract** — POST JSON: `{url, source: "browser", action, tags?}`. Actions: `checkres`, `conjure`, `both`, `craft`. Same as the userscript.
5. **Userscript untouched** — Browser-only users keep using Tampermonkey; the desktop client is optional.

## Harem-only files (never delete on rebase)

```
booru_viewer/harem/
  __init__.py
  bridge.py          # HTTP to 127.0.0.1:8767
  controller.py      # Qt toolbar → bridge
  defaults.py        # Danbooru + Rule34 seeding
  post_url.py        # Post page URL for Bridge
  tags.py            # craft payload from Post.tag_categories
  menu.py            # RMB submenu for bridge actions
tests/harem/
  test_harem_fork.py
AGENTS.md
FORK_GUIDE.md          # this file
README_HAREM.md
```

## Upstream files with Harem hunks (grep `HAREM_FORK`)

After every upstream merge, verify these markers still exist and compile:

| File | Change |
|------|--------|
| `booru_viewer/core/config.py` | `APPNAME = "harem-booru-viewer"` |
| `booru_viewer/core/db.py` | Call `ensure_default_sites(self)` after `_migrate()` |
| `booru_viewer/gui/preview_pane.py` | `append_bridge_actions` at top of RMB menu + signal |
| `booru_viewer/gui/popout/window.py` | Same in popout RMB menu |
| `booru_viewer/gui/settings.py` | Thumbnail max 500px, optional scroll speed multiplier (HAREM_FORK) |
| `booru_viewer/gui/main_window.py` | `HaremBridgeController`, signal wiring |
| `booru_viewer/gui/popout_controller.py` | Connect popout `harem_bridge_requested` |
| `booru_viewer/main_gui.py` | `SetCurrentProcessExplicitAppUserModelID(u"slavique.harem-booru-viewer.gui.1")` |
| `pyproject.toml` | `name = "harem-booru-viewer"`, version `{upstream}-harem.{n}`, extra script entry |

Find all markers:

```bash
cd harem-booru-viewer
rg "HAREM_FORK" -n
```

## Rebase procedure (agent checklist)

### 1. Record versions

- Read `harem-booru-viewer/pyproject.toml` → current `version` (e.g. `0.3.1+harem`).
- Read upstream latest tag on GitHub (e.g. `v0.3.2`).

### 2. Fresh upstream checkout

```bash
git clone --depth 1 --branch v0.3.2 https://github.com/pxlwh/booru-viewer.git /tmp/booru-viewer-upstream
```

Use the tag the user requested; if none, use latest release tag.

### 3. Merge strategy

**Preferred:** three-way merge with the previous fork base commit if this directory is git-tracked.

**Practical (monorepo):**

1. Back up Harem-only paths listed above.
2. Delete everything in `harem-booru-viewer/` except those backups and docs.
3. Copy `/tmp/booru-viewer-upstream/*` into `harem-booru-viewer/`.
4. Restore Harem-only paths from backup.
5. Re-apply each `HAREM_FORK` hunk (use `rg HAREM_FORK` on backup or git diff from last fork commit).

### 4. Resolve conflicts by area

| Conflict area | Resolution |
|---------------|------------|
| `preview_pane.py` / `popout/window.py` toolbar | Keep upstream toolbar structure; re-insert `HaremBridgeBar` block before `addStretch()` |
| `main_window.py` imports / `__init__` | Keep upstream controller order; re-add `HaremBridgeController` next to `PostActionsController` |
| `db.py` `conn` property | Keep upstream migration order; call `ensure_default_sites` **after** `_migrate()` and `_restrict_perms()` |
| `config.py` | Keep Harem `APPNAME` |
| Tests | Upstream tests replace; keep `tests/harem/` |

### 5. Verify

```bash
cd harem-booru-viewer
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install -e .
python -m pytest tests/harem -q
python -m pytest tests/core -q   # optional broader smoke
```

Manual (Windows):

1. Start Harem Link Bridge (tray app).
2. `harem-booru-viewer` from venv.
3. Site combo shows **Danbooru** and **Rule34** without manual add.
4. Search Danbooru, select a post → preview toolbar shows four bridge buttons.
5. Click **both** → Bridge log shows browser action; bot DM/checkres as usual.
6. Popout (fullscreen) → same buttons work.
7. Userscript on danbooru.donmai.us still works with Bridge running.

### 6. Version bump

In `pyproject.toml`:

```
version = "0.3.2+harem.1"
```

Increment the `harem.N` suffix for follow-up fork fixes on the same upstream tag.

### 7. Deliverables

- Updated `harem-booru-viewer/` tree with passing `tests/harem`.
- Short changelog in commit message: upstream tag + any conflict notes.
- If GUI layout shifted, update the table in **Upstream files with Harem hunks** above.

## Default sites reference

```python
HAREM_DEFAULT_SITES = (
    ("Danbooru", "https://danbooru.donmai.us", "danbooru"),
    ("Rule34", "https://rule34.xxx", "gelbooru"),
)
```

Rule34 uses Gelbooru API shape; users still add API key/user id in **Manage Sites** when needed (same as upstream README).

## Bridge troubleshooting

| Symptom | Check |
|---------|--------|
| "Bridge not running" | Harem Link Bridge tray app; `browser_hook_enabled` in `harem_link_bridge.json` |
| craft fails | OmniCraft card must be open in Bridge |
| conjure no DM | `source` must be `"browser"` in payload (fork sends this intentionally) |
| Wrong post URL | `post_url.py` — compare with `main_window._open_post_id_in_browser` upstream |

## Future: Windows .exe

Upstream uses PyInstaller (`booru-viewer.spec`) and Inno Setup (`installer.iss`). For Harem releases:

1. Copy spec/installer; rename artifacts to `harem-booru-viewer`.
2. Point `APPNAME` / icons / AppUserModelID at Harem branding.
3. Publish via GitHub Releases on SlaviqueBots (separate from this monorepo when ready).

Until then, dev install is `pip install -e .` from this directory.
