---
okf_version: "0.2"
---

# OKF Abstract Classes

Shared class ontology for knowledge bundles which adhere to OKF v0.2, modeled on the OWL
`subClassOf` pattern. Concrete concepts in other bundles reference these classes via a
`subtypes_of` frontmatter list of `{ type, resource, version }` entries.

# Classes

The lattice is organized into four OWL-style layers, each a subdirectory of `entities/`:

* `foundational/` - L0, very basic abstractions; the top of the lattice.
* `core/` - L1, general domain-neutral concepts.
* `domain/` - L2, specialized entities and content genres.
* `application/` - L3, specific types.

## Foundational (L0 - very basic abstractions)

* [Spec](/entities/foundational/okf-spec.md) - the canonical Google OKF v0.2 specification, top of the lattice.
* [Thing](/entities/foundational/thing.md) - universal root class; everything is a Thing.
* [Entity](/entities/foundational/entity.md) - anything that exists.
* [Object](/entities/foundational/object.md) - a bounded, spatiotemporal thing.
* [Concept](/entities/foundational/concept.md) - a unit of knowledge.
* [Process](/entities/foundational/process.md) - something that unfolds over time.
* [Agent](/entities/foundational/agent.md) - a performer of action.
* [Relation](/entities/foundational/relation.md) - a connection between things.
* [Quality](/entities/foundational/quality.md) - a property or attribute.

## Core (L1 - general concepts, domain-neutral)

* [Artifact](/entities/core/artifact.md) - a created object that carries information or function.
* [Knowledge Artifact](/entities/core/knowledge-artifact.md) - an artifact whose purpose is knowledge.
* [Operational Artifact](/entities/core/operational-artifact.md) - an artifact that guides action.
* [Communicative Artifact](/entities/core/communicative-artifact.md) - an artifact meant to transfer a message.
* [Instructional Artifact](/entities/core/instructional-artifact.md) - an artifact meant to teach.
* [Asset](/entities/core/asset.md) - something of value.
* [Metric](/entities/core/metric.md) - a definition of measurement.
* [Workflow](/entities/core/workflow.md) - a repeatable sequence of activities.
* [Event](/entities/core/event.md) - a process at a place and time.
* [Person](/entities/core/person.md) - a human being.
* [Organization](/entities/core/organization.md) - a structured group of agents.
* [Software Agent](/entities/core/software-agent.md) - a computational performer.

## Domain (L2 - specialized entities, content genres)

* [Glossary](/entities/domain/glossary.md) - term-to-definition mapping.
* [Technical Document](/entities/domain/technical-document.md) - specification or reference documentation.
* [Help Article](/entities/domain/help-article.md) - user-facing how-to content.
* [Reference](/entities/domain/reference.md) - a pointer to a source.
* [Case Study](/entities/domain/case-study.md) - a narrative of a specific instance.
* [Email Message](/entities/domain/email-message.md) - a single email correspondence.
* [Playbook](/entities/domain/playbook.md) - a set of procedures for recurring situations.
* [Template](/entities/domain/template.md) - a fillable structural pattern.
* [Lesson](/entities/domain/lesson.md) - a single instructional unit.
* [Learning Module](/entities/domain/learning-module.md) - a grouping of lessons.
* [Training Program](/entities/domain/training-program.md) - a structured course of study.
* [Product](/entities/domain/product.md) - a created artifact offered for use or exchange.
* [Software Product](/entities/domain/software-product.md) - a product delivered as software.
* [Hardware Product](/entities/domain/hardware-product.md) - a product delivered as physical equipment.
* [Legal Document](/entities/domain/legal-document.md) - a document with legal effect or significance.
* [Policy](/entities/domain/policy.md) - a stated course or principle of action.
* [Knowledge Base](/entities/domain/knowledge-base.md) - a structured store of knowledge.
* [Knowledge Bundle](/entities/domain/knowledge-bundle.md) - a portable OKF knowledge artifact.
* [Country](/entities/domain/country.md) - a sovereign state.
* [Government Agency](/entities/domain/government-agency.md) - a state body that administers public functions.
* [Political Party](/entities/domain/political-party.md) - an organization that fields candidates for office.
* [Legislature](/entities/domain/legislature.md) - an assembly that makes laws.
* [Business Enterprise](/entities/domain/business-enterprise.md) - a for-profit organization.
* [Politician](/entities/domain/politician.md) - a person holding or seeking political office.
* [Election](/entities/domain/election.md) - an event in which offices are decided by vote.
* [Parliamentary Session](/entities/domain/parliamentary-session.md) - a sitting period of a legislature.
* [Foreign Relation](/entities/domain/foreign-relation.md) - a connection between states.
* [Machine Learning Algorithm](/entities/domain/machine-learning-algorithm.md) - a computational procedure that learns patterns from data.
* [Business Department](/entities/domain/business-department.md) - a functional unit within an organization.
* [Persona](/entities/domain/persona.md) - a fictional representation of a target user or customer segment.
* [Software System](/entities/domain/software-system.md) - a cohesive software product or platform.
* [Architecture Pattern](/entities/domain/architecture-pattern.md) - a reusable architectural solution template.
* [Security Control](/entities/domain/security-control.md) - a safeguard protecting confidentiality, integrity, availability.
* [Identity Provider](/entities/domain/identity-provider.md) - a system entity managing identity and authentication.
* [Software Development Lifecycle](/entities/domain/software-development-lifecycle.md) - the end-to-end process for building software.

