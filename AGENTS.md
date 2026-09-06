# AGENTS.md

## Critical Instruction

**NEVER COMMIT OR PUSH CHANGES YOURSELF.** Always leave changes locally for the user to review and decide if they're ready to push. The user will explicitly ask for commits/pushes when ready.

## What This Repo Is

Public shared class ontology for [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) knowledge bundles, modeled on the OWL `subClassOf` pattern. Downstream bundles pin it by URL + version tag (`blob/vX.Y.Z`), and their CI resolves those pins — so every merge to `main` must keep the lattice strict and every tag must be exactly what the pins promise. Quality here propagates; sloppiness here breaks other repos.

## Layout

- `entities/<layer>/<class>.md` — the ontology. `<layer>` is `foundational` (L0), `core` (L1), `domain` (L2), or `application` (L3). Every file is `type: Class`.
- `skills/` — executable skills (`validate-subtype`, `lineage`, `generate`, `layers`, `adversarial-review`).
- `scripts/` + `tests/` — validators, checkers, generator, unit tests (`requirement.txt` pins `pyyaml`, nothing else).
- `index.md`, `log.md`, `CHANGELOG.md`, `VERSION`, `LICENSE` — scaffolding; never concepts.

## Proposing a Class or Change

- **Layer first.** L0: domain-neutral abstractions. L1: general concepts reusable across domains. L2: domain specializations. L3: application-specific leaves. When torn between two layers, prefer the more general one — downstream bundles specialize.
- **Every class needs a `# Contract` section** with at least one falsifiable requirement on instances (what must hold, not what the class means). A class without a testable contract is a glossary entry, not ontology.
- **`subtype_of` is singular and canonical.** One most-specific parent, first entry. Aliases (`subtypes_of`, `subclass_of`, `subconcept_of`) are accepted with warnings — never introduce new ones. Parent `type` + pinned `version` on every entry; inside this repo `resource` is same-repo relative (`/entities/<layer>/<class>.md`).
- **Frontmatter hygiene:** descriptions containing a colon use single quotes, never double. `generated` and every `verified[]` entry carry exactly `by` and `at` (actor + ISO 8601, no other keys). Sources cited with `[^id]` footnotes matching `sources[].id`.
- **One trailing newline** per Markdown file, no trailing blank lines. Never hand-edit generated copies; re-run the generator.

## Gates (run all, before proposing merge)

`validate_subtype.py --strict` (0 errors, 0 warnings), `check_consistency.py`, `check_links.py`, `check_newlines.py`, `python -m unittest discover tests`, and `pre-commit run --all-files`. Then the `okf-adversarial-review` skill — BLOCKING findings must clear before release.

## Changelog & Release

- Log user-facing changes under `## [Unreleased]` in `CHANGELOG.md`; never pre-create version sections or delete `Unreleased` (the release workflow promotes it and fails without it). `log.md` keeps one section per day.
- Release: dispatch the `release` workflow with `x.y.z` → `release/vX.Y.Z` PR from `develop` (version bump + promotion) → review → merge to `main` → tag `vX.Y.Z` + GitHub Release. Release this repo before downstream bundles — their pins resolve only after the tag exists and this repo is public.
