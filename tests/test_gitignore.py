"""Tests for .gitignore-awareness (.gitkeep exception) in bundle scripts.

A git-ignored, untracked file is local-only (absent post-push) and skipped
by validation — unless it sits under a directory holding a .gitkeep marker.
Run: python -m unittest discover tests. Skipped when git is unavailable.
"""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from _helpers import load_module

GOOD = (
    "---\ntype: Skill\ntitle: G\ndescription: g\nsubtype_of:\n"
    "  - { type: Skill, resource: /entities/domain/skill.md, version: v0.1.0 }\n"
    "status: draft\ntags: []\n---\n\n# G\n"
)
BAD = (
    "---\ntype: Skill\ntitle: B\ndescription: b\nsubtype_of:\n"
    "  - { type: Nope, resource: /x.md, version: v0.1.0 }\n"
    "status: draft\ntags: []\n---\n\n# B\n"
)


@unittest.skipUnless(shutil.which("git"), "git not available")
class GitignoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / ".gitignore").write_text("concepts/bad.md\n", encoding="utf-8")
        (self.root / "concepts").mkdir()
        (self.root / "concepts" / "good.md").write_text(GOOD, encoding="utf-8")
        (self.root / "concepts" / "bad.md").write_text(BAD, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_validator_skips_ignored(self):
        vs = load_module("validate_subtype")
        code, _ = vs.validate_bundle(self.root, abstracts_repo=None)
        self.assertEqual(code, 0)

    def test_validator_relative_root(self):
        import os

        vs = load_module("validate_subtype")
        prev = os.getcwd()
        try:
            os.chdir(self.root)
            code, _ = vs.validate_bundle(Path("."), abstracts_repo=None)
            self.assertEqual(code, 0)
        finally:
            os.chdir(prev)

    def test_validator_enforces_gitkeep(self):
        (self.root / "concepts" / ".gitkeep").write_text("", encoding="utf-8")
        vs = load_module("validate_subtype")
        code, _ = vs.validate_bundle(self.root, abstracts_repo=None)
        self.assertEqual(code, 1)

    def test_newlines_skips_ignored(self):
        nl = load_module("check_newlines")
        (self.root / "concepts" / "bad.md").write_text(
            "# no trailing newline", encoding="utf-8"
        )
        self.assertEqual(nl.check_bundle(self.root), [])

    def test_links_skips_ignored(self):
        lk = load_module("check_links")
        (self.root / "concepts" / "bad.md").write_text(
            "# B\n\n[nowhere](./missing.md)\n", encoding="utf-8"
        )
        _, bad = lk.check_bundle(self.root)
        self.assertEqual(bad, [])

    def test_links_enforces_gitkeep(self):
        lk = load_module("check_links")
        (self.root / "concepts" / ".gitkeep").write_text("", encoding="utf-8")
        (self.root / "concepts" / "bad.md").write_text(
            "# B\n\n[nowhere](./missing.md)\n", encoding="utf-8"
        )
        _, bad = lk.check_bundle(self.root)
        self.assertEqual(len(bad), 1)


if __name__ == "__main__":
    unittest.main()
