# CHANGELOG

## [Unreleased]

## [0.1.1] - 2026-09-20
### Added

- `CONTRIBUTING.md`, `README.md`, `AGENTS.md`: contribution workflow, repo overview, agent instructions
- `SECURITY.md`: vulnerability reporting policy + SkillSpector static-scan triage (all findings false positives; no actionable issue)
- `README.md`: Install section (clone / pin-as-dependency / 7 harness manifests), BundleDex badge
- PR template: explicit `Fixes:` field plus no-issue-no-merge checklist item

### Fixed

- Validator walks concept paths only (`docs/`, `.openclaw/` mirrors out of scope)
- `_is_local_only` path resolution with CWD-relative bundle roots
- `release.yml`: tag job fetches tags first; auto-merge removed; Node-24 action majors
- `README` counts and layer enumerations verified against the index (105 classes, 8+19+42+36)
- Skill contract clarifications from SkillSpector semantic findings: `okf-abstract-lineage` read-only default vs confirmed `--update-versions` writes, `okf-intermediate-layers` mutation warning, `okf-validate-subtype` allowed-tools scope
- Adversarial review: private-origin drafts moved out of the bundle to local-only `docs/abstracts/`; counts confirmed 105 (L3 36)
- Reverted RESERVED_FILES filtering in `iter_bundle_mds` (ontology checkers already skip reserved files; the shared change stripped hygiene coverage)

### Security

- SkillSpector 2.11.2 semantic re-scan of `skills/` (2026-09-19, `copilot_cli`/Copilot Free, all 5 skills successful): max risk 34 (CAUTION); 2 HIGH hits are analyzer misfires on markdown-only skills (FP), 1 MEDIUM doc inconsistency and 1 MEDIUM missing-mutation-warning logged as doc-clarity backlog. No exploitable issues; see `SECURITY.md`

## [0.1.0] - 2026-09-05

### Added

- **Initial public release**: shared OWL-style class ontology for OKF v0.2 knowledge bundles
- **105 abstract classes** across four layers: foundational L0 (8 classes + Spec anchor), core L1 (19), domain L2 (41), application L3 (36)
- **5 skills**: `okf-validate-subtype`, `okf-abstract-lineage`, `okf-generate-bundle`, `okf-intermediate-layers`, `okf-adversarial-review`
- **Validation toolkit** (`scripts/`, `requirement.txt` pins `pyyaml==6.0.3`): subtype validator (canonical `subtype_of` key with `subclass_of`/`subconcept_of` aliases), consistency checker (manifests, indexes, placeholders, sources, skills, graph, URLs, provenance, connectivity, fences, push-completeness), link checker, newline checker, frontmatter YAML checker, abstract lineage checker, bundle generator (codex/claude/devin/grok/qoder/openclaw/copilot targets)
- **Unit tests** (`tests/`): validator diagnostics, generator golden test, gitignore exemption, provenance shape, reserved-file and structure rules
- **Cross-harness manifests**: Codex (plus Codex-native marketplace), Claude, Devin, Grok, Qoder, OpenClaw, Copilot
- **CI and pre-commit**: GitHub Actions CI (tests, strict validation, lineage, lint) and pre-commit hooks (hygiene, ruff, lint-only markdownlint, OKF gates)

### Changed

- **Tooling slim-down**: removed dead lineage-checker flags and logger, unread generator method, unreachable validator branch and aliases
- **Checker dedup**: shared frontmatter parser, constants, manifest finder, and file-walk iterator in `_common.py`; all gates re-verified green
