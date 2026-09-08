# Harem booru-viewer

Desktop Danbooru/Rule34 browser with one-click actions into Harem Link Bridge. Fork of [pxlwh/booru-viewer](https://github.com/pxlwh/booru-viewer) — upstream behavior is otherwise unchanged.

> 100% vibecoded — written entirely with AI assistance, no hand-written code.

## How it differs from upstream

- **Sites ready to go** — Danbooru and Rule34 pre-added; no manual setup.
- **Bridge buttons** — preview and popout viewers get `checkres`, `conjure`, `both`, `craft`, posting to Harem Link Bridge. Same contract as the browser userscript, which keeps working untouched.
- **Quick Tags** (Danbooru) — apply preset tag combos through the Danbooru API (add-only, never removes). Needs an API user + key under File > Manage Sites.
- **Slow Tag + eyedropper** — free-text tagging dialog with live autocomplete (Space), middle-click tagging, number keys 1–5 for combos, pixel color picker (for when you can't decide what color of the background it is, useful for tagging images), transparency badges - makes it easy to understand if the image uses transparency layers at a glance (so that you don't tag an image with transparent_background as a white_background one by mistake).
- **Tag Bookmarks** — bookmark tags from the info panel; per-tag random previews.
- **High-resolution thumbnails** — on by default; samples/originals instead of ~150px previews.
- **Keybinds** — arrow/hjkl navigation, RU layout supported (Ы=S, …). See [KEYBINDS.md](KEYBINDS.md).
- **Per-site page sizes** — Danbooru 100, Rule34 50, each adjustable per site under File > Manage Sites.
- **Screenspace first** — one merged bottom bar (page nav + status + progress), tags-first info panel with post meta below the fold, no duplicate info lines, panels that never jump around.
- **Separate data dir** — `%APPDATA%\harem-booru-viewer\` (Windows) or `~/.local/share/harem-booru-viewer/` (Linux); stock booru-viewer data is untouched.

## Harem Bot integration

Pairs with [@slaviquegamebot](https://t.me/slaviquegamebot) through [Harem Link Bridge](https://github.com/SlaviqueBots/harem-link-bridge): right-click any post for a max-res diagnostic (`checkres`), the cheapest summon path (`conjure`), or both — results land back in the bot. Fully optional: File > Settings > Harem tab switches the Bridge actions off and the viewer works standalone.

## Install

Download `harem-booru-viewer-setup.exe` (or the portable zip) from [Releases](https://github.com/SlaviqueBots/harem-booru-viewer/releases) and run it. To update, install over the old copy — sites, keys and library are preserved. Needs Harem Link Bridge running only for the bridge buttons.

## From source

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -e .
.\.venv\Scripts\harem-booru-viewer
```

Requires **mpv** on PATH. Maintainer rebase notes: [FORK_GUIDE.md](FORK_GUIDE.md); harem feature details: [README_HAREM.md](README_HAREM.md).

## License

MIT — see [LICENSE](LICENSE), same as upstream.
