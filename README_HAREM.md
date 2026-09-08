# Harem booru-viewer

Desktop booru browser (Danbooru + Rule34) with one-click actions into Harem Link Bridge. Fork of [pxlwh/booru-viewer](https://github.com/pxlwh/booru-viewer).

## Harem changes

- **Default sites** — Danbooru and Rule34 are pre-added; no manual setup.
- **Bridge buttons** — preview and popout viewers get `checkres`, `conjure`, `both`, `craft` (same as the browser userscript). Needs Harem Link Bridge running.
- **Quick Tags** (Danbooru) — right-click a post, apply a preset tag combo through the Danbooru API (add-only, never removes). Combos live under File > Settings > Quick Tags; needs a Danbooru API user + key under File > Manage Sites.
- **Tag Bookmarks** — bookmark any tag from the info panel; saved tags get a tab with per-tag random previews.
- **High-resolution thumbnails** — on by default (File > Settings); pulls samples/originals instead of ~150px previews.
- **Extra keybinds** — arrows flip pages, Shift+arrows seek images. See `KEYBINDS.md`.
- **Separate data dir** — `%APPDATA%\harem-booru-viewer\` (Windows) or `~/.local/share/harem-booru-viewer/` (Linux); stock booru-viewer data is untouched.

## Quick start

```powershell
cd harem-booru-viewer
python -m venv .venv
.\.venv\Scripts\pip install -e .
.\.venv\Scripts\harem-booru-viewer
```

Requires **mpv** on PATH (same as upstream). Start Harem Link Bridge first if you want the bridge buttons.

## Docs

- [Upstream README](https://github.com/pxlwh/booru-viewer#readme) — full stock documentation (themes, Hyprland).
- [FORK_GUIDE.md](FORK_GUIDE.md) — maintainer notes for rebasing onto new upstream releases.
- [KEYBINDS.md](KEYBINDS.md) — key bindings.
