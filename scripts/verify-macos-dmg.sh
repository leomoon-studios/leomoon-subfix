#!/usr/bin/env bash
set -euo pipefail

[[ $# -eq 2 ]] || { echo "Usage: $0 DMG VERSION" >&2; exit 2; }
dmg="$1"
version="$2"
[[ -f "$dmg" ]] || { echo "DMG is missing: $dmg" >&2; exit 1; }
[[ "$(basename "$dmg")" == "leomoon-subfix-$version-macos-arm64.dmg" ]] || { echo "Unexpected DMG filename" >&2; exit 1; }
hdiutil imageinfo "$dmg" >/dev/null

mount_dir="$(mktemp -d)"
device=""
cleanup() {
    if [[ -n "$device" ]]; then hdiutil detach "$device" -quiet || true; fi
    rmdir "$mount_dir" 2>/dev/null || true
}
trap cleanup EXIT
device="$(hdiutil attach -nobrowse -readonly -mountpoint "$mount_dir" "$dmg" | awk '/^\/dev\// {print $1; exit}')"
[[ -d "$mount_dir/LeoMoon SubFix.app" ]] || { echo "DMG does not contain LeoMoon SubFix.app" >&2; exit 1; }
[[ -x "$mount_dir/LeoMoon SubFix.app/Contents/MacOS/LeoMoon SubFix" ]] || { echo "DMG application executable is missing" >&2; exit 1; }
[[ -f "$mount_dir/LICENSE.txt" && -f "$mount_dir/THIRD_PARTY_NOTICES.md" ]] || { echo "DMG notices are missing" >&2; exit 1; }
