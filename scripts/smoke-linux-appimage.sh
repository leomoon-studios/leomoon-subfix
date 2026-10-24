#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
    echo "Usage: $0 APPIMAGE" >&2
    exit 2
fi

appimage="$(realpath "$1")"
[[ -x "$appimage" ]] || { echo "AppImage is not executable: $appimage" >&2; exit 1; }
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
input="$work_dir/legacy-windows-1256.srt"
printf '\355 \337\n' > "$input"
env -i HOME="$work_dir/home" PATH=/usr/bin:/bin TMPDIR="$work_dir" APPIMAGE_EXTRACT_AND_RUN=1 \
    "$appimage" --convert "$input"
[[ -f "$work_dir/legacy-windows-1256_fixed.srt" ]] || { echo "AppImage did not convert the fixture" >&2; exit 1; }

echo "Linux AppImage launch and conversion check passed"
