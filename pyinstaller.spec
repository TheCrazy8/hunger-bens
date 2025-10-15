# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

project_name = 'HungerBens'
base_dir = os.path.abspath(os.path.dirname(__file__))
main_script = os.path.join(base_dir, 'docs', 'main.py')

hiddenimports = collect_submodules('sv_ttk')

a = Analysis(
    [main_script],
    pathex=[base_dir],
    binaries=[],
    datas=[
        (os.path.join(base_dir, 'docs', 'favicon.svg'), 'docs'),
        (os.path.join(base_dir, 'docs', 'index.html'), 'docs'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=project_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=project_name,
)
