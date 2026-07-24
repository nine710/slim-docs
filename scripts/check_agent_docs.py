#!/usr/bin/env python3
"""Validate agent-docs/index.md routing table and topic set for slim-docs tiers."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TIER_TOPIC_RANGES = {"low": (2, 3), "medium": (4, 8), "high": (8, 20)}


def parse_index_rows(index_text: str) -> list[tuple[str, str, str]]:
    """Parse markdown table rows: triggers | path | read when.

    Skips header and separator rows. Returns list of (triggers, path, read_when).
    """
    rows: list[tuple[str, str, str]] = []
    for line in index_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        triggers, path, read_when = parts[0], parts[1], parts[2]
        if triggers.lower().startswith("trigger"):
            continue
        if re.match(r"^[-:]+$", triggers.replace(" ", "")):
            continue
        if set(triggers) <= {"-", ":", " "}:
            continue
        if path.lower() == "path":
            continue
        rows.append((triggers, path, read_when))
    return rows


def list_topic_files(agent_docs: Path) -> list[Path]:
    files = []
    for p in agent_docs.rglob("*.md"):
        if p.name == "index.md":
            continue
        files.append(p)
    return files


def check(root: Path, tier: str) -> tuple[int, list[str]]:
    messages: list[str] = []
    failed = False
    agent_docs = root / "agent-docs"
    index_path = agent_docs / "index.md"

    if not agent_docs.is_dir():
        return 1, ["FAIL: agent-docs/ directory missing"]

    if not index_path.is_file():
        return 1, ["FAIL: agent-docs/index.md missing"]

    index_text = index_path.read_text(encoding="utf-8")
    rows = parse_index_rows(index_text)
    if not rows:
        return 1, [
            "FAIL: no data rows parsed from agent-docs/index.md",
            "Expected a markdown table with columns: triggers | path | read when / get",
            "Example row: | auth, login | auth.md | auth boundaries |",
        ]

    referenced: set[Path] = set()
    for triggers, rel, read_when in rows:
        target = (agent_docs / rel).resolve()
        try:
            target.relative_to(agent_docs.resolve())
        except ValueError:
            messages.append(f"FAIL: path escapes agent-docs/: {rel}")
            failed = True
            continue
        if not target.is_file():
            messages.append(f"FAIL: broken link in index: {rel}")
            failed = True
            continue
        referenced.add(target)
        messages.append(f"OK: index -> {rel} ({triggers[:40]}...)")

    topics = list_topic_files(agent_docs)
    for t in topics:
        if t.resolve() not in referenced:
            messages.append(f"FAIL: orphan topic not in index: {t.relative_to(agent_docs)}")
            failed = True

    lo, hi = TIER_TOPIC_RANGES[tier]
    n = len(topics)
    if n < lo or n > hi:
        messages.append(
            f"FAIL: topic count {n} outside tier={tier} range [{lo}, {hi}]"
        )
        failed = True
    else:
        messages.append(f"OK: topic count {n} within tier={tier} range [{lo}, {hi}]")

    for t in topics:
        head = t.read_text(encoding="utf-8")[:500]
        if "Read when" not in head and "read when" not in head.lower():
            messages.append(f"WARN: missing 'Read when' near top: {t.relative_to(agent_docs)}")

    if failed:
        return 1, messages
    messages.append(f"agent-docs check passed for tier={tier}")
    return 0, messages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate agent-docs index and topics")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--tier",
        choices=sorted(TIER_TOPIC_RANGES.keys()),
        default="medium",
    )
    args = parser.parse_args(argv)
    code, messages = check(args.root.resolve(), args.tier)
    for line in messages:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
