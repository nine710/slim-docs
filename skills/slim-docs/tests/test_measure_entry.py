import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "measure_entry.py"


def run_measure(root: Path, tier: str = "low"):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), "--tier", tier],
        capture_output=True,
        text=True,
    )


class TestMeasureEntry(unittest.TestCase):
    def test_fails_when_no_entry_files(self):
        with tempfile.TemporaryDirectory() as d:
            r = run_measure(Path(d), "low")
            self.assertEqual(r.returncode, 1)
            self.assertIn("No entry file", r.stdout + r.stderr)

    def test_passes_when_under_limit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "CLAUDE.md").write_text("\n".join(f"line {i}" for i in range(10)), encoding="utf-8")
            r = run_measure(root, "low")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("CLAUDE.md", r.stdout)

    def test_fails_when_over_limit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "CLAUDE.md").write_text("\n".join(f"line {i}" for i in range(81)), encoding="utf-8")
            r = run_measure(root, "low")
            self.assertEqual(r.returncode, 1)
            self.assertIn("exceeds", (r.stdout + r.stderr).lower())

    def test_tier_medium_allows_100(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "AGENTS.md").write_text("\n".join(f"x{i}" for i in range(100)), encoding="utf-8")
            r = run_measure(root, "medium")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_both_entries_checked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "CLAUDE.md").write_text("\n".join("a" for _ in range(5)), encoding="utf-8")
            (root / "AGENTS.md").write_text("\n".join("b" for _ in range(200)), encoding="utf-8")
            r = run_measure(root, "high")
            self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
