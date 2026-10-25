# Changelog

## 2.1.0 (2026-10-24)

- Native release packages for Windows x64 and ARM64, Linux x86_64 and ARM64 AppImages, and a macOS ARM64 DMG.
- GitHub Actions platform builds, installer and package smoke tests, checksums, and tag-driven GitHub releases with linked commit and contributor credits.
- Regression tests for subtitle conversion and PySide6 GUI behavior.
- Optional protected Windows signing and macOS signing and notarization support.
- Migrated the application from PyQt5 to PySide6 and Qt 6.
- Moved the application to a standard `src/` package layout with generated Qt sources and modern project metadata.
- Locked maintained Python dependencies in `uv.lock` and updated DarkDetect, PyInstaller, and development tooling.
- Replaced legacy build scripts and compatibility DLLs with deterministic PyInstaller packaging and native platform installers.
- Updated supported systems to current Windows, Linux, and macOS releases.
- Improved Windows installer cleanup checks and architecture validation.
- Improved Linux AppImage packaging and macOS ARM64 bundle handling.

## 2.0.6 (2021-10-05)

- Added cross-platform auto dark mode
- Added Ctrl + M hotkey to toggle dark mode
- Updated all dependencies

## 2.0.5 (2020-12-19)

- Fixed compatibility issue with macOS Big Sur
- Minimum supported macOS has changed to 10.14 Mojave
- Fixed uninstall icon for Windows setup
- Updated all dependencies

## 2.0.4 (2020-05-20)

- Fixed crash on Windows 10 update 1909
- Updated all dependencies

## 2.0.3

- Updated core to the latest version
- Updated all dependencies
- Embedded main font into the application
- Fixed DPI scaling not working sometimes
- Minimum supported macOS has changed to 10.13

## 2.0.2

- Minor changes
- Windows binary is now digitally signed

## 2.0.1

- Minor improvements

## 2.0.0

- SubFix was re-written from scratch to support Linux and macOS

## 1.22

- Minor changes

## 1.0

- Initial release
