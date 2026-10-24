#!/usr/bin/env bash
set -euo pipefail

if (( $# != 3 )); then
    echo "Usage: $0 APPIMAGE VERSION x86_64|aarch64" >&2
    exit 2
fi

appimage="$(realpath "$1")"
version="$2"
architecture="$3"
[[ "$architecture" == x86_64 || "$architecture" == aarch64 ]] || { echo "Unsupported architecture: $architecture" >&2; exit 2; }
[[ "$(basename "$appimage")" == "leomoon-subfix-$version-linux-$architecture.AppImage" ]] || { echo "AppImage filename does not match release metadata" >&2; exit 1; }
[[ -x "$appimage" ]] || { echo "AppImage is not executable" >&2; exit 1; }

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
(
    cd "$work_dir"
    APPIMAGE_EXTRACT_AND_RUN=1 "$appimage" --appimage-extract >/dev/null
)
app_dir="$work_dir/squashfs-root"
required_paths=(
    "AppRun"
    "usr/bin/leomoon-subfix"
    "usr/lib/leomoon-subfix/LeoMoon SubFix"
    "usr/share/applications/com.leomoon.SubFix.desktop"
    "usr/share/icons/hicolor/256x256/apps/com.leomoon.SubFix.png"
    "usr/share/doc/leomoon-subfix/LICENSE"
    "usr/share/doc/leomoon-subfix/THIRD_PARTY_NOTICES.md"
)
for relative_path in "${required_paths[@]}"; do
    [[ -s "$app_dir/$relative_path" || -x "$app_dir/$relative_path" ]] || { echo "AppImage is missing required file: $relative_path" >&2; exit 1; }
done
grep -qx 'Exec=leomoon-subfix' "$app_dir/usr/share/applications/com.leomoon.SubFix.desktop"
grep -qx 'Icon=com.leomoon.SubFix' "$app_dir/usr/share/applications/com.leomoon.SubFix.desktop"
grep -qx 'Categories=Utility;' "$app_dir/usr/share/applications/com.leomoon.SubFix.desktop"

while IFS= read -r binary; do
    file "$binary" | grep -q "$( [[ "$architecture" == aarch64 ]] && echo 'ARM aarch64' || echo 'x86-64' )" || { echo "Unexpected architecture: $binary" >&2; exit 1; }
done < <(find "$app_dir/usr/lib/leomoon-subfix" -type f \( -name '*.so' -o -name '*.so.*' -o -name 'LeoMoon SubFix' \) -print)

echo "Verified self-contained AppImage $appimage"