## Application (L3 - specific types)

* [Online Program](/entities/application/online-program.md) - a training program delivered online.
* [SaaS Product](/entities/application/saas-product.md) - a software product delivered as a hosted service.
* [Internal Tool](/entities/application/internal-tool.md) - a software product for use inside an organization.
* [Agent Product](/entities/application/agent-product.md) - a product delivered by autonomous agents.
* [Unmanned Aerial Vehicle](/entities/application/unmanned-aerial-vehicle.md) - a pilotless powered aircraft.
* [Autonomous Agent](/entities/application/autonomous-agent.md) - a software agent that pursues goals independently.
* [Act](/entities/application/act.md) - a law enacted by a legislature.
* [Regulation](/entities/application/regulation.md) - a binding rule implementing a statute.
* [Treaty](/entities/application/treaty.md) - a binding agreement between states.
* [Bill](/entities/application/bill.md) - a draft law proposed to a legislature.
* [Startup](/entities/application/startup.md) - a young enterprise scaling a novel product.
* [Small and Medium Enterprise](/entities/application/small-and-medium-enterprise.md) - a business below large-corporation thresholds.
* [Global Corporation](/entities/application/global-corporation.md) - a large multi-country enterprise.
* [Educational Institution](/entities/application/educational-institution.md) - a school or university.
* [Armed Force](/entities/application/armed-force.md) - an organized military service of a state.
* [Supervised Learning](/entities/application/supervised-learning.md) - a machine learning paradigm learning from labeled data.
* [Unsupervised Learning](/entities/application/unsupervised-learning.md) - a machine learning paradigm discovering patterns in unlabeled data.
* [Reinforcement Learning](/entities/application/reinforcement-learning.md) - a machine learning paradigm maximizing rewards through interaction.
* [Deep Learning](/entities/application/deep-learning.md) - a machine learning subset using multi-layer neural networks.
* [Regression](/entities/application/regression.md) - a supervised learning task predicting continuous values.
* [Classification](/entities/application/classification.md) - a supervised learning task predicting categorical labels.
* [Clustering](/entities/application/clustering.md) - an unsupervised learning task grouping similar instances.
* [Model](/entities/application/model.md) - a trained machine learning artifact for prediction.
* [Marketing Department](/entities/application/marketing-department.md) - a department responsible for promotion and demand generation.
* [Finance Department](/entities/application/finance-department.md) - a department responsible for financial planning and accounting.
* [Operations Department](/entities/application/operations-department.md) - a department responsible for core process execution.
* [Human Resources Department](/entities/application/human-resources-department.md) - a department managing the employee lifecycle.
* [Risk Management Department](/entities/application/risk-management-department.md) - a department identifying and mitigating organizational risks.
* [Information Technology Department](/entities/application/information-technology-department.md) - a department managing technology infrastructure.
* [Product Department](/entities/application/product-department.md) - a department responsible for product strategy and development.
* [Sales Department](/entities/application/sales-department.md) - a department responsible for revenue generation.
* [Customer Success Department](/entities/application/customer-success-department.md) - a department ensuring customer outcomes and retention.
* [User Persona](/entities/application/user-persona.md) - a persona representing a typical end user.
* [Buyer Persona](/entities/application/buyer-persona.md) - a persona representing a decision-maker or purchaser.
* [Decision Maker](/entities/application/decision-maker.md) - a persona representing an authority for approvals.
* [Product User](/entities/application/product-user.md) - a persona representing an active product user.
* [Cloud Infrastructure](/entities/application/cloud-infrastructure.md) - computing infrastructure hosted by a cloud service provider.
* [On-Premise Infrastructure](/entities/application/on-premise-infrastructure.md) - computing infrastructure hosted on organizational premises.

# Implemented by

* [AI-Product-Manager](https://www.github.com/Yoseph-Zuskin/ai-product-manager) - public bundle curating product-management knowledge (type: Agent).
* AI Strategies for Business Transformations - private; concepts reference the classes above.
* AI-Driven Product Strategy - private; concepts reference the classes above.
