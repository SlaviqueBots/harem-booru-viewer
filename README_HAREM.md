# Harem booru-viewer

Desktop booru client for Harem Link Bridge users. Based on
[pxlwh/booru-viewer](https://github.com/pxlwh/booru-viewer) v0.3.1.

## Harem changes

- **Danbooru** and **Rule34** are pre-added as sites (no manual setup).
- Preview and popout viewers include **Harem Link Bridge** in the right-click menu (`checkres`, `conjure`, `both`, `craft`) — same behaviour as the browser userscript.
- Data is stored under `%APPDATA%\harem-booru-viewer\` (Windows) or `~/.local/share/harem-booru-viewer/` (Linux), separate from stock booru-viewer.

The browser userscript is optional; nothing in Bridge is removed.

## Quick start (dev)

```powershell
cd harem-booru-viewer
python -m venv .venv
.\.venv\Scripts\pip install -e .
.\.venv\Scripts\harem-booru-viewer
```

1. Start **Harem Link Bridge** (system tray).
2. Launch **harem-booru-viewer**.
3. Pick Danbooru or Rule34, search, open a post, use the bridge buttons.

Rule34 may need API credentials under **File → Manage Sites** (same as upstream).

## Updating from upstream

See **[FORK_GUIDE.md](FORK_GUIDE.md)** — give that file plus this directory to an agent with “fork the new version”.

## Full upstream documentation

See [README.md](README.md) for themes, keybinds, Hyprland, and the rest of stock booru-viewer.
