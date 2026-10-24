# LeoMoon SubFix

## Introduction

LeoMoon SubFix converts legacy Windows-1256 subtitle files to UTF-8.

## Supported packages

- Windows: x64 and ARM64 Inno Setup installers.
- Linux: x86_64 and ARM64 AppImages.
- macOS: one universal DMG containing an x86_64 and ARM64 application.

## Development setup

Python 3.12 is required. Create the project environment with `uv` inside `.venv` only:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install "uv==0.13.5"
.venv/bin/uv sync --all-extras --locked
```

Launch the application with:

```bash
.venv/bin/python src/leomoon_subfix/app.py
```

Regenerate the Qt-derived modules after changing the UI. `resources_rc.py` is generated locally because Qt embeds source timestamps in it; `main_window.py` is tracked and must remain current:

```bash
.venv/bin/python scripts/generate_qt.py
git diff --exit-code -- src/leomoon_subfix/_generated/main_window.py
```

Run checks in a headless Linux environment with:

```bash
.venv/bin/python -m ruff check src tests scripts
QT_QPA_PLATFORM=offscreen QT_QPA_PLATFORMTHEME='' QT_STYLE_OVERRIDE=Fusion .venv/bin/python -m pytest -q -rs
```

## Release builds

GitHub Actions builds installers and packages from `release.yml`. Use its `workflow_dispatch` form for a non-publishing platform test. Pushing a `vMAJOR.MINOR.PATCH` tag builds every platform and publishes the release after all packages pass.

Windows packages are Inno Setup `.exe` installers, Linux packages are `.AppImage` files, and macOS packages are universal `.dmg` files. The app executable is named `LeoMoon SubFix`; release assets use the stable `leomoon-subfix` slug.

Developer ID signing and notarization are optional. Configure the macOS GitHub secrets only for protected release runs. Certificates, signing keys, Apple passwords, and GitHub tokens must never be committed to the repository.
