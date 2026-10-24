#!/usr/bin/env bash
set -euo pipefail

[[ $# -eq 3 ]] || { echo "Usage: $0 ARTIFACT_DIRECTORY VERSION arm64" >&2; exit 2; }
artifact_dir="$(cd "$1" && pwd)"
version="$2"
architecture="$3"
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dmg="$artifact_dir/leomoon-subfix-$version-macos-$architecture.dmg"

(cd "$artifact_dir" && shasum -a 256 -c SHA256SUMS)
mount_dir="$(mktemp -d)"
copy_dir="$(mktemp -d)"
device=""
cleanup() { [[ -n "$device" ]] && hdiutil detach "$device" -quiet || true; rm -rf "$mount_dir" "$copy_dir"; }
trap cleanup EXIT
device="$(hdiutil attach -nobrowse -readonly -mountpoint "$mount_dir" "$dmg" | awk '/^\/dev\// {print $1; exit}')"
app="$mount_dir/LeoMoon SubFix.app"
bash "$repo_dir/scripts/verify-macos-package.sh" "$app" "$dmg" "$version" "$architecture"
cp -a "$app" "$copy_dir/"
fixture="$copy_dir/legacy-windows-1256.srt"
cp "$repo_dir/tests/fixtures/legacy-windows-1256.srt" "$fixture"
"$copy_dir/LeoMoon SubFix.app/Contents/MacOS/LeoMoon SubFix" --convert "$fixture"
[[ -f "$copy_dir/legacy-windows-1256_fixed.srt" ]] || { echo "Packaged macOS app did not convert the fixture" >&2; exit 1; }
if grep -q '"signed": true' "$artifact_dir/release-manifest.json"; then spctl --assess --type execute "$copy_dir/LeoMoon SubFix.app"; fi
