# Contributing to LeoMoon SubFix

Use Python 3.12 and create dependencies only inside `.venv`: `python3.12 -m venv .venv`, `.venv/bin/python -m pip install "uv==0.13.5"`, then `.venv/bin/uv sync --all-extras --locked`.

Before opening a change, regenerate Qt code when UI files change, run Ruff, and run the headless test suite described in the README. Keep generated UI output in sync when it is tracked.

Use `release.yml` through GitHub Actions for platform packages. Manual runs do not publish releases. A `vMAJOR.MINOR.PATCH` tag is the only release trigger and publishes Windows x64 and ARM64 installers, Linux x86_64 and ARM64 AppImages, and the macOS ARM64 DMG after all checks pass.

Do not commit certificates, private keys, provisioning profiles, Apple passwords, tokens, package outputs, virtual environments, or local signing keychains. Signing secrets belong only in protected GitHub repository secrets.
