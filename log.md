# Directory Update Log

## 2026-08-19

* **Initialization**: Created the `okf-abstracts` bundle as a shared class ontology for
  the bundle workspace, modeled on the OWL `subClassOf` pattern with a four-level class
  lattice (very basic abstractions, general concepts, specialized entities, specific types).
  Root is the Google OKF v0.2 specification; `thing` is the universal root class. Concrete
  concepts in the workspace bundles reference these classes with a `subtype_of` frontmatter
  list.

* **Restructure into OWL layers**: Reorganized `entities/` into four subdirectories —
  `foundational/` (L0), `core/` (L1), `domain/` (L2), `application/` (L3) — moved all 33
  class files, rewrote internal `resource` paths, and migrated the pinned cross-bundle
  `subtype_of` URLs to the layer-aware paths (version pin unchanged `v0.1.0`). Removed
  the `build_abstracts.py` generator so the bundle contains only OKF content; class files
  are now hand-maintained.

## 2026-08-23

* **Review pass**: third-party agent review across the workspace bundles; findings
  recorded as `verified` stamps on reviewed files.

## 2026-08-29

* **Role and governance batch**: Added `Role`, `Stakeholder`, `Sponsor`, `Client`,
  `Approver`, `Decision`, `Approval` (L1) with a documented played-by pattern
  (roles are played by agents; instances link both branches).
* **Skill branch**: Added `okf-validate-subtype`, `okf-abstract-lineage`,
  `okf-generate-bundle`, `okf-intermediate-layers` skills plus `ExecPlan`,
  `Generator`, `Validator` (L2) entities.

## 2026-09-05

* **Reparenting pass**: Business Department and Country are Organizations;
  paradigms under Machine Learning Algorithm; Stakeholder/Sponsor/Client/Approver
  under Agent (dual-linked to Role); Decision Maker under Approver; Product User
  under Persona; Quality/Relation under Entity; SDLC under Workflow; ExecPlan
  under Operational Artifact; infrastructure under new `Infrastructure` (L2);
  classification/regression/clustering under new `Machine Learning Task` (L2),
  separating tasks from paradigms. Pinned all 104 parent versions.
* **Canonical key**: `subtypes_of` renamed to `subtype_of` across linked bundles;
  validator accepts `subclass_of`/`subconcept_of` aliases with warnings.
* **Contracts sharpened**: merged doubled `## Contract` sections; added one
  falsifiable instance requirement to the ten most-subtyped parents.
* **Thing root**: `thing` subtypes the Spec anchor per AGENTS.md.

## 2026-09-05 (continued)

* **Correction**: the 09-05 reparenting entry above is superseded where it says
  paradigms sit under Machine Learning Algorithm and role classes dual-link
  Agent and Role. Supervised/Unsupervised/Reinforcement now subtype the new
  `Learning Paradigm` (L2); Stakeholder/Sponsor/Client/Approver subtype `Role`
  only and Decision Maker subtypes `Approver` only (instances dual-link per
  `role.md:30`). Counts are 105 public classes (8+19+42+36).
* **Dedup**: `Email` (L3) removed as duplicating `Email Message`.
* **Tooling**: validator scans all content paths with Class-parent rules;
  consistency suite (manifests, indexes, placeholders, sources, skills, graph,
  URLs, provenance, connectivity, fences, push-completeness); link/newline/
  frontmatter checkers; gitignore-aware with `.gitkeep` exceptions; unit tests;
  CI and pre-commit gates; Copilot harness target in the generator.
* **Review skill**: Added `okf-adversarial-review` protocol skill.
* **Provenance rule**: `generated`/`verified[]` carry `by` and `at` only.
* **Tooling slim-down**: removed dead lineage-checker flags
  (`--update-versions`, `--check-all`) and dead logger; deleted unread
  `_load_entities` from the generator; cut the unreachable Check 3b branch
  and dead plural aliases from the subtype validator.
* **Checker dedup**: one `parse_frontmatter` (`_common.py`) across the
  consistency checker; shared `RESERVED_FILES`/`SKIP_DIRS`; one
  `find_manifests()` helper; one `iter_bundle_mds()` walk adopted by all
  checkers. Gates re-verified green (35/35 tests, strict 0/0 both bundles).

## 2026-09-07

* **Validator scope**: `validate_subtype` now walks concept paths only —
  `docs/` process docs and `.openclaw/` generated mirrors are out of scope
  (they broke `--strict`); dead imports dropped. Gates green (35/35 tests).
* **Path fix**: `_is_local_only` no longer double-joins CWD-relative roots,
  so git-ignored local-only files are correctly exempt from indexing.
* **Release workflow**: tag job fetches tags before checking (re-push safe);
  auto-merge removed (solo repo — the merge click is the audit gate);
  Node-24 action majors.
