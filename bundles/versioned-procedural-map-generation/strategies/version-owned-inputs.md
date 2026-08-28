---
type: Strategy
title: Version-owned inputs
description: Load one immutable, confined input graph for each generator version before consuming random state.
tags:
  - versioning
  - templates
  - graphs
  - procedural-maps
sources:
  - id: owasp-path-traversal
    resource: https://owasp.org/www-community/attacks/Path_Traversal
    title: OWASP Path Traversal
---

# Version-owned inputs

## Problem

Replay fails when a version selects mutable shared configuration, when references can escape the intended snapshot, or when includes produce ambiguous or cyclic input graphs.

## Strategy

Treat each released version folder as an immutable replay unit. Resolve its root document first, then resolve every include and data reference relative to the document that declares it. Canonicalize each resolved location and reject it unless it remains confined to the selected version root. Reject absolute, missing, unreadable, or disallowed resource references before generation.

Manipulated relative or absolute paths can escape an intended root; validate and
normalize before file operations.[^owasp-path-traversal] Check confinement after
canonicalization, not by searching raw text for separators.

Load includes with an active traversal stack and a separate completed-resource set. Re-entering an active resource is a cycle and reports the path from its first active occurrence back to itself. Reusing a completed resource is not a cycle unless the schema forbids shared includes.

Parse configuration into a normalized application model. If a format treats
mapping-key order as non-semantic, the replay contract must define every
ordering that affects generation.

## Invariants

* The seed version is resolved before any version-owned input is loaded.
* Every replay-affecting resource belongs to the selected immutable version unit.
* References resolve relative to the declaring resource, are canonicalized, and remain confined to the selected version root.
* Missing, escaping, duplicate, malformed, or cyclic inputs fail before random state is consumed.
* Include-cycle diagnostics contain the complete active cycle path.
* Parsing and merging produce one validated, frozen snapshot before generation.
* Presentation details or unspecified mapping order never control replay behavior.

## Customization choices

The customization interview must ask about:

* Physical packaging of the immutable version unit: folder, archive, object store, database snapshot, or another boundary.
* Configuration syntax and versioned schema.
* Root-resource naming, include syntax, permitted resource kinds, and reference-base rules.
* Canonical identity rules, symbolic-link or alias treatment, case sensitivity, and platform portability.
* Duplicate identifiers, merge precedence, shared includes, and unknown fields.
* Snapshot immutability enforcement, publication, retention, migration, and integrity verification.
* Resource-size, include-depth, and graph-size limits.

## Alternatives and tradeoffs

* Fully self-contained documents reduce reference risk but can become difficult to maintain.
* Split version folders improve reuse inside one version but require explicit merge and cycle rules.
* Content-addressed resources make mutation detectable but add manifest and distribution complexity.
* Schema migration at load time can reduce authored versions, but the migration code then becomes version-owned replay behavior.

## Failure modes

* A shared mutable template changes old output without a generator-version change.
* A raw prefix check accepts a canonical path outside the version boundary.
* An include cycle recurses until a resource limit is reached and loses the cycle path.
* Merge order depends on mapping or directory enumeration.
* Random state is initialized before configuration validation, so an input error changes later consumption behavior.

[^owasp-path-traversal]: OWASP Path Traversal
