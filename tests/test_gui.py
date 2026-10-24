from __future__ import annotations

import os
from pathlib import Path

import pytest


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QPA_PLATFORMTHEME", "")
os.environ.setdefault("QT_STYLE_OVERRIDE", "Fusion")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")
from PySide6 import QtCore, QtGui


@pytest.fixture(scope="session")
def qapp():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    app.setStyle("Fusion")
    return app


def test_main_window_displays_version_and_converts_file(qapp, monkeypatch, tmp_path: Path) -> None:
    import main

    monkeypatch.setattr(main, "isDark", lambda: False)
    source = tmp_path / "window.srt"
    source.write_bytes("ي ك\n".encode("windows-1256"))
    window = main.mainUi()
    window.ui.fixCbox.setChecked(True)

    window._convert(str(source))

    assert window.ui.verLbl.text() == "v1.0.0"
    assert (tmp_path / "window_fixed.srt").read_text(encoding="utf-8") == "ی ک\n"
    assert "All done" in window.ui.statusLbl.text()
    assert not window.windowIcon().isNull()
    assert QtGui.QFontDatabase.addApplicationFont(":/res/fonts/Vazir.ttf") >= 0
    window.close()


def test_main_window_applies_dark_theme(qapp, monkeypatch) -> None:
    import main

    monkeypatch.setattr(main, "isDark", lambda: True)
    window = main.mainUi()

    assert QtGui.QGuiApplication.palette().color(QtGui.QPalette.ColorRole.Window) == QtGui.QColor(55, 53, 53)
    window.close()


def test_drop_event_converts_a_subtitle(qapp, monkeypatch, tmp_path: Path) -> None:
    import main

    monkeypatch.setattr(main, "isDark", lambda: False)
    source = tmp_path / "dropped.srt"
    source.write_bytes("ي ك\n".encode("windows-1256"))
    mime_data = QtCore.QMimeData()
    mime_data.setUrls([QtCore.QUrl.fromLocalFile(str(source))])
    event = QtGui.QDropEvent(
        QtCore.QPointF(1, 1),
        QtCore.Qt.DropAction.CopyAction,
        mime_data,
        QtCore.Qt.MouseButton.LeftButton,
        QtCore.Qt.KeyboardModifier.NoModifier,
    )
    window = main.mainUi()
    window.ui.fixCbox.setChecked(True)

    window.dropEvent(event)

    assert event.isAccepted()
    assert (tmp_path / "dropped_fixed.srt").read_text(encoding="utf-8") == "ی ک\n"
    window.close()
