#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
stage_dir=""
dist_dir=""
version=""
release_date=""
commit=""

usage() {
    echo "Usage: $0 --stage-dir DIR --dist-dir DIR --version VERSION --release-date DATE --commit SHA" >&2
}

while (( $# )); do
    case "$1" in
        --stage-dir) stage_dir="$2"; shift 2 ;;
        --dist-dir) dist_dir="$2"; shift 2 ;;
        --version) version="$2"; shift 2 ;;
        --release-date) release_date="$2"; shift 2 ;;
        --commit) commit="$2"; shift 2 ;;
        *) usage; exit 2 ;;
    esac
done

[[ -n "$stage_dir" && -n "$dist_dir" && -n "$version" && -n "$release_date" && -n "$commit" ]] || { usage; exit 2; }
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Version must be MAJOR.MINOR.PATCH" >&2; exit 2; }
[[ "$release_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T ]] || { echo "Release date must be ISO 8601" >&2; exit 2; }
[[ "$commit" =~ ^[0-9a-fA-F]{7,64}$ ]] || { echo "Commit must be a Git SHA" >&2; exit 2; }

stage_dir="$(realpath "$stage_dir")"
dist_parent="$(cd "$(dirname "$dist_dir")" && pwd -P)"
dist_dir="$dist_parent/$(basename "$dist_dir")"
app="$stage_dir/LeoMoon SubFix.app"
[[ -d "$app" ]] || { echo "Stage directory must contain LeoMoon SubFix.app" >&2; exit 1; }
[[ -x "$app/Contents/MacOS/LeoMoon SubFix" ]] || { echo "Application bundle is missing its executable" >&2; exit 1; }
[[ "$dist_dir" != / && "$dist_dir" != "$repo_dir" ]] || { echo "Refusing to replace unsafe artifact directory: $dist_dir" >&2; exit 1; }

package_dir="$repo_dir/build/package/macos"
dmg_root="$package_dir/dmg-root"
rm -rf "$package_dir" "$dist_dir"
mkdir -p "$dmg_root" "$dist_dir"
cp -a "$app" "$dmg_root/"
install -m 0644 "$repo_dir/LICENSE" "$dmg_root/LICENSE.txt"
install -m 0644 "$repo_dir/THIRD_PARTY_NOTICES.md" "$dmg_root/THIRD_PARTY_NOTICES.md"

dmg="$dist_dir/leomoon-subfix-$version-macos-arm64.dmg"
# Use the normal Finder layout and icon. No custom installer artwork is required.
hdiutil create -quiet -volname "LeoMoon SubFix" -srcfolder "$dmg_root" -ov -format UDZO "$dmg"
bash "$repo_dir/scripts/verify-macos-dmg.sh" "$dmg" "$version"

cat > "$dist_dir/release-manifest.json" <<EOF
{
  "application": "LeoMoon SubFix",
  "version": "$version",
  "release_date": "$release_date",
  "commit": "$commit",
  "platform": "macos",
  "architectures": "arm64",
  "artifact_format": "DMG"
}
EOF
(
    cd "$dist_dir"
    shasum -a 256 ./* > SHA256SUMS
)
echo "macOS release artifacts are ready in $dist_dir"
