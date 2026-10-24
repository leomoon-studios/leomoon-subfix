"""Subtitle encoding conversion independent of the graphical interface."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

DEFAULT_SOURCE_ENCODING = "windows-1256"
DEFAULT_TARGET_ENCODING = "utf-8"


def fixed_output_path(source: str | Path) -> Path:
    """Return the default UTF-8 output path for a source subtitle file."""

    source_path = Path(source)
    return source_path.with_name(f"{source_path.stem}_fixed{source_path.suffix}")


def normalize_persian_characters(text: str) -> str:
    """Replace Arabic Yeh and Kaf with their Persian equivalents."""

    return text.replace("ي", "ی").replace("ك", "ک")


def convert_subtitle(
    source: str | Path,
    *,
    source_encoding: str = DEFAULT_SOURCE_ENCODING,
    target_encoding: str = DEFAULT_TARGET_ENCODING,
    normalize_persian: bool = False,
    destination: str | Path | None = None,
) -> Path:
    """Convert one subtitle file and atomically return its output path.

    Input line endings are normalized to LF without discarding the last
    character of a file that has no final newline. A failed conversion leaves
    an existing destination unchanged and removes any temporary output.
    """

    source_path = Path(source)
    output_path = Path(destination) if destination is not None else fixed_output_path(source_path)

    if source_path.resolve() == output_path.resolve():
        raise ValueError("The conversion destination must differ from the source file.")

    with source_path.open("r", encoding=source_encoding, newline=None) as source_file:
        text = source_file.read()

    if normalize_persian:
        text = normalize_persian_characters(text)

    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            dir=output_path.parent,
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding=target_encoding, newline="\n") as output_file:
            output_file.write(text)
        temporary_path.replace(output_path)
        return output_path
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise


def convert_subtitles(
    sources: Iterable[str | Path],
    *,
    source_encoding: str = DEFAULT_SOURCE_ENCODING,
    target_encoding: str = DEFAULT_TARGET_ENCODING,
    normalize_persian: bool = False,
) -> list[Path]:
    """Convert each source and return output paths in the supplied order."""

    return [
        convert_subtitle(
            source,
            source_encoding=source_encoding,
            target_encoding=target_encoding,
            normalize_persian=normalize_persian,
        )
        for source in sources
    ]
