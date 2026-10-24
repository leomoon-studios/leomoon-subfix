from __future__ import annotations

from pathlib import Path

import pytest

from leomoon_subfix.converter import convert_subtitle, convert_subtitles, fixed_output_path


FIXTURES_DIRECTORY = Path(__file__).parent / "fixtures"


def test_fixed_output_path_preserves_directory_and_suffix(tmp_path: Path) -> None:
    source = tmp_path / "episode.one.srt"

    assert fixed_output_path(source) == tmp_path / "episode.one_fixed.srt"
    assert fixed_output_path(tmp_path / "subtitle") == tmp_path / "subtitle_fixed"


def test_converts_tracked_windows_1256_fixture(tmp_path: Path) -> None:
    source = tmp_path / "legacy.srt"
    source.write_bytes((FIXTURES_DIRECTORY / "legacy-windows-1256.srt").read_bytes())

    output = convert_subtitle(source)

    text = output.read_text(encoding="utf-8")
    assert output == tmp_path / "legacy_fixed.srt"
    assert text.startswith("1\n00:00:06,000 --> 00:00:12,074\n")
    assert "به تمام پارسي زبانان جهان" in text


def test_normalizes_persian_characters_when_requested(tmp_path: Path) -> None:
    source = tmp_path / "characters.srt"
    source.write_bytes("ي ك\n".encode("windows-1256"))

    unchanged = convert_subtitle(source)
    normalized = convert_subtitle(source, normalize_persian=True, destination=tmp_path / "normalized.srt")

    assert unchanged.read_text(encoding="utf-8") == "ي ك\n"
    assert normalized.read_text(encoding="utf-8") == "ی ک\n"


def test_normalizes_line_endings_without_losing_final_character(tmp_path: Path) -> None:
    source = tmp_path / "line-endings.srt"
    source.write_bytes(b"first\r\nsecond\rthird")

    output = convert_subtitle(source)

    assert output.read_bytes() == b"first\nsecond\nthird"


def test_converts_multiple_files_in_order(tmp_path: Path) -> None:
    first = tmp_path / "first.srt"
    second = tmp_path / "second.srt"
    first.write_bytes("اول\n".encode("windows-1256"))
    second.write_bytes("دوم\n".encode("windows-1256"))

    outputs = convert_subtitles([first, second])

    assert outputs == [tmp_path / "first_fixed.srt", tmp_path / "second_fixed.srt"]
    assert [output.read_text(encoding="utf-8") for output in outputs] == ["اول\n", "دوم\n"]


def test_decode_failure_leaves_existing_destination_unchanged(tmp_path: Path) -> None:
    source = tmp_path / "invalid.srt"
    destination = tmp_path / "invalid_fixed.srt"
    source.write_bytes(b"\xff")
    destination.write_text("preserve this output", encoding="utf-8")

    with pytest.raises(UnicodeDecodeError):
        convert_subtitle(source, source_encoding="utf-8", destination=destination)

    assert destination.read_text(encoding="utf-8") == "preserve this output"
    assert list(tmp_path.glob(".invalid_fixed.srt.*.tmp")) == []


def test_encode_failure_removes_temporary_output(tmp_path: Path) -> None:
    source = tmp_path / "unencodable.srt"
    destination = tmp_path / "unencodable_fixed.srt"
    source.write_bytes("فارسي\n".encode("windows-1256"))
    destination.write_text("preserve this output", encoding="utf-8")

    with pytest.raises(UnicodeEncodeError):
        convert_subtitle(source, target_encoding="ascii", destination=destination)

    assert destination.read_text(encoding="utf-8") == "preserve this output"
    assert list(tmp_path.glob(".unencodable_fixed.srt.*.tmp")) == []
