# okf-abstracts

> **Shared OWL-style Class Ontology for OKF v0.2 Knowledge Bundles** — 105 public abstract classes across four layers, modeled on the `subClassOf` pattern.

[![Specification](https://img.shields.io/badge/Specification-OKF_v0.2-blue.svg)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) [![Version](https://img.shields.io/badge/Version-0.1.0-green.svg)](https://github.com/Yoseph-Zuskin/okf-abstracts/releases/tag/v0.1.0) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

**okf-abstracts** is the public, shared class ontology that downstream OKF v0.2 knowledge bundles pin by URL + version tag. It provides 105 public abstract `type: Class` concepts organized into four OWL-style layers, plus the `Spec` anchor for the OKF specification itself.

Every class carries a `# Contract` section stating what instances must do — making this a living, testable ontology, not a glossary.

---

## Layer Architecture

| Layer | Name | Count | Purpose |
| ----- | ---- | ----- | ------- |
| **L0** | `foundational/` | 8 | Domain-neutral upper-ontology primitives (Thing, Entity, Concept, Process, Agent, Object, Quality, Relation — plus the Spec anchor) |
| **L1** | `core/` | 19 | General reusable concepts (Person, Organization, Role, Approver, Approval, Workflow, Artifact, Asset, Event, Decision, Instructional Artifact, Communicative Artifact, Knowledge Artifact, Operational Artifact, Metric, Client, Sponsor, Stakeholder, Software Agent) |
| **L2** | `domain/` | 42 | Domain specializations (Infrastructure, ML Task, Learning Paradigm, Generator, Validator, Skill, Template, Reference, Persona, Architecture Pattern, Product, Business Department, Country, Case Study, Election, etc.) |
| **L3** | `application/` | 36 | Application-specific leaves (SaaS Product, Cloud Infrastructure, Buyer Persona, Regression, Classification, Deep Learning, Supervised/Unsupervised/Reinforcement Learning, etc.) |

**Lattice Root**: `Thing` subtypes the `Spec` anchor per AGENTS.md — the entire lattice is a subtype of the OKF spec itself.

---

## Skills

Five executable skills for bundle authors and downstream consumers:

| Skill | Purpose |
| ----- | ------- |
| `okf-validate-subtype` | Strict `subtype_of` lattice validation (canonical `subtype_of`, alias warnings) |
| `okf-abstract-lineage` | Timestamp-based check: have abstract entities changed since concept verification? |
| `okf-generate-bundle` | Bare-bones OKF v0.2 bundle scaffolding (7 harness targets) |
| `okf-intermediate-layers` | L1/L2 layer management utilities |
| `okf-adversarial-review` | Read-only review protocol; BLOCKING findings must clear before release |

---

## Quickstart

### Prerequisites

- Python 3.11+ (stdlib + `pyyaml==6.0.3` only)
- Git

### Installation

```bash
git clone https://github.com/Yoseph-Zuskin/okf-abstracts.git
cd okf-abstracts
pip install -r requirement.txt
```

### Run Gates

```bash
# Strict subtype validation
python scripts/validate_subtype.py . --strict

# Consistency, links, newlines
python scripts/check_consistency.py .
python scripts/check_links.py .
python scripts/check_newlines.py .

# Unit tests
python -m unittest discover tests

# Pre-commit hygiene
pre-commit run --all-files
```

---

## Pinning This Repo

Downstream bundles pin by tag URL:

```yaml
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
```

**Release order matters**: this repo must be released (public + tagged) before downstream bundles — their CI resolves pins only after the tag exists and the repo is public.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete contribution workflow, development setup, commit conventions, gates, and release process.

---

## License

MIT. See [LICENSE](LICENSE).

---

## References

- [OKF v0.2 Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [OKF Viewer / Visualization](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md)
- [okf-skills](https://github.com/scaccogatto/okf-skills) — reference validator for OKF v0.2 compliance
