#!/usr/bin/env python3
"""Launch a packaged application briefly and fail if it exits with an error."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("application", type=Path)
    parser.add_argument("--seconds", type=float, default=3.0)
    args = parser.parse_args()
    if not args.application.is_file():
        print(f"error: packaged application was not found: {args.application}", file=sys.stderr)
        return 2

    environment = os.environ.copy()
    environment.setdefault("QT_QPA_PLATFORM", "offscreen")
    environment.setdefault("QT_QPA_PLATFORMTHEME", "")
    environment.setdefault("QT_STYLE_OVERRIDE", "Fusion")
    process = subprocess.Popen(
        [str(args.application)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=environment,
    )
    time.sleep(args.seconds)
    status = process.poll()
    if status is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        return 0
    output = process.stdout.read() if process.stdout else ""
    print(output, file=sys.stderr, end="")
    print(f"error: packaged application exited early with status {status}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
