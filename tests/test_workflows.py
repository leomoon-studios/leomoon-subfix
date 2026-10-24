from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = PROJECT_ROOT / ".github" / "workflows"


def test_release_dispatches_to_dedicated_platform_workflows() -> None:
    release = (WORKFLOWS / "release.yml").read_text(encoding="utf-8")

    assert "./.github/workflows/linux.yml" in release
    assert "./.github/workflows/windows.yml" in release
    assert "./.github/workflows/macos.yml" in release
    assert "Publish GitHub release" in release
    assert "Generate release notes with commit list" in release
    assert "collect-release-assets.sh" in release


def test_release_asset_collector_requires_each_platform_asset() -> None:
    collector = (PROJECT_ROOT / "scripts" / "collect-release-assets.sh").read_text(encoding="utf-8")

    assert '"leomoon-subfix-$version-linux-x86_64.AppImage"' in collector
    assert '"leomoon-subfix-$version-linux-aarch64.AppImage"' in collector
    assert '"leomoon-subfix-$version-windows-x64-setup.exe"' in collector
    assert '"leomoon-subfix-$version-windows-arm64-setup.exe"' in collector
    assert '"leomoon-subfix-$version-macos-universal.dmg"' in collector
    assert "Expected exactly one release asset" in collector


def test_linux_publishes_appimages_not_raw_bundles() -> None:
    linux = (WORKFLOWS / "linux.yml").read_text(encoding="utf-8")

    assert "Upload Linux release artifact" in linux
    assert "Retain raw bundle diagnostics on failure" in linux
    assert "if: failure()" in linux
    assert "path: dist/" in linux


def test_macos_workflow_packages_a_dmg() -> None:
    macos = (WORKFLOWS / "macos.yml").read_text(encoding="utf-8")
    package_script = (PROJECT_ROOT / "scripts" / "package-macos.sh").read_text(encoding="utf-8")

    assert "package-macos.sh" in macos
    assert "hdiutil create" in package_script
    assert '"$architecture" == universal' in package_script
    assert "macos-$architecture.dmg" in package_script
    assert "merge-macos-universal.sh" in macos
