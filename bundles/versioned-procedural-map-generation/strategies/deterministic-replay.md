---
type: Strategy
title: Deterministic replay
description: Preserve ordered generation results by versioning the random algorithm, state-consumption schedule, and candidate ordering together.
tags:
  - deterministic-generation
  - seeded-randomness
  - determinism
  - versioning
sources:
  - id: pcg-paper
    resource: https://www.pcg-random.org/paper.html
    title: The PCG Paper
---

# Deterministic replay

## Problem

A seed does not preserve a generated map when the random algorithm, candidate enumeration, or number and order of random draws can change independently.

## Strategy

Give each released generator version an immutable random contract:

1. Name the exact pseudo-random algorithm and all parameters that affect its transition and output functions.
2. Define how seed entropy initializes algorithm state and how bounded integers or weighted choices are derived.
3. Define every decision point that consumes state, including decisions whose candidate count is one.
4. Filter candidates without consuming random state, then sort identifiers with a documented ordinal comparison before selecting an index.
5. Preserve versioned replay vectors containing the seed, immutable input identity, expected random decisions, and complete ordered output.

An algorithm identity includes its state transition and output function, not
only a product name.[^pcg-paper]

Equal seeds can reproduce a sequence, but a runtime change can alter that
sequence. A runtime generator is replay-safe only when its effective behavior
belongs to the generator version.

## Invariants

* Generator version and seed entropy are both part of replay identity.
* Algorithm identity, initialization, bounded-selection behavior, and state-consumption order cannot change within a released version.
* Candidate enumeration has a stable total order before every random selection.
* Unordered containers, locale-sensitive comparisons, concurrent completion order, and filesystem enumeration do not determine output order.
* The complete ordered result—not only aggregate counts or a final hash—is reproducible for each retained test vector.

## Customization choices

The customization interview must ask about:

* Random algorithm and whether it must be portable across languages or runtimes.
* Seed entropy size, encoding, normalization, and invalid-seed policy.
* Ordinal identifier representation and tie/duplicate handling.
* Whether single-candidate choices consume random state.
* Parallelism boundaries and the deterministic merge order for parallel work.
* Replay-vector contents, storage, retention, and compatibility gates.
* Whether output serialization is part of replay or only the logical ordered model is compared.

## Alternatives and tradeoffs

* Recording every random draw can help diagnosis but increases storage and couples tests tightly to internal decisions.
* Comparing only final output permits internal refactoring, but a mismatch reveals less about the first diverging decision.
* A custom portable algorithm can stabilize behavior across runtimes, while a platform generator may be simpler but requires pinning its effective implementation to the version.
* Independent random substreams can isolate changes, but their derivation and consumption rules become additional version-owned behavior.

## Failure modes

* A stable seed with a changed algorithm produces a different map under the same claimed version.
* Adding an eligible candidate changes later choices because enumeration or state consumption was not fixed.
* A set, map, directory, locale, or race supplies nondeterministic candidate order.
* A retry after placement failure consumes extra random values without appearing in the version contract.
* A replay test compares only membership and misses an ordered-output regression.

[^pcg-paper]: The PCG Paper
