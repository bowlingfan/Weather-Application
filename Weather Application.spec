# -*- mode: python ; coding: utf-8 -*-
# guide: pyinstaller --noconsole --icon=resource/big_sun_icon.ico --add-data="resource;resource" --add-data="src/data_read/sql;data_read/sql" --name "Weather Application" src/main.py

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('resource', 'resource'), ('src/data_read/sql', 'data_read/sql')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Weather Application',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resource\\big_sun_icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Weather Application',
)
