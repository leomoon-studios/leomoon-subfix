#!/usr/bin/env python3
"""Create release metadata from one validated annotated semantic-version tag."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


TAG_PATTERN = re.compile(r"^v(?P<version>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$")
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def git(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        check=True,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def parse_tag(tag: str) -> tuple[str, tuple[int, int, int]]:
    match = TAG_PATTERN.fullmatch(tag)
    if match is None:
        raise ValueError("Release tags must match vMAJOR.MINOR.PATCH, for example v2.1.0.")
    version = tag.removeprefix("v")
    return version, tuple(int(match.group(name)) for name in ("version", "minor", "patch"))


def annotated_tag_date(tag: str) -> str:
    tag_type = git("cat-file", "-t", tag)
    if tag_type != "tag":
        raise ValueError(f"{tag} must be an annotated tag, not a lightweight tag.")
    tag_date = git("for-each-ref", f"refs/tags/{tag}", "--format=%(taggerdate:iso-strict)")
    if not tag_date:
        raise ValueError(f"{tag} does not have an annotated tag date.")
    return normalize_date(tag_date)


def normalize_date(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def metadata_for(
    tag: str,
    *,
    release_date: str,
    commit_sha: str,
) -> dict[str, object]:
    version, version_parts = parse_tag(tag)
    windows_version = ".".join(str(part) for part in (*version_parts, 0))
    return {
        "tag": tag,
        "version": version,
        "release_date": normalize_date(release_date),
        "commit_sha": commit_sha,
        "windows_file_version": windows_version,
        "windows_setup_filename": f"leomoon-subfix-{version}-windows-x64-setup.exe",
        "linux_appimage_filename": f"leomoon-subfix-{version}-linux-x86_64.AppImage",
        "macos_dmg_filename": f"leomoon-subfix-{version}-macos-universal2.dmg",
        "release_manifest_filename": f"leomoon-subfix-{version}-manifest.json",
    }


def windows_version_file(metadata: dict[str, object]) -> str:
    version = str(metadata["windows_file_version"])
    file_version = ", ".join(version.split("."))
    return f'''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({file_version}),
    prodvers=({file_version}),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904b0',
        [
          StringStruct(u'CompanyName', u'LeoMoon Studios'),
          StringStruct(u'ProductName', u'LeoMoon SubFix'),
          StringStruct(u'ProductVersion', u'{version}'),
          StringStruct(u'FileVersion', u'{version}'),
          StringStruct(u'InternalName', u'leomoon-subfix'),
          StringStruct(u'OriginalFilename', u'leomoon-subfix.exe'),
          StringStruct(u'FileDescription', u'LeoMoon SubFix'),
          StringStruct(u'LegalCopyright', u'Copyright 2018 LeoMoon Studios'),
        ]
      )
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="Release tag. Defaults to GITHUB_REF_NAME or the exact HEAD tag.")
    parser.add_argument("--release-date", help="UTC or offset-aware ISO 8601 release date.")
    parser.add_argument("--commit-sha", help="Commit SHA. Defaults to the release tag commit.")
    parser.add_argument("--output", type=Path, help="Write JSON metadata to this file instead of stdout.")
    parser.add_argument("--windows-version-file", type=Path, help="Write PyInstaller Windows version metadata.")
    parser.add_argument(
        "--allow-unverified-tag",
        action="store_true",
        help="Allow --tag without checking that it is an annotated Git tag. Intended for local template tests only.",
    )
    return parser.parse_args()


def main() -> int:
    args = arguments()
    tag = args.tag or os.environ.get("GITHUB_REF_NAME")
    if tag is None:
        tag = git("describe", "--exact-match", "--tags", "HEAD")

    try:
        parse_tag(tag)
        if args.allow_unverified_tag:
            if not args.release_date or not args.commit_sha:
                raise ValueError("Unverified tag mode requires --release-date and --commit-sha.")
            release_date = args.release_date
            commit_sha = args.commit_sha
        else:
            release_date = args.release_date or annotated_tag_date(tag)
            commit_sha = args.commit_sha or git("rev-parse", f"{tag}^{{commit}}")
        metadata = metadata_for(tag, release_date=release_date, commit_sha=commit_sha)
    except (subprocess.CalledProcessError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    rendered = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.windows_version_file:
        args.windows_version_file.write_text(windows_version_file(metadata), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
