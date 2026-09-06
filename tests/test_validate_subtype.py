"""Fixture tests for scripts/validate_subtype.py.

Each test builds a minimal concept file in a tmp dir and asserts the exact
diagnostics. Run: python -m unittest discover tests  (needs pyyaml).
"""

import tempfile
import unittest
from pathlib import Path

from _helpers import load_module

vs = load_module("validate_subtype")

PINNED = "{ type: Skill, resource: /entities/domain/skill.md, version: v0.1.0 }"
ENTITIES = {
    "Skill": {"required_headers": set(), "required_tags": set()},
    "Concept": {"required_headers": set(), "required_tags": set()},
}


def doc(key, entry, extra=""):
    return (
        "---\ntype: Skill\ntitle: T\ndescription: d\n"
        + key
        + ":\n  - "
        + entry
        + "\nstatus: draft\ntags: []\n---\n\n# T\n"
        + extra
    )


class KeyFlexibilityTests(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.md"
            p.write_text(text, encoding="utf-8")
            return vs.validate_concept(p, abstract_entities=ENTITIES)

    def test_canonical_key_clean(self):
        self.assertEqual(self.check(doc("subtype_of", PINNED)), [])

    def test_legacy_plural_warns_twice(self):
        issues = self.check(doc("subtypes_of", PINNED))
        self.assertEqual(len([i for i in issues if i[0] == "WARNING"]), 2)
        self.assertFalse([i for i in issues if i[0] == "ERROR"])
        self.assertTrue(any("Plural" in m for _, m in issues))

    def test_subclass_singular_warns_once(self):
        issues = self.check(doc("subclass_of", PINNED))
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0][0], "WARNING")
        self.assertFalse(any("Plural" in m for _, m in issues))

    def test_subconcept_warns_once(self):
        issues = self.check(doc("subconcept_of", PINNED))
        self.assertEqual(len(issues), 1)


class LinkageTests(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.md"
            p.write_text(text, encoding="utf-8")
            return vs.validate_concept(p, abstract_entities=ENTITIES)

    def test_first_mismatch_no_match_errors(self):
        entry = "{ type: Concept, resource: /x.md, version: v0.1.0 }"
        issues = self.check(doc("subtype_of", entry))
        self.assertTrue(any(lvl == "ERROR" and "Concept" in m for lvl, m in issues))

    def test_first_mismatch_other_matches_warns(self):
        text = (
            "---\ntype: Skill\ntitle: T\ndescription: d\nsubtype_of:\n"
            "  - { type: Concept, resource: /x.md, version: v0.1.0 }\n"
            "  - " + PINNED + "\nstatus: draft\ntags: []\n---\n\n# T\n"
        )
        issues = self.check(text)
        self.assertFalse([i for i in issues if i[0] == "ERROR"])
        self.assertTrue(any("another entry does match" in m for _, m in issues))

    def test_missing_version_warns(self):
        entry = "{ type: Skill, resource: /entities/domain/skill.md }"
        issues = self.check(doc("subtype_of", entry))
        self.assertTrue(any(lvl == "WARNING" and "version" in m for lvl, m in issues))

    def test_empty_frontmatter_line_errors(self):
        text = "---\ntype: Skill\n\ntitle: T\n---\n\n# T\n"
        issues = self.check(text)
        self.assertTrue(any(lvl == "ERROR" and "Empty line" in m for lvl, m in issues))

    def test_invalid_yaml_reports_cause(self):
        text = "---\ntype: Skill\ndescription: has: colon\n---\n\n# T\n"
        issues = self.check(text)
        self.assertTrue(any(lvl == "ERROR" and "YAML" in m for lvl, m in issues))

    def test_class_self_parent_errors(self):
        text = (
            "---\ntype: Class\ntitle: Skill\nsubtype_of:\n"
            "  - { type: Skill, resource: /s.md, version: v0.1.0 }\n---\n\n# S\n"
        )
        issues = self.check(text)
        self.assertTrue(any(lvl == "ERROR" and "itself" in m for lvl, m in issues))

    def test_class_unknown_parent_errors(self):
        text = (
            "---\ntype: Class\ntitle: Widget\nsubtype_of:\n"
            "  - { type: Nope, resource: /n.md, version: v0.1.0 }\n---\n\n# W\n"
        )
        issues = self.check(text)
        self.assertTrue(any(lvl == "ERROR" and "Nope" in m for lvl, m in issues))

    def test_class_known_parent_passes(self):
        text = (
            "---\ntype: Class\ntitle: Widget\nsubtype_of:\n"
            "  - { type: Skill, resource: /s.md, version: v0.1.0 }\n---\n\n# W\n"
        )
        self.assertEqual(self.check(text), [])


if __name__ == "__main__":
    unittest.main()
