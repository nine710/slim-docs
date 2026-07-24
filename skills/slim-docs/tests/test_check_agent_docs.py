import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_agent_docs.py"


def run_check(root: Path, tier: str = "low"):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), "--tier", tier],
        capture_output=True,
        text=True,
    )


def write_good_low(root: Path):
    ad = root / "agent-docs"
    ad.mkdir(parents=True)
    (ad / "architecture-map.md").write_text(
        "Read when: layout\nOut of scope: none\n\n## Invariants\n- x\n",
        encoding="utf-8",
    )
    (ad / "commands-and-verify.md").write_text(
        "Read when: test build\nOut of scope: deploy\n\n## Verify\n- pytest\n",
        encoding="utf-8",
    )
    (ad / "index.md").write_text(
        """# agent-docs index

| triggers (keywords / globs) | path | read when / get |
|-----------------------------|------|-----------------|
| layout, modules, where | architecture-map.md | map of modules |
| build, test, lint, verify | commands-and-verify.md | how to verify |
""",
        encoding="utf-8",
    )


class TestCheckAgentDocs(unittest.TestCase):
    def test_fails_without_agent_docs(self):
        with tempfile.TemporaryDirectory() as d:
            r = run_check(Path(d), "low")
            self.assertEqual(r.returncode, 1)
            self.assertIn("agent-docs", (r.stdout + r.stderr).lower())

    def test_passes_good_low(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_good_low(root)
            r = run_check(root, "low")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_fails_broken_link(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_good_low(root)
            idx = (root / "agent-docs" / "index.md").read_text(encoding="utf-8")
            idx = idx.replace("architecture-map.md", "missing-map.md")
            (root / "agent-docs" / "index.md").write_text(idx, encoding="utf-8")
            r = run_check(root, "low")
            self.assertEqual(r.returncode, 1)
            self.assertIn("missing-map.md", r.stdout + r.stderr)

    def test_fails_orphan_topic(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_good_low(root)
            (root / "agent-docs" / "orphan.md").write_text(
                "Read when: never\n", encoding="utf-8"
            )
            r = run_check(root, "low")
            self.assertEqual(r.returncode, 1)
            self.assertIn("orphan", (r.stdout + r.stderr).lower())

    def test_fails_topic_count_outside_tier(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_good_low(root)
            # low needs 2-3; add two more topics + index rows → 4 topics → fail low
            ad = root / "agent-docs"
            for name in ("t3.md", "t4.md"):
                (ad / name).write_text(f"Read when: {name}\n", encoding="utf-8")
            idx = (ad / "index.md").read_text(encoding="utf-8")
            idx += "| t3 | t3.md | t3 |\n| t4 | t4.md | t4 |\n"
            (ad / "index.md").write_text(idx, encoding="utf-8")
            r = run_check(root, "low")
            self.assertEqual(r.returncode, 1)
            self.assertIn("topic count", (r.stdout + r.stderr).lower())


if __name__ == "__main__":
    unittest.main()
