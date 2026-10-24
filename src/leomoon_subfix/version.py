"""Runtime access to the package version."""

from __future__ import annotations

try:
    from ._version import __version__
except ImportError:  # Source checkout before a package build creates _version.py.
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("leomoon-subfix")
    except PackageNotFoundError:
        __version__ = "0.0.0+unknown"
