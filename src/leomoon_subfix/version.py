"""Runtime access to the package version."""

from __future__ import annotations

import os

_build_version = os.environ.get("LEOMOON_SUBFIX_VERSION")

if _build_version:
    __version__ = _build_version
else:
    try:
        from ._version import __version__
    except ImportError:  # Source checkout before a package build creates _version.py.
        from importlib.metadata import PackageNotFoundError, version

        try:
            __version__ = version("leomoon-subfix")
        except PackageNotFoundError:
            __version__ = "0.0.0+unknown"
