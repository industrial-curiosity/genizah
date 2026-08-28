---
type: Specification
title: AI agent skill installation specification
description: Portable requirements for selecting one project-contained skill destination before installing reusable agent skills.
tags:
  - agent-skills
  - agent-installation
  - ai-agents
sources:
  - id: agent-skills
    resource: https://agentskills.io
    title: Agent Skills
---

# AI agent skill installation

## Purpose

Define a portable contract for an installer that makes reusable agent skills available to a project without making an implicit or unsafe destination choice.

## Inputs

* A current project root.
* Packaged or otherwise identified skill content.
* An optional noninteractive override naming a destination relative to the project root.
* Interactive input when no override or reusable prior installation determines the destination.

## Requirements

* The installer chooses a destination before writing skill files.
* Each installation invocation writes to one selected destination only.
* The default project-level location is documented and offered first among supported project-level locations.
* A noninteractive override selects one relative destination without prompting.
* Without an override, the installer reuses a prior installation location when that location contains the expected installed-skill identity.
* Every selected destination is a relative path that resolves inside the current project; absolute and escaping paths fail before any write.
* The installer distinguishes project-level locations from user-profile locations and does not select a user-profile location implicitly.
* The installer preserves unrelated content already present at the selected destination.
* A failed installation leaves no partially installed skill content and restores any replaced installer-owned content.
* On success, the installer reports the selected location, installed skill identities, and the exact next prompt that begins use of the installed skills.

The Agent Skills format supplies the interoperable skill concept; this specification does not require a particular host, language, package manager, filesystem API, or user interface.[^agent-skills]

## Customization choices

An adopting agent must ask about and record each applicable choice:

* Supported project-level locations and their displayed order.
* The default location, prior-installation identity, and reuse precedence.
* Interactive selection format, cancellation behavior, and the form of an explicit override.
* Ownership checks, replacement policy, rollback boundary, and report format.
* The installed skill set, its identity marker, and the prompt that starts its workflow.

Choices may add compatible locations or reporting detail, but they cannot weaken choice-before-write, containment, single-destination, or rollback requirements.

## Failure behavior

An invalid, absolute, or escaping destination fails before writing skill files. An ambiguous or unrelated pre-existing skill directory stops installation before replacement. A copy, validation, or replacement failure removes newly installed content and restores installer-owned content moved during the same invocation. Each failure identifies the rejected destination or installation stage and the action required to proceed.

[^agent-skills]: Agent Skills
