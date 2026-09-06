"""Tests for reserved-file skips, connectivity warnings, and fence balance.

Run: python -m unittest discover tests.
"""

import tempfile
import unittest
from pathlib import Path

from _helpers import load_module

CC = load_module("check_consistency")
VS = load_module("validate_subtype")

GOOD = (
    "---\ntype: Concept\ntitle: G\ndescription: g\nsubtype_of:\n"
    "  - { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }\n"
    "status: draft\ntags: []\n---\n\n# G\n\nSee [other](./other.md).\n"
)
OTHER = (
    "---\ntype: Concept\ntitle: O\ndescription: o\nsubtype_of:\n"
    "  - { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }\n"
    "status: draft\ntags: []\n---\n\n# O\n"
)


class ReservedAndStructureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "concepts").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_reserved_skipped_by_sources(self):
        (self.root / "README.md").write_text(
            "# R\n\n[^missing] has no sources id.\n", encoding="utf-8"
        )
        issues = []
        CC.check_sources(self.root, issues)
        self.assertEqual(issues, [])

    def test_reserved_skipped_by_placeholders(self):
        (self.root / "CHANGELOG.md").write_text(
            "# C\n\nTODO: write more.\n", encoding="utf-8"
        )
        issues = []
        CC.check_placeholders(self.root, issues)
        self.assertEqual(issues, [])

    def test_connected_concept_passes(self):
        (self.root / "concepts" / "a.md").write_text(GOOD, encoding="utf-8")
        (self.root / "concepts" / "other.md").write_text(
            OTHER.replace("# O\n", "# O\n\nBack to [a](./a.md).\n"), encoding="utf-8"
        )
        issues = []
        CC.check_connectivity(self.root, issues)
        self.assertEqual(issues, [])

    def test_lonely_concept_warns(self):
        (self.root / "concepts" / "solo.md").write_text(OTHER, encoding="utf-8")
        issues = []
        CC.check_connectivity(self.root, issues)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0][0], "WARNING")

    def test_references_exempt(self):
        (self.root / "references").mkdir()
        (self.root / "references" / "r.md").write_text(OTHER, encoding="utf-8")
        issues = []
        CC.check_connectivity(self.root, issues)
        self.assertEqual(issues, [])

    def test_balanced_fences_pass(self):
        (self.root / "concepts" / "a.md").write_text(
            GOOD + "\n```text\ncode\n```\n", encoding="utf-8"
        )
        issues = []
        CC.check_fences(self.root, issues)
        self.assertEqual(issues, [])

    def test_unclosed_fence_errors(self):
        (self.root / "concepts" / "a.md").write_text(
            GOOD + "\n```text\ncode\n", encoding="utf-8"
        )
        issues = []
        CC.check_fences(self.root, issues)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0][0], "ERROR")

    def test_table_blank_inside_errors(self):
        body = GOOD + "\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n| 3 | 4 |\n"
        (self.root / "concepts" / "a.md").write_text(body, encoding="utf-8")
        issues = []
        CC.check_tables(self.root, issues)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0][0], "ERROR")

    def test_table_blank_outside_passes(self):
        body = GOOD + "\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\nText.\n"
        (self.root / "concepts" / "a.md").write_text(body, encoding="utf-8")
        issues = []
        CC.check_tables(self.root, issues)
        self.assertEqual(issues, [])

    def test_blank_between_tables_passes(self):
        body = (
            GOOD + "\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n"
            "| C | D |\n| --- | --- |\n| 3 | 4 |\n"
        )
        (self.root / "concepts" / "a.md").write_text(body, encoding="utf-8")
        issues = []
        CC.check_tables(self.root, issues)
        self.assertEqual(issues, [])

    def test_missing_required_header_errors(self):
        ents = {"Policy": {"required_headers": {"Definition"}, "required_tags": set()}}
        doc = (
            "---\ntype: Policy\ntitle: P\ndescription: p\nsubtype_of:\n"
            "  - { type: Policy, resource: /x.md, version: v0.1.0 }\n"
            "status: draft\ntags: []\n---\n\n# P\n\n## Other\n"
        )
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.md"
            p.write_text(doc, encoding="utf-8")
            issues = VS.validate_concept(p, abstract_entities=ents)
        self.assertTrue(any(lvl == "ERROR" and "Definition" in m for lvl, m in issues))

    def test_present_required_header_passes(self):
        ents = {"Policy": {"required_headers": {"Definition"}, "required_tags": set()}}
        doc = (
            "---\ntype: Policy\ntitle: P\ndescription: p\nsubtype_of:\n"
            "  - { type: Policy, resource: /x.md, version: v0.1.0 }\n"
            "status: draft\ntags: []\n---\n\n# P\n\n## Definition\n\nText.\n"
        )
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.md"
            p.write_text(doc, encoding="utf-8")
            issues = VS.validate_concept(p, abstract_entities=ents)
        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
