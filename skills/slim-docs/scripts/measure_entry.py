#!/usr/bin/env python3
"""Measure CLAUDE.md / AGENTS.md line counts against slim-docs tier limits."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TIER_LINE_LIMITS = {"low": 80, "medium": 100, "high": 120}
ENTRY_FILENAMES = ("CLAUDE.md", "AGENTS.md")


def count_lines(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    if text == "":
        return 0
    return len(text.splitlines())


def measure(root: Path, tier: str) -> tuple[int, list[str]]:
    limit = TIER_LINE_LIMITS[tier]
    messages: list[str] = []
    found = []
    failed = False

    for name in ENTRY_FILENAMES:
        path = root / name
        if not path.is_file():
            continue
        n = count_lines(path)
        found.append(name)
        status = "OK" if n <= limit else "FAIL"
        messages.append(f"{status}: {name} has {n} lines (limit {limit} for tier={tier})")
        if n > limit:
            failed = True
            messages.append(f"  -> exceeds limit by {n - limit} lines")

    if not found:
        messages.append("No entry file found (expected CLAUDE.md and/or AGENTS.md)")
        return 1, messages

    if failed:
        return 1, messages
    messages.append(f"All entry files within limit for tier={tier}")
    return 0, messages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measure agent entry file line counts")
    parser.add_argument("--root", type=Path, default=Path("."), help="Project root")
    parser.add_argument(
        "--tier",
        choices=sorted(TIER_LINE_LIMITS.keys()),
        default="medium",
        help="Tier line limit",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    code, messages = measure(root, args.tier)
    for line in messages:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
