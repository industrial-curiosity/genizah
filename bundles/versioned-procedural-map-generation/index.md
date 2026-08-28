---
okf_version: "0.2"
---

# Versioned Procedural Map Generation

A specification for deterministic, replayable procedural map generation with version-owned inputs.

## Authors

* @therightstuff
* industrial-curiosity

## Tags

* deterministic-generation
* procedural-maps
* seeded-randomness
* maps
* seeds
* procedural
* determinism
* versioning
* generation
* templates

## Specifications

* [Core specification](specification.md) - Defines portable requirements, invariants, customization points, generation flow, and failure behavior.

## Validation

* [Acceptance scenarios](validation.md) - Defines portable Given/When/Then checks for replay, version ownership, safe inputs, deterministic selection, placement, and failure behavior.

## Strategies

* [Deterministic replay](strategies/deterministic-replay.md) - Preserves replay by versioning the random algorithm, stabilizing state consumption and candidate ordering, and maintaining test vectors.
* [Version-owned inputs](strategies/version-owned-inputs.md) - Keeps replay-affecting input graphs immutable, relative, confined, validated, and cycle-free.
* [Template composition and selection](strategies/template-composition-and-selection.md) - Validates acyclic template graphs and selects matching candidates in a stable order.
* [Placement and reachability](strategies/placement-and-reachability.md) - Applies data-defined shapes and connectors while validating required graph reachability from an explicit start.
