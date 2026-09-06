"""Tests for provenance shape (generated/verified carry by and at only).

Run: python -m unittest discover tests.
"""

import unittest
from pathlib import Path

from _helpers import load_module

CC = load_module("check_consistency")


def doc(extra):
    return (
        "---\ntype: Concept\ntitle: T\ndescription: d\n"
        + extra
        + "status: draft\ntags: []\n---\n\n# T\n"
    )


class ProvenanceTests(unittest.TestCase):
    def check(self, frontmatter_extra):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "c.md").write_text(doc(frontmatter_extra), encoding="utf-8")
            issues = []
            CC.check_provenance(root, issues)
            return issues

    def test_clean_provenance_passes(self):
        fm = "generated: { by: human:a, at: '2026-09-05T18:11:16Z' }\nverified:\n- { by: human:b, at: '2026-09-05T18:11:16Z' }\n"
        self.assertEqual(self.check(fm), [])

    def test_version_in_verified_errors(self):
        fm = "generated: { by: human:a, at: '2026-09-05T18:11:16Z' }\nverified:\n- { by: human:b, at: '2026-09-05T18:11:16Z', version: v0.1.0 }\n"
        issues = self.check(fm)
        self.assertTrue(any(lvl == "ERROR" and "extra keys" in m for lvl, m in issues))

    def test_missing_at_errors(self):
        fm = "generated: { by: human:a }\n"
        issues = self.check(fm)
        self.assertTrue(any(lvl == "ERROR" and "by and at" in m for lvl, m in issues))

    def test_missing_by_errors(self):
        fm = "verified:\n- { at: '2026-09-05T18:11:16Z' }\n"
        issues = self.check(fm)
        self.assertTrue(any(lvl == "ERROR" and "by and at" in m for lvl, m in issues))


if __name__ == "__main__":
    unittest.main()
