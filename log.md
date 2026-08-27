# Directory Update Log

## 2026-08-19

* **Initialization**: Created the `okf-abstracts` bundle as a shared class ontology for
  the bundle workspace, modeled on the OWL `subClassOf` pattern with a four-level class
  lattice (very basic abstractions, general concepts, specialized entities, specific types).
  Root is the Google OKF v0.2 specification; `thing` is the universal root class. Concrete
  concepts in the workspace bundles reference these classes with a `subtypes_of` frontmatter
  list.

* **Restructure into OWL layers**: Reorganized `entities/` into four subdirectories —
  `foundational/` (L0), `core/` (L1), `domain/` (L2), `application/` (L3) — moved all 33
  class files, rewrote internal `resource` paths, and migrated the pinned cross-bundle
  `subtypes_of` URLs to the layer-aware paths (version pin unchanged `v0.1.0`). Removed
  the `build_abstracts.py` generator so the bundle contains only OKF content; class files
  are now hand-maintained.
