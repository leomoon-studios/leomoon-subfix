from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = PROJECT_ROOT / "packaging" / "windows" / "subfix.iss"
PACKAGE_SCRIPT = PROJECT_ROOT / "scripts" / "package-windows.ps1"
VERIFY_SCRIPT = PROJECT_ROOT / "scripts" / "verify-windows-package.ps1"


def test_windows_installer_uses_native_application_closing() -> None:
    installer = INSTALLER.read_text(encoding="utf-8")

    assert "CloseApplications=yes" in installer
    assert "SetupIconFile" not in installer
    assert "istask.dll" not in installer


def test_windows_packaging_rejects_legacy_runtime_dlls() -> None:
    verifier = VERIFY_SCRIPT.read_text(encoding="utf-8")
    package_script = PACKAGE_SCRIPT.read_text(encoding="utf-8")

    assert '"msvcp100.dll"' in verifier
    assert '"msvcr100.dll"' in verifier
    assert '"istask.dll"' in verifier
    assert "THIRD_PARTY_NOTICES.md" in package_script
    assert "release-manifest.json" in package_script
    assert "SHA256SUMS" in package_script
    assert '".exe", ".dll", ".pyd"' in verifier
