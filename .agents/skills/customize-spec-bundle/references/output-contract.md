---
type: Guide
title: Customization output contract
description: Required structure for a target implementation profile and customized specification draft.
tags:
  - specification-customization
  - output-contract
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification
---

<!-- markdownlint-disable MD025 -->

# Customization output contract

## Target implementation profile

### Discovered facts

Record evidence-backed facts from the target repository and supplied context.

### User decisions

Record choices the user explicitly made during the interview.

### Bundle invariants retained

List applicable source-bundle invariants that remain in force.

### Deliberate deviations

Record every rejected or weakened invariant with rationale and provenance.

### Unresolved questions

List blockers and unanswered choices without inventing a resolution.

## Customized specification draft

### Purpose

State the target-specific outcome.

### Target environment

Describe the applicable language, runtime, integrations, and persistence.

### Requirements

State retained and target-specific requirements.

### Selected strategies

Name the selected bundle strategies and target adaptations.

### Failure behavior

Define expected failures, handling, and recovery policy.

### Acceptance scenarios

List verifiable target scenarios derived from source validation.

### Provenance

Link each material choice and deviation back to its source bundle.
