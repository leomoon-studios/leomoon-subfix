#!/usr/bin/env bash
set -euo pipefail
[[ $# -eq 3 ]] || { echo "Usage: $0 X86_APP ARM_APP OUTPUT_DIRECTORY" >&2; exit 2; }
x86_app="$1"; arm_app="$2"; output_dir="$3"
[[ -d "$x86_app" && -d "$arm_app" ]] || { echo "Both native application bundles are required" >&2; exit 1; }
rm -rf "$output_dir"; mkdir -p "$output_dir"; app="$output_dir/LeoMoon SubFix.app"; cp -a "$arm_app" "$app"
diff -u <(cd "$x86_app" && find . -print | sort) <(cd "$arm_app" && find . -print | sort)
while IFS= read -r -d '' arm_file; do
    relative="${arm_file#"$arm_app"/}"; x86_file="$x86_app/$relative"; output_file="$app/$relative"
    if file "$arm_file" | grep -q 'Mach-O'; then lipo -create "$x86_file" "$arm_file" -output "$output_file"; else cmp -s "$x86_file" "$arm_file" || { echo "Non-native file differs between bundles: $relative" >&2; exit 1; }; fi
done < <(find "$arm_app" -type f -print0)
architectures="$(lipo -archs "$app/Contents/MacOS/LeoMoon SubFix")"
[[ " $architectures " == *' x86_64 '* && " $architectures " == *' arm64 '* ]] || { echo "Merged application is not universal" >&2; exit 1; }
