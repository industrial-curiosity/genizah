---
type: Strategy
title: Template composition and selection
description: Validate recursive template graphs and choose eligible templates from a stable ordinal order.
tags:
  - templates
  - graphs
  - deterministic-generation
  - procedural-maps
sources:
  - id: nist-depth-first
    resource: https://xlinux.nist.gov/dads/HTML/depthfirst.html
    title: NIST Dictionary of Algorithms and Data Structures depth-first search
---

# Template composition and selection

## Problem

Reusable templates need composition and conditional selection, but unchecked recursion, ambiguous matching, or unstable candidate order can make generation fail late or replay inconsistently.

## Strategy

Represent feature and layout composition as one directed graph whose vertices are stable template identifiers and whose edges are child-template references. Validate that every target exists and that the combined graph is acyclic before generation.

Use depth-first search with unvisited, active, and complete states. It explores a
vertex's outgoing edges before its siblings.[^nist-depth-first] An edge to an
active vertex reports the active-stack slice plus that vertex; an edge to a
complete vertex is safe reuse, not recursion.

For selection, evaluate every selector against normalized map facts, layer or region roles, feature tags, and other version-owned context. A selector matches only when all of its defined clauses succeed. Collect matching candidates without consuming random state, sort them by a documented ordinal comparison of stable identifiers, and then use one version-owned random decision to select from that ordered list.

## Invariants

* The combined composition graph contains only known template identifiers and is acyclic before generation.
* Cycle failure includes the traceable closed path, not only the repeated identifier.
* Selector semantics, normalization, and empty-clause behavior belong to the generator version.
* Candidate filtering consumes no random state.
* Matching candidates are sorted by the version's documented ordinal identifier comparison before random selection.
* Recursive expansion order is stable and does not depend on map, set, or filesystem enumeration.
* No eligible candidate is an explicit failure unless the customized specification defines that selection as optional.

## Customization choices

The customization interview must ask about:

* Template kinds and which cross-kind composition edges are permitted.
* Selector vocabulary, Boolean semantics, normalization, inheritance, and missing-value behavior.
* Stable identifier syntax, ordinal comparison, duplicate policy, and namespace rules.
* Candidate weights, uniform versus weighted selection, and bounded-random conversion.
* Parent-child offset, transform, layer/region, and override semantics.
* Maximum graph size, expansion depth, repeated-subgraph policy, and diagnostic detail.
* Optional selections and the meaning of an empty candidate list.

## Alternatives and tradeoffs

* Pre-validating the full graph gives early complete failures but may inspect templates unused by one request.
* Lazy validation can reduce startup work but lets malformed released inputs fail only for particular seeds.
* Uniform choice is easy to replay; weighted choice is equally valid when weight normalization and boundary behavior are versioned.
* Reusable directed acyclic graphs avoid duplication, while copying templates simplifies traversal at the cost of maintenance drift.

## Failure modes

* Separate feature and layout checks miss a cycle that crosses template kinds.
* A visited-only traversal mistakes shared subgraphs for cycles or fails to identify the active cycle path.
* Selector evaluation iterates an unordered catalog and changes random index meaning.
* Locale-aware sorting changes candidate order between environments.
* Invalid references are discovered only after random state has been consumed.

[^nist-depth-first]: NIST Dictionary of Algorithms and Data Structures depth-first search
