---
okf_version: "0.2"
---
# OKF Abstract Classes

Shared class ontology for knowledge bundles which adhere to OKF v0.2, modeled on the OWL
`subClassOf` pattern. Concrete concepts in other bundles reference these classes via a
`subtype_of` frontmatter list of `{ type, resource, version }` entries.

## Layers

The lattice is organized into four OWL-style layers, each a subdirectory of
`entities/` with its own `index.md`:

* [Foundational (L0)](/entities/foundational/index.md) - 8 classes plus the Spec anchor: very basic

  abstractions; the top of the lattice.
* [Core (L1)](/entities/core/index.md) - 19 classes: general domain-neutral

  concepts.
* [Domain (L2)](/entities/domain/index.md) - 42 classes: specialized entities

  and content genres.
* [Application (L3)](/entities/application/index.md) - 36 classes: specific

  types.

## Implemented by

* [AI-Product-Manager](https://www.github.com/Yoseph-Zuskin/ai-product-manager) - public bundle curating

  product-management knowledge (type: Agent).
* AI Strategies for Business Transformations - private; concepts reference the

  classes above.
* AI-Driven Product Strategy - private; concepts reference the classes above.

## Skills

* [OKF Validate Subtype](/skills/okf-validate-subtype/SKILL.md) - validates
  `subtype_of` linkage against these classes.
* [OKF Abstract Lineage](/skills/okf-abstract-lineage/SKILL.md) - detects
  abstract changes newer than concept verification.
* [OKF Generate Bundle](/skills/okf-generate-bundle/SKILL.md) - generates new
  bundles with abstract lineage.
* [OKF Intermediate Layers](/skills/okf-intermediate-layers/SKILL.md) - helps
  add custom layers between the four.
* [OKF Adversarial Review](/skills/okf-adversarial-review/SKILL.md) - reviews
  bundles for logical quality before release or contribution.
