---
type: Specification
title: Versioned procedural map generation specification
description: Portable requirements for deterministic procedural maps whose replay-affecting algorithms and inputs belong to immutable generator versions.
tags:
  - deterministic-generation
  - procedural-maps
  - seeded-randomness
  - versioning
  - templates
  - graphs
sources:
  - id: pcg-paper
    resource: https://www.pcg-random.org/paper.html
    title: The PCG Paper
  - id: owasp-path-traversal
    resource: https://owasp.org/www-community/attacks/Path_Traversal
    title: OWASP Path Traversal
  - id: nist-breadth-first
    resource: https://xlinux.nist.gov/dads/HTML/breadthfirst.html
    title: NIST Dictionary of Algorithms and Data Structures breadth-first search
  - id: nist-depth-first
    resource: https://xlinux.nist.gov/dads/HTML/depthfirst.html
    title: NIST Dictionary of Algorithms and Data Structures depth-first search
---

# Versioned procedural map generation

## Purpose

Define a portable contract for generating ordered map topology from a caller-provided seed while preserving old results after new generator versions are introduced.

## Inputs

* A seed value containing both entropy and a generator-version identifier.
* A registry that resolves each supported generator version to one immutable replay unit.
* Version-owned configuration, templates, shapes, selectors, transforms, layer rules, connector rules, and random algorithm.
* A caller request identifying which generated features and reachability conditions are required.

Configuration syntax must not make presentation-only ordering semantic. If a
format treats mappings as unordered, define every ordering that affects
generation.

## Outputs

* The normalized seed and selected generator version.
* An ordered generated-map result containing its layers or regions, placed features, connectors, and explicit start location.
* Stable identifiers sufficient to compare the ordered result with replay test vectors.
* One diagnosable failure when a required precondition or generation invariant cannot be satisfied.

The contract defines logical map topology. It does not require a particular programming language, random-number library, serialization syntax, coordinate representation, grid storage, or package format.

## Invariants

* A seed carries entropy plus a generator version; entropy alone is not a replay identity.
* The selected version owns every replay-affecting input and algorithm, including random-number generation, bounded-value conversion, state-consumption order, normalization, matching, ordering, placement, and reachability rules.
* An unknown seed version fails before configuration or other version-owned inputs are loaded.
* Every referenced input is resolved inside the selected version boundary. Missing or escaping references fail before generation; canonicalization and confinement prevent traversal outside that boundary.[^owasp-path-traversal]
* Configuration is completely loaded, normalized, validated, and frozen before random state is consumed.
* Include and template-composition graphs are acyclic. A cycle reports its full active path; depth-first traversal can maintain that path portably.[^nist-depth-first]
* Every candidate list is filtered and placed into a documented stable order before random selection.
* Shapes, permitted transforms, layers or regions, selectors, placements, and connectors are data-defined rather than assigned hidden domain meaning by the engine.
* Only transforms enabled for a shape may be applied, and transformed occupied cells and anchors are evaluated together.
* Connector relationships become explicit graph edges. Required reachability is evaluated from an explicit start location across navigable adjacency and connector edges; breadth-first traversal is one portable way to visit neighbors before more distant vertices.[^nist-breadth-first]
* Executing a caller-provided seed attempts that seed once. Failure does not silently allocate, substitute, or retry with another seed.
* A released replay version is immutable. A behavior change uses a new version so prior version mappings remain replayable.

## Customization points

An adopting agent must ask about and record each applicable choice:

* Seed representation, entropy range, version range, parsing rules, and whether a separate allocator is required.
* Pseudo-random algorithm, identity, bounded-selection method, state model, and replay-vector format. Identify its state transition and output function.[^pcg-paper]
* Version registry and immutable replay-unit packaging, such as directories, archives, database records, or content-addressed objects.
* Configuration syntax, schema, include mechanism, reference semantics, normalization rules, and frozen in-memory representation.
* Map topology, coordinate model, layer or region model, shapes, anchors, enabled transforms, occupancy rules, and placement constraints.
* Selector vocabulary, matching policy, stable comparison rule, duplicate handling, and empty-candidate policy.
* Connector representation, navigable adjacency, start-location policy, required-reachability scope, and unreachable-output policy.
* Output ordering, identity fields, diagnostics, observability, persistence, resource limits, and failure taxonomy.

Choices may specialize the model, but they cannot silently weaken an invariant. An intentional departure is documented as a deviation with corresponding acceptance scenarios.

## Generation flow

1. Parse the caller seed without consuming random state.
2. Resolve its generator version or fail before loading version-owned input.
3. Load every referenced input through the selected version boundary, rejecting missing, escaping, duplicate, or cyclic references.
4. Normalize and freeze one configuration snapshot.
5. Validate schemas, identifiers, ranges, selectors, shapes, enabled transforms, connector rules, template references, and graph acyclicity.
6. Initialize the version-owned random algorithm from the seed entropy.
7. Enumerate eligible layers, layouts, templates, transforms, and placements in their documented stable orders; consume random state only at specified decision points.
8. Expand selected templates, transform shapes and anchors, reject invalid occupancy, and add explicit connector edges.
9. Build the navigability graph and validate every required vertex from the explicit start location.
10. Return the ordered result, or return the single failure for this caller-seed attempt.

## Failure behavior

Pre-generation failures include a malformed seed, unknown version, missing or escaping reference, invalid schema, duplicate identifier, include cycle, template cycle, unknown template reference, invalid shape or anchor, and invalid connector rule. They occur before random consumption whenever the invalidity can be known from the frozen configuration.

Generation failures include no eligible candidate, out-of-bounds or overlapping placement, unsatisfied required feature, invalid start location, and unreachable required topology. A failure identifies the seed version and a stable reason without returning a partial successful map.

A seed allocator, retry loop, or history service is a separate caller concern. The generation operation never converts failure of a supplied seed into success with a different seed.

## Replay evidence

Separately initialized generators can reproduce a sequence from the same seed,
but runtime changes can alter that sequence. Therefore the generator version
owns the effective random-algorithm behavior.

Replay conformance fixes the version-owned input snapshot, algorithm identity,
candidate ordering, and random-consumption schedule, then compares complete
ordered output with versioned test vectors.

[^pcg-paper]: The PCG Paper
[^owasp-path-traversal]: OWASP Path Traversal
[^nist-breadth-first]: NIST Dictionary of Algorithms and Data Structures breadth-first search
[^nist-depth-first]: NIST Dictionary of Algorithms and Data Structures depth-first search
