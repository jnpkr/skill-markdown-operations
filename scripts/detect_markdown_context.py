#!/usr/bin/env python3
"""Classify a target path as standard Markdown or part of an Obsidian vault."""

import argparse
import stat
import sys
from pathlib import Path
from typing import Optional


def parse_args() -> Path:
    """Parse the target path from the command line."""
    parser = argparse.ArgumentParser(
        description=(
            "Classify an existing or proposed path as standard Markdown or part "
            "of an Obsidian vault."
        )
    )
    parser.add_argument("target_path", type=Path)
    return parser.parse_args().target_path


def nearest_existing_path(target: Path) -> Path:
    """Return the target or its nearest existing ancestor."""
    candidate = target

    while True:
        try:
            candidate.stat()
        except FileNotFoundError:
            parent = candidate.parent
            if parent == candidate:
                raise
            candidate = parent
        else:
            return candidate


def start_directory(target: Path) -> Path:
    """Resolve the directory from which ancestor detection should begin."""
    expanded = target.expanduser()
    absolute = expanded if expanded.is_absolute() else Path.cwd() / expanded
    existing = nearest_existing_path(absolute)
    resolved = existing.resolve(strict=True)

    if stat.S_ISDIR(resolved.stat().st_mode):
        return resolved
    return resolved.parent


def find_vault_root(target: Path) -> Optional[Path]:
    """Return the nearest ancestor containing an .obsidian directory."""
    start = start_directory(target)

    for directory in (start, *start.parents):
        marker = directory / ".obsidian"
        try:
            marker_mode = marker.stat().st_mode
        except FileNotFoundError:
            continue

        if stat.S_ISDIR(marker_mode):
            return directory

    return None


def main() -> int:
    """Classify the requested target and emit a stable key-value result."""
    target = parse_args()

    try:
        vault_root = find_vault_root(target)
    except (OSError, RuntimeError) as error:
        print(f"Unable to classify {target}: {error}", file=sys.stderr)
        return 1

    if vault_root is None:
        print("context=standard-markdown")
        print("vault_root=")
    else:
        print("context=obsidian")
        print(f"vault_root={vault_root}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
