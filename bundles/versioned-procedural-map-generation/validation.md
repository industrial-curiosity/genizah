---
type: Validation
title: Versioned procedural map generation validation
description: Portable acceptance scenarios for deterministic replay, safe version-owned inputs, template selection, placement, reachability, and caller-seed failure.
tags:
  - deterministic-generation
  - procedural-maps
  - determinism
  - versioning
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification
---

# Versioned procedural map generation validation

## Scope

These scenarios test observable behavior without prescribing a language, framework, random library, serialization syntax, filesystem layout, or map storage structure. OKF defines `sources` as provenance and claim-level footnote IDs as joins to those sources; this document uses that structure to preserve the origin of its validation contract.[^okf-spec]

## Scenario: Same-version replay

### Given

A fixed generator version, seed entropy, immutable input snapshot, random algorithm, state-consumption schedule, and requested output.

### When

The caller executes generation twice in independently initialized contexts.

### Then

Both executions return the same complete ordered output, including selected templates, transforms, placements, connectors, start location, and topology.

## Scenario: Intentional version change

### Given

An older released version with a retained replay vector and a newer version that intentionally changes replay-affecting behavior.

### When

Both versioned seeds are executed against their respective immutable replay units.

### Then

The newer version may produce different output, while the older version still reproduces its original ordered output.

## Scenario: Unknown seed version

### Given

A well-formed seed naming a generator version absent from the version registry.

### When

The caller executes generation.

### Then

Generation fails with an unknown-version reason before loading configuration or any other version-owned input and before consuming random state.

## Scenario: Escaping or missing input reference

### Given

A selected version whose input graph contains either a reference that canonicalizes outside its version boundary or a reference to a missing resource.

### When

The configuration snapshot is loaded.

### Then

Loading fails before generation and identifies the declaring resource and rejected reference without reading an escaping target.

## Scenario: Include cycle

### Given

An include graph containing a cycle across two or more resources.

### When

The selected version is validated.

### Then

Validation fails before random-state initialization and reports the closed include-cycle path from the repeated resource back to itself.

## Scenario: Template-composition cycle

### Given

A combined feature and layout template graph containing a recursive cycle.

### When

The selected version is validated.

### Then

Validation fails before random-state initialization and reports the closed template-cycle path, including cycles that cross template kinds.

## Scenario: Stable selector candidate order

### Given

Multiple templates that match the same selector facts but are supplied in different physical enumeration orders.

### When

Generation reaches the selection point with the same version and random state.

### Then

Both executions order candidates with the version's documented ordinal comparison before selection and choose the same template.

## Scenario: Disabled transform

### Given

A shape supports several transform operations in the generator, but its template enables only a strict subset.

### When

Candidate placements are enumerated.

### Then

No disabled transform is applied or consumes random state, even if it would create a valid placement.

## Scenario: Unreachable required feature

### Given

A completed candidate topology with a valid explicit start location and at least one configured required feature outside the reachable graph.

### When

Reachability validation traverses ordinary adjacency and placed connector edges.

### Then

The caller-seed attempt returns one generation failure identifying the unreachable requirement and does not return a partial successful map.

## Scenario: Invalid caller-provided seed

### Given

A caller supplies a malformed seed or a valid seed whose single generation attempt cannot satisfy the required constraints.

### When

The caller executes generation.

### Then

Generation returns that seed's failure without allocating, substituting, or retrying with another seed.

## Conformance record

A conforming implementation records the generator version and stable replay vector used for each applicable scenario. Implementation-specific tests may add stronger checks, but they cannot replace or weaken these portable outcomes.

[^okf-spec]: Open Knowledge Format specification
