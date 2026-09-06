---
type: Class
title: Learning Paradigm
description: 'A paradigm governing how machine learning happens (from labeled data, from unlabeled structure, through interaction rewards). Paradigms are not procedures and not tasks: a paradigm is how learning happens, an algorithm is the procedure, a task is what gets solved.'
subtype_of:
- { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }
status: stable
stale_after: 2027-09-05
generated: { by: human:yoseph-zuskin, at: '2026-09-05T18:11:16Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- machine-learning
- paradigms
---

# Learning Paradigm

A learning paradigm names HOW machine learning happens: from labeled examples (supervised), from unlabeled structure (unsupervised), or through interaction rewards (reinforcement). It is neither a procedure (`Machine Learning Algorithm`) nor a problem type (`Machine Learning Task`).

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

Instances of `Learning Paradigm` MUST:

- State the learning signal (labels, structure, rewards) the paradigm learns from.

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
