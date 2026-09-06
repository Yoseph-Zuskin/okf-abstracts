# Contributing to okf-abstracts

Thank you for your interest in contributing to **okf-abstracts** — the shared class ontology for OKF v0.2 knowledge bundles.

---

## Core Principles

Before submitting, please keep these tenets in mind:

1. **OWL-style Subtyping Only**: All classes use `subtype_of` (canonical singular) with one most-specific parent first. Plural aliases (`subtypes_of`, `subclass_of`, `subconcept_of`) are accepted with warnings only.
2. **Cross-Repo Pinning**: Downstream bundles pin this repo by URL + version tag (`blob/vX.Y.Z`). Every merge to `main` must keep the lattice strict; every tag must be exactly what the pins promise.
3. **Frontmatter Hygiene**: Descriptions containing a colon use single quotes. `generated` and every `verified[]` entry carry exactly `by` and `at` (actor + ISO 8601). Sources cited with `[^id]` footnotes matching `sources[].id`.
4. **Spec Conformance**: All concepts comply with [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) and the [OKF Style Guide](https://github.com/Yoseph-Zuskin/Bundles/blob/main/OKF_STYLE_GUIDE.md).
5. **Walk the Talk**: Any PR introducing new classes, modifying the lattice, or changing tooling must update `entities/`, `CHANGELOG.md` under `[Unreleased]`, and pass all gates.

---

## Development Setup

### Prerequisites

- Python 3.11+ (stdlib + `pyyaml==6.0.3` only)
- Git
- `make` (optional, for convenience targets)

### Getting Started

```bash
git clone https://github.com/Yoseph-Zuskin/okf-abstracts.git
cd okf-abstracts
pip install -r requirement.txt
```

---

## Development Workflow

### Branching Strategy

- **`develop`** — active development branch; all feature/bugfix branches branch from here
- **`main`** — locked, protected; receives only release PRs from `develop`
- **Feature branches**: `feat/<short-description>` off `develop`
- **Bugfix branches**: `fix/<short-description>` off `develop`

### Commit Message Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New class, skill, validator, or tooling capability
- `fix:` Bug fix in validators, checkers, generator, or docs
- `docs:` Documentation-only changes (README, CHANGELOG, AGENTS, OKF_STYLE_GUIDE.md at workspace root)
- `refactor:` Code restructuring with no behavioral change
- `test:` Adding or updating tests
- `chore:` CI, release, dependency pins, scaffolding

### Knowledge & Ontology Maintenance

If your PR adds/modifies classes, skills, or the lattice:

1. **Layer first**: L0 (foundational) → L1 (core) → L2 (domain) → L3 (application). When torn, prefer the more general layer.
2. **Every class needs a `# Contract`** with at least one falsifiable instance requirement.
3. **`subtype_of` is singular and canonical** — one most-specific parent first. Parent `type` + pinned `version` on every entry; inside this repo `resource` is same-repo relative (`/entities/<layer>/<class>.md`).
4. **Update `CHANGELOG.md` under `## [Unreleased]`** using Added/Changed/Deprecated/Removed/Fixed/Security categories.
5. **Run all gates** (see below) and ensure `0 errors, 0 warnings` on both this repo and the AI-Product-Manager bundle.

---

## Gates (run all before proposing merge)

```bash
# Strict subtype validation (canonical key, alias warnings)
python scripts/validate_subtype.py . --strict

# 12-rule consistency suite (manifests, indexes, placeholders, sources, skills, graph, URLs, provenance, connectivity, fences, tables, push-completeness)
python scripts/check_consistency.py .

# Link checker (internal markdown links + cross-repo anchors)
python scripts/check_links.py .

# Newline checker (exactly 1 trailing newline per .md file)
python scripts/check_newlines.py .

# Unit tests
python -m unittest discover tests

# Pre-commit hygiene (ruff, markdownlint, OKF gates)
pre-commit run --all-files

# Adversarial review skill (no BLOCKING findings)
# (invoke via your agent: "run okf-adversarial-review skill on this bundle")
```

All must pass with `0 errors, 0 warnings` on both this repo and the AI-Product-Manager bundle.

---

## Release Workflow (maintainer only)

1. On `develop`, verify `## [Unreleased]` in `CHANGELOG.md` has the right bullets.
2. Dispatch the `release` workflow (Actions tab → `release` → "Run workflow") with explicit version:
   - Patch: `0.1.1` (bug fixes, tooling cleanup, docs)
   - Minor: `0.2.0` (new classes, skills, backward-compatible additions)
   - Major: `1.0.0` (breaking changes to contracts, Spec anchor, layer reorg)
3. Workflow bumps `VERSION`, promotes `[Unreleased]` → `[version] - date`, prepends fresh `[Unreleased]`, opens `release/vX.Y.Z` PR.
4. Review the PR (reconcile any duplicate headers), squash-merge to `main`.
5. Tag job fires on `VERSION` change → creates `vX.Y.Z` tag + GitHub Release.
6. **Release this repo before downstream bundles** — their CI pins this repo by tag, which must exist and be public.

---

## Pre-Submission Checklist

- [ ] `python -m py_compile scripts/*.py` clean
- [ ] All gates above pass (`0 errors, 0 warnings`)
- [ ] `CHANGELOG.md` updated under `## [Unreleased]`
- [ ] `log.md` appended to today's section (ISO 8601 date)
- [ ] Relevant documentation (`README.md`, `AGENTS.md`, `OKF_STYLE_GUIDE.md` at workspace root) updated
- [ ] **Adversarial review completed: run `okf-adversarial-review` skill on this bundle — no BLOCKING findings**

---

## Pull Request Process

1. Push branch to your fork.
2. Open PR against `develop`.
3. Describe: what problem, what changes, how verified.
4. Ensure all GitHub Actions checks pass green.
5. Squash-merge on approval (you are the sole approver).

---

## License

MIT. See [LICENSE](LICENSE).

---

*By contributing, you agree that your contributions will be licensed under the MIT License.*
