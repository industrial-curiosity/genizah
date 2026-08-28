---
type: Validation
title: AI agent skill installation validation
description: Portable acceptance scenarios for explicit project-contained destination selection and complete skill installation.
tags:
  - agent-skills
  - agent-installation
  - ai-agents
sources:
  - id: agent-skills
    resource: https://agentskills.io
    title: Agent Skills
---

# AI agent skill installation validation

## Scope

These scenarios test destination choice, containment, reuse, reporting, and transaction outcomes without prescribing a host, programming language, package manager, user interface, or filesystem API. Agent Skills provides the portable skill format context for these scenarios.[^agent-skills]

## Scenario: Default project-level location

### Given

A project with no prior installer-owned skill location and an interactive user who accepts the default.

### When

The installer runs.

### Then

It writes the complete skill set only below the documented default project-level location and reports that location and the next prompt.

## Scenario: Selected project-level location

### Given

A project with no prior installer-owned skill location and an interactive user who selects a listed compatible project-level location.

### When

The installer runs.

### Then

It writes the complete skill set only below the selected location and leaves the default location untouched.

## Scenario: Noninteractive override

### Given

A project and an explicit contained relative destination override.

### When

The installer runs without interactive input.

### Then

It writes the complete skill set only below that destination and reports the selected location.

## Scenario: Repeat installation

### Given

A project containing the expected installer-owned skill identity in one supported project-level location and no explicit override.

### When

The installer runs again.

### Then

It reuses that location, updates only installer-owned skill content according to its replacement policy, and does not write a second location.

## Scenario: Invalid path

### Given

An absolute destination or a relative destination that resolves outside the current project.

### When

The installer validates the requested location.

### Then

It fails before writing skill files and reports the rejected location and containment requirement.

## Scenario: No partial installation

### Given

A selected valid destination and an installation that fails during staging, validation, or replacement.

### When

The installer handles the failure.

### Then

No partially installed skill directory remains, and any installer-owned content moved during the invocation is restored.

[^agent-skills]: Agent Skills
