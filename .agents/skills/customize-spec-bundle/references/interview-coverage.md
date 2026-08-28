---
type: Guide
title: Customization interview coverage
description: A portable checklist for turning a specification bundle into an evidence-backed target implementation profile.
tags:
  - specification-customization
  - interviews
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification
---

<!-- markdownlint-disable MD025 -->

# Interview coverage

Read discoverable target-repository facts before asking the user. Inspect the
relevant code, configuration, documentation, and tests, then record each fact
with its evidence separately from a user decision.

Extract the bundle invariants, customization choices, alternatives, failure
conditions, and validation scenarios into an adaptation checklist. Ask one
unresolved question at a time; do not ask for a fact that is discoverable from
the target context.

Implementation samples are optional supporting material, not checklist items.
Do not treat sample code or sample tests as requirements, validation scenarios,
or evidence that a target conforms. Use them only as clearly labeled
illustrations when they help resolve a target-specific implementation choice.

## Applicable domains

Cover these topics only when relevant to the bundle and target: domain;
language and runtime; integration; data and persistence; determinism and
compatibility; security; scale and performance; operations; failure policy;
testing; and excluded scope.

## Completion criteria

Stop only when every applicable customization point has one of these recorded
outcomes: a recorded fact, a user decision, an explicit deviation, or an
unresolved blocker. Preserve unresolved blockers when the user stops answering;
do not invent a target choice.
