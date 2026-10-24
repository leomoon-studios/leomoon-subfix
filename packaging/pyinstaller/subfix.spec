# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for the LeoMoon SubFix one-directory application."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, copy_metadata


PROJECT_ROOT = Path(SPECPATH).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SOURCE_ROOT / "leomoon_subfix"

DATA_FILES = collect_data_files(
    "leomoon_subfix",
    includes=["assets/**", "ui/*.qrc", "ui/*.ui"],
)
DATA_FILES.extend(copy_metadata("darkdetect"))
DATA_FILES.extend(copy_metadata("PySide6"))

# PyInstaller's Qt hooks collect the Qt libraries used by QtCore, QtGui, and
# QtWidgets. These modules are not used by SubFix and are intentionally omitted.
EXCLUDED_MODULES = [
    "PySide6.Qt3DAnimation",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DExtras",
    "PySide6.Qt3DInput",
    "PySide6.Qt3DLogic",
    "PySide6.Qt3DRender",
    "PySide6.QtCharts",
    "PySide6.QtDataVisualization",
    "PySide6.QtMultimedia",
    "PySide6.QtNetworkAuth",
    "PySide6.QtPdf",
    "PySide6.QtPdfWidgets",
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.QtQuick3D",
    "PySide6.QtQuickWidgets",
    "PySide6.QtWebChannel",
    "PySide6.QtWebEngine",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineQuick",
    "PySide6.QtWebEngineWidgets",
]

if sys.platform == "win32":
    APPLICATION_ICON = PACKAGE_ROOT / "assets" / "icons" / "main.ico"
elif sys.platform == "darwin":
    APPLICATION_ICON = PACKAGE_ROOT / "assets" / "icons" / "main.icns"
else:
    APPLICATION_ICON = None

RUNTIME_HOOKS = []
if runtime_hook := os.environ.get("LEOMOON_SUBFIX_RUNTIME_HOOK"):
    RUNTIME_HOOKS.append(runtime_hook)

a = Analysis(
    [str(PROJECT_ROOT / "packaging" / "pyinstaller" / "entry.py")],
    pathex=[str(SOURCE_ROOT)],
    binaries=[],
    datas=DATA_FILES,
    hiddenimports=[
        "leomoon_subfix._generated.main_window",
        "leomoon_subfix._generated.resources_rc",
        "darkdetect._dummy",
        "darkdetect._linux_detect",
        "darkdetect._mac_detect",
        "darkdetect._windows_detect",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=RUNTIME_HOOKS,
    excludes=EXCLUDED_MODULES,
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="leomoon-subfix",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(APPLICATION_ICON) if APPLICATION_ICON else None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="leomoon-subfix",
)
