# -*- mode: python ; coding: utf-8 -*-
# Harem fork — Windows onedir bundle (libmpv-2.dll + PySide6 + httpx).

import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hiddenimports = [
    *collect_submodules("booru_viewer"),
    "httpx",
    "httpx._transports",
    "httpx._transports.default",
    "h2",
    "hpack",
    "hyperframe",
    "PIL",
    "PIL.Image",
    "PIL.JpegImagePlugin",
    "PIL.PngImagePlugin",
    "PIL.GifImagePlugin",
    "PIL.WebPImagePlugin",
    "PIL.BmpImagePlugin",
    "mpv",
]

a = Analysis(
    ["booru_viewer/main_gui.py"],
    pathex=[],
    binaries=[("libmpv-2.dll", ".")] if sys.platform == "win32" else [],
    datas=[
        ("icon.png", "."),
        ("icon.ico", "."),
        ("themes", "themes"),
        ("licenses", "licenses"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["textual", "tkinter", "unittest", "pytest"],
    noarchive=True,
    optimize=2,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="harem-booru-viewer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon="icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="harem-booru-viewer",
)
