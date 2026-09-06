"""Golden tests for scripts/generate_bundle.py.

Generates a bundle into a tmp dir, asserts canonical output shape, then
validates the result. Run: python -m unittest discover tests.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _helpers import REPO, load_module

GEN = REPO / "scripts" / "generate_bundle.py"


class GenerateBundleTests(unittest.TestCase):
    def test_generates_canonical_valid_bundle(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "bundle"
            r = subprocess.run(
                [
                    sys.executable,
                    str(GEN),
                    "--title",
                    "T",
                    "--domain",
                    "test",
                    "--harnesses",
                    "codex,copilot",
                    str(out),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((out / ".github" / "plugin.json").exists())
            self.assertTrue((out / ".codex-plugin" / "plugin.json").exists())
            skills = list((out / "skills").iterdir())
            concepts = list((out / "concepts").glob("*.md"))
            templates = list((out / "templates").glob("*.md"))
            self.assertEqual(len(skills), 1)
            self.assertEqual(len(concepts), 1)
            self.assertEqual(len(templates), 1)
            texts = [p.read_text(encoding="utf-8") for p in out.rglob("*.md")]
            self.assertTrue(any("subtype_of:" in t for t in texts))
            self.assertFalse(any("subtypes_of:" in t for t in texts))
            self.assertFalse(any("TODO" in t for t in texts))
            vs = load_module("validate_subtype")
            code, _ = vs.validate_bundle(out, abstracts_repo=REPO)
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
