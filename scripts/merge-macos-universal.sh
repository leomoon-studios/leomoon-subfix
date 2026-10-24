#!/usr/bin/env bash
set -euo pipefail
[[ $# -eq 3 ]] || { echo "Usage: $0 X86_APP ARM_APP OUTPUT_DIRECTORY" >&2; exit 2; }
x86_app="$1"; arm_app="$2"; output_dir="$3"
[[ -d "$x86_app" && -d "$arm_app" ]] || { echo "Both native application bundles are required" >&2; exit 1; }
rm -rf "$output_dir"; mkdir -p "$output_dir"; app="$output_dir/LeoMoon SubFix.app"; cp -a "$arm_app" "$app"
rm -rf "$app/Contents/_CodeSignature"
diff -u <(cd "$x86_app" && find . -path './Contents/_CodeSignature' -prune -o -print | sort) <(cd "$arm_app" && find . -path './Contents/_CodeSignature' -prune -o -print | sort)
while IFS= read -r -d '' arm_file; do
    relative="${arm_file#"$arm_app"/}"; x86_file="$x86_app/$relative"; output_file="$app/$relative"
    [[ "$relative" == Contents/_CodeSignature/* ]] && continue
    if file "$arm_file" | grep -q 'Mach-O'; then lipo -create "$x86_file" "$arm_file" -output "$output_file"; chmod +x "$output_file"; fi
done < <(find "$arm_app" -type f -print0)
architectures="$(lipo -archs "$app/Contents/MacOS/LeoMoon SubFix")"
[[ " $architectures " == *' x86_64 '* && " $architectures " == *' arm64 '* ]] || { echo "Merged application is not universal" >&2; exit 1; }
