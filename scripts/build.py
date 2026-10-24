#!/usr/bin/env python3
"""Build a versioned, one-directory LeoMoon SubFix application with PyInstaller."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


VERSION_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILD_ROOT = PROJECT_ROOT / "build"
SPECIFICATION = PROJECT_ROOT / "packaging" / "pyinstaller" / "subfix.spec"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Release version in MAJOR.MINOR.PATCH form.")
    parser.add_argument("--release-date", required=True, help="UTC ISO 8601 release date.")
    parser.add_argument("--commit", required=True, help="Source commit SHA.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=BUILD_ROOT / "pyinstaller",
        help="Dedicated build directory under build/.",
    )
    parser.add_argument("--clean", action="store_true", help="Replace the dedicated output directory.")
    return parser.parse_args()


def resolved_output_directory(value: Path) -> Path:
    output_directory = value.resolve()
    build_root = BUILD_ROOT.resolve()
    if output_directory == build_root or build_root not in output_directory.parents:
        raise ValueError(f"--output-dir must be a dedicated directory below {build_root}.")
    return output_directory


def validate_arguments(args: argparse.Namespace) -> Path:
    if VERSION_PATTERN.fullmatch(args.version) is None:
        raise ValueError("--version must use MAJOR.MINOR.PATCH form.")
    parsed_date = datetime.fromisoformat(args.release_date.replace("Z", "+00:00"))
    if parsed_date.tzinfo is None:
        raise ValueError("--release-date must include a UTC or numeric offset.")
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", args.commit):
        raise ValueError("--commit must be a hexadecimal Git commit SHA.")
    return resolved_output_directory(args.output_dir)


def write_runtime_hook(path: Path, version: str) -> None:
    path.write_text(
        "import os\n"
        f"os.environ.setdefault('LEOMOON_SUBFIX_VERSION', {version!r})\n",
        encoding="utf-8",
    )


def installed_versions() -> tuple[str, str, str]:
    from PySide6 import QtCore, __version__ as pyside6_version
    from PyInstaller import __version__ as pyinstaller_version

    return pyside6_version, QtCore.qVersion(), pyinstaller_version


def build(args: argparse.Namespace, output_directory: Path) -> Path:
    if output_directory.exists():
        if not args.clean:
            raise FileExistsError(f"{output_directory} exists. Pass --clean to replace it.")
        shutil.rmtree(output_directory)
    output_directory.mkdir(parents=True)
    work_directory = output_directory / ".work"
    runtime_hook = work_directory / "set_build_version.py"
    work_directory.mkdir()
    write_runtime_hook(runtime_hook, args.version)

    environment = os.environ.copy()
    environment["LEOMOON_SUBFIX_VERSION"] = args.version
    environment["LEOMOON_SUBFIX_RUNTIME_HOOK"] = str(runtime_hook)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--distpath",
            str(output_directory),
            "--workpath",
            str(work_directory / "pyinstaller"),
            str(SPECIFICATION),
        ],
        check=True,
        cwd=PROJECT_ROOT,
        env=environment,
    )
    application_directory = output_directory / "leomoon-subfix"
    executable_name = "LeoMoon SubFix.exe" if sys.platform == "win32" else "LeoMoon SubFix"
    if not (application_directory / executable_name).is_file():
        raise FileNotFoundError("PyInstaller did not produce the expected application executable.")
    return application_directory


def write_manifest(args: argparse.Namespace, output_directory: Path, application_directory: Path) -> Path:
    pyside6_version, qt_version, pyinstaller_version = installed_versions()
    manifest = {
        "application": "LeoMoon SubFix",
        "version": args.version,
        "release_date": args.release_date,
        "commit": args.commit,
        "platform": sys.platform,
        "architecture": platform.machine(),
        "artifact_format": "pyinstaller-onedir",
        "application_directory": application_directory.name,
        "python_version": platform.python_version(),
        "pyside6_version": pyside6_version,
        "qt_version": qt_version,
        "pyinstaller_version": pyinstaller_version,
    }
    manifest_path = output_directory / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def main() -> int:
    try:
        args = arguments()
        output_directory = validate_arguments(args)
        application_directory = build(args, output_directory)
        manifest_path = write_manifest(args, output_directory, application_directory)
    except (FileExistsError, FileNotFoundError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
