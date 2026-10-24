from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = PROJECT_ROOT / "scripts" / "build.py"
SPECIFICATION = PROJECT_ROOT / "packaging" / "pyinstaller" / "subfix.spec"


def test_built_application_uses_the_display_name_and_stable_artifact_slug() -> None:
    specification = SPECIFICATION.read_text(encoding="utf-8")
    build_script = BUILD_SCRIPT.read_text(encoding="utf-8")

    assert 'name="LeoMoon SubFix"' in specification
    assert 'name="leomoon-subfix"' in specification
    assert 'executable_name = "LeoMoon SubFix.exe"' in build_script


def test_build_rejects_an_unsafe_output_directory() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(BUILD_SCRIPT),
            "--version",
            "2.1.0",
            "--release-date",
            "2026-10-24T00:00:00Z",
            "--commit",
            "a" * 40,
            "--output-dir",
            ".",
            "--clean",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "dedicated directory below" in result.stderr


def test_build_rejects_a_non_release_version() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(BUILD_SCRIPT),
            "--version",
            "2.1",
            "--release-date",
            "2026-10-24T00:00:00Z",
            "--commit",
            "a" * 40,
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "MAJOR.MINOR.PATCH" in result.stderr
