# main.spec

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis

block_cipher = None

a = Analysis(
    ['main.py'],              # your entry point script
    pathex=['.'],
    binaries=[],
    # datas=[
    #     ('assets', 'assets'), # add/remove folders here (mirror xcopy lines in workflow)
    #     ('data',   'data'),   # add/remove folders here (mirror xcopy lines in workflow)
    # ],
    hiddenimports=[],         # add imports PyInstaller misses at runtime
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',              # must match OUTPUT_NAME in workflow
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,            # False for GUI, True for CLI
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/icon.ico',   # path to your .ico, or remove this line
)