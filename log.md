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
