# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for GhostMEAN.

Usage: pyinstaller ghostmean.spec
Produces a onedir bundle in dist/ghostmean/ (used by scripts/build_appimage.sh
to assemble the AppDir). Not meant to be run directly by end users.
"""

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['ghostmean/__main__.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files('ghostmean', includes=['assets/*.png']),
    hiddenimports=[
        # i18n language packs are imported explicitly in ghostmean/i18n/__init__.py
        # (from ghostmean.i18n import pl, en, ru, es, de, fr), so PyInstaller's
        # static import analysis already picks them up -- no hidden-imports
        # needed for them. Listed here anyway as a safety net in case that
        # import style ever changes to something PyInstaller can't trace.
        'ghostmean.i18n.pl', 'ghostmean.i18n.en', 'ghostmean.i18n.ru',
        'ghostmean.i18n.es', 'ghostmean.i18n.de', 'ghostmean.i18n.fr',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ghostmean',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='ghostmean',
)