* **Docs**: new `CONTRIBUTING.md`, `README.md` (105 classes, 8+19+42+36),
  `AGENTS.md`; markdownlint numbering and link fixes.
* **v0.1.1 goals**: expand the bundle generator from 7 supported harnesses
  to the 14 configured in AI-Product-Manager (add cursor, windsurf, cline,
  kiro, opencode, pi, gemini, mcp targets; fold qoder rules/hooks into the
  qoder target); add missing `privacy.md` + `terms.md` (AI-PM ships both;
  abstracts has neither yet - draft, don't generate until scoped).

## 2026-09-12

* **SkillSpector scan**: static-only (no LLM provider locally), score 81 on
  42 hits, every one verified false positive (ignored pycache artifacts,
  mislabeled lint invocations, doc citations, fixed-argv git calls). No MCP
  server, hooks, or network sinks in repo. Verdict: no actionable issue.
* **Skill-subtype research**: three subagents inventoried Superpowers (14),
  Ponytail (6), and OpenAI plugins (62 plugins, 535 skills). Converged
  extensions for the Skill class: header equivalence classes, blessed
  Overview/When-to-Use/Rationalizations/Red-Flags/Boundaries sections,
  optional invocation metadata, new Plugin and Command parents, behavioral
  and meta subtypes, optional routing key, Workflow-less implies Reference.
  No implementation - queued for lattice review.
* **SECURITY.md**: vulnerability policy plus scan triage; `SECURITY.md`
  (and missing `CONTRIBUTING.md`, `PULL_REQUEST_TEMPLATE.md`) added to
  `RESERVED_FILES`.
* **CI verdict**: SkillSpector viable in CI only as fork-safe static job
  gated on recommendation (never raw exit code); LLM stage conditional on
  non-fork runs with secrets. No workflow added yet.

## 2026-09-13

* **Semantic scan**: `opencode_cli` provider with Nemotron 3 Ultra Free,
  score 83/100 (static 81 + 2 semantic delta), 0 semantic findings (3
  analyzers succeeded, 1 degraded). Delta: 0 findings — no actionable
  security issues. Static CRITICAL score remains a pattern artifact.
* **SECURITY.md**: updated with semantic scan addendum (score 83, 0
  findings, posture unchanged).
* **Semantic re-scan (Muse Spark)**: `opencode_cli` provider, model
  `opencode/muse-spark-1.3-contributor-free`, score 83/100 — identical to
  the Nemotron semantic baseline. LLM stage degraded (0/4 calls: shared
  runtime budget expired before any model inference), so the run is
  static-only and the model was never invoked.
* **Triage**: 0 new findings, 0 new true positives — posture unchanged.
* **SECURITY.md**: appended Muse Spark re-scan addendum.
* **Semantic re-scan (Nemotron 3 Ultra Free)**: `opencode_cli` provider,
  model `opencode/nemotron-3-ultra-free`, score 83/100 — identical to the
  prior semantic baseline. LLM stage degraded (0/4 calls: shared runtime
  budget expired), run is static-only, no new findings. Posture unchanged.

## 2026-09-19

* **Semantic re-scan (Copilot Free)**: `copilot_cli` provider (local
  fork), all 5 skills executed successfully — max risk 34 (CAUTION),
  4 findings triaged (2 HIGH analyzer misfires on markdown-only
  skills; lineage contract vs `--update-versions` doc inconsistency;
  intermediate-layers missing mutation warning). No exploitable
  issues. `opencode_cli`/Nemotron route delivered 0/4 LLM calls:
  Zen answers 403 to any call carrying the deny-all isolation
  (bisected, model-independent, new since 09-12).
* **Skill doc fixes**: lineage read-only default vs confirmed writes,
  intermediate-layers mutation warning, validate-subtype
  allowed-tools scope.
* **Adversarial review**: READY-WITH-FIXES — 2 private-origin drafts moved out of the bundle
  to local-only `docs/abstracts/`; counts confirmed 105 (L3 36).
* **SkillEvaluator Tier 1 (keyless)**: PII/Unicode/License/Lint PASS,
  quality grade C; `validate`-gate fails are Agent-Skills contract
  mismatch (advisory, policy-overlay territory).
* **Tooling**: `check_newlines.py` counts in-scope files only;
  RESERVED_FILES filtering experiment in `iter_bundle_mds`
  reverted (stripped hygiene coverage; ontology checkers already
  skip reserved files); `SECURITY.md` + `CHANGELOG.md` scan addenda.

## 2026-09-20

* **README**: new Install section (clone / pin / 7 harnesses),
  Quickstart normalized to Quick Start, BundleDex badge.
* **PR template**: explicit `Fixes: #NNN` field + no-issue-no-merge
  checklist item.
* **PR #2**: chore/release-hardening branch pushed, 4 commits,
  awaiting signed-commit setup (branch protection requires
  cryptographic signatures, not just DCO trailers).
