---
okf_version: "0.2"
---

# OKF Abstract Classes

Shared class ontology for knowledge bundles which adhere to OKF v0.2, modeled on the OWL
`subClassOf` pattern. Concrete concepts in other bundles reference these classes via a
`subtypes_of` frontmatter list of `{ type, resource, version }` entries.

# Layers

The lattice is organized into four OWL-style layers, each a subdirectory of `entities/` with its own `index.md`:

* [Foundational (L0)](/entities/foundational/index.md) - 9 classes: very basic abstractions; the top of the lattice.
* [Core (L1)](/entities/core/index.md) - 12 classes: general domain-neutral concepts.
* [Domain (L2)](/entities/domain/index.md) - 32 classes: specialized entities and content genres.
* [Application (L3)](/entities/application/index.md) - 42 classes: specific types.

# Implemented by

* [AI-Product-Manager](https://www.github.com/Yoseph-Zuskin/ai-product-manager) - public bundle curating product-management knowledge (type: Agent).
* AI Strategies for Business Transformations - private; concepts reference the classes above.
* AI-Driven Product Strategy - private; concepts reference the classes above.
