# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_all

hidden_rich = collect_submodules("rich")

datas_cn, binaries_cn, hiddenimports_cn = collect_all("charset_normalizer")
datas_pow, binaries_pow, hiddenimports_pow = collect_all("python_on_whales")
datas_git, binaries_git, hiddenimports_git = collect_all("git")

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=binaries_cn + binaries_pow + binaries_git,
    datas=datas_cn + datas_pow + datas_git + [('app/commands/docs/content', 'app/commands/docs/content')],
    hiddenimports=[
        "charset_normalizer",
        "python_on_whales",
        "git",
        "rich",
        "typer"
    ] + hidden_rich + hiddenimports_cn + hiddenimports_pow + hiddenimports_git,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["chardet"],   # IMPORTANT
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="mate",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)