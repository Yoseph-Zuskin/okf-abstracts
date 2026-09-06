# CHANGELOG

## [0.1.0] - 2026-09-05

### Added

- **Initial public release**: shared OWL-style class ontology for OKF v0.2 knowledge bundles
- **105 abstract classes** across four layers: foundational L0 (8 classes + Spec anchor), core L1 (19), domain L2 (41), application L3 (36)
- **5 skills**: `okf-validate-subtype`, `okf-abstract-lineage`, `okf-generate-bundle`, `okf-intermediate-layers`, `okf-adversarial-review`
- **Validation toolkit** (`scripts/`, `requirement.txt` pins `pyyaml==6.0.3`): subtype validator (canonical `subtype_of` key with `subclass_of`/`subconcept_of` aliases), consistency checker (manifests, indexes, placeholders, sources, skills, graph, URLs, provenance, connectivity, fences, push-completeness), link checker, newline checker, frontmatter YAML checker, abstract lineage checker, bundle generator (codex/claude/devin/grok/qoder/openclaw/copilot targets)
- **Unit tests** (`tests/`): validator diagnostics, generator golden test, gitignore exemption, provenance shape, reserved-file and structure rules
- **Cross-harness manifests**: Codex (plus Codex-native marketplace), Claude, Devin, Grok, Qoder, OpenClaw, Copilot
- **CI and pre-commit**: GitHub Actions CI (tests, strict validation, lineage, lint) and pre-commit hooks (hygiene, ruff, lint-only markdownlint, OKF gates)
