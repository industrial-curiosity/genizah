---
type: Strategy
title: Placement and reachability
description: Place transformed data-defined shapes, construct connector edges, and validate required topology from an explicit start.
tags:
  - procedural-maps
  - maps
  - generation
  - graphs
sources:
  - id: nist-breadth-first
    resource: https://xlinux.nist.gov/dads/HTML/breadthfirst.html
    title: NIST Dictionary of Algorithms and Data Structures breadth-first search
---

# Placement and reachability

## Problem

A generated map can satisfy local placement rules yet remain globally unusable when transformed shapes overlap, connectors do not create intended adjacency, or required features cannot be reached from the start.

## Strategy

Define each shape as a set of occupied logical positions relative to a named anchor. A transform maps the occupied positions and anchor together. Enumerate only transforms enabled by the template, normalize transformed positions, and validate bounds, blocked space, occupancy, adjacency, and other placement constraints before committing a candidate.

Keep logical occupancy independent of storage. A grid, sparse set, navigation
mesh, or room graph conforms when it exposes equivalent positions, adjacency,
occupancy, and connector relationships.

Represent traversable adjacency and placed connectors as graph edges. Validate
the start before traversal, then compare visited vertices with required
vertices or features. Breadth-first search visits neighbors before more distant
vertices and is a portable reachability method, not a grid-storage requirement.[^nist-breadth-first]

## Invariants

* Shapes, anchors, permitted transforms, placement constraints, layers or regions, and connector relationships are data-defined.
* A disabled transform is never considered or applied.
* Occupied positions and the anchor undergo the same transform.
* A committed placement is in bounds, respects blocked space, and does not violate occupancy or other configured constraints.
* Connector edges exist only for placed connectors and their configured endpoint relationships.
* Reachability starts at one explicit, valid location and traverses both ordinary navigable adjacency and connector edges.
* Every configured required feature or vertex is reachable, or the caller-seed attempt fails once without returning a partial success.

## Customization choices

The customization interview must ask about:

* Coordinate, region, and dimensional model, including whether boundaries wrap.
* Shape and anchor syntax, transform set, normalization, and transform ordering.
* Blocked-space, occupancy, overlap, adjacency, clearance, and placement-priority rules.
* Connector shape, directionality, capacity, endpoint constraints, layer spans, and traversal cost.
* Start-location selection and whether it consumes random state.
* Required-reachability scope: every open position, every layer or region, selected features, or another set.
* Traversal direction, movement rules, conditional edges, resource limits, and unreachable-output policy.

## Alternatives and tradeoffs

* Dense grids simplify local collision checks; sparse or graph models can better fit irregular spaces.
* Validating after all placement gives a complete topology view; incremental connectivity checks may reject bad branches earlier but add version-owned decision behavior.
* Breadth-first and depth-first traversals both establish unweighted reachability; breadth-first additionally exposes hop layers when shortest unweighted distance matters.
* Backtracking can rescue a failed placement, but retry order and random consumption must then be versioned.

## Failure modes

* The anchor is transformed differently from occupied positions.
* A transform omitted from configuration is applied as a hidden default.
* Occupancy tracks only bounding boxes and rejects or accepts irregular masks incorrectly.
* A connector is rendered but no graph edge is added, or an edge is added without a placed connector.
* Traversal begins from an implicit or invalid start and falsely reports success.
* Unreachable required features trigger an internal retry that silently changes the caller's seed outcome.

[^nist-breadth-first]: NIST Dictionary of Algorithms and Data Structures breadth-first search
