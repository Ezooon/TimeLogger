# -*- mode: python ; coding: utf-8 -*-
import os

from kivy_deps import sdl2, glew

from kivymd import hooks_path as kivymd_hooks_path
from PyInstaller.utils.hooks import collect_submodules

path = os.path.abspath(".")
modules = collect_submodules("database") + collect_submodules("screens") + collect_submodules("uix") + collect_submodules("plyer.platforms.win.filechooser")

print("shit "*100, collect_submodules("uix"))
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database/logs.db', 'database'),
        ('assets', 'assets'),
        ('screens/*.kv', 'screens'),
        ('uix/*.kv', 'uix'),
        ('*.kv', '.'),
        ('continuous_logging/Continuous Logging.exe', 'continuous_logging'),
        ('continuous_logging/logo.png', 'continuous_logging'),

        ('aitool/keys.json', 'aitool'),
        ('socialapi/keys.data', 'socialapi')
    ],
    hiddenimports=modules + [

    'screens.__init__',
    'screens.aitool',
    'screens.entries',
    'screens.post',
    'screens.preferences',

    'uix.__init__',
    'uix.attachmentcard',
    'uix.entrycard',
    'uix.messagecard',
    'uix.postcard',
    'uix.settings',
    'uix.tagchip',

    'aitool.__init__',
    'aitool.chat',
    'aitool.post_generator.py',

    'socialapi.__init__',
    'socialapi.facebook',
    'socialapi.linkedin',
    'socialapi.twitter',
    ],
    hookspath=[kivymd_hooks_path],
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
    name='Time Logger',
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
    icon=['assets\\logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Time Logger',
)
