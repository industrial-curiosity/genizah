---
type: Strategy
title: Project location selection
description: Select one compatible project-level skill location before installation while keeping user-profile locations out of implicit selection.
tags:
  - agent-skills
  - agent-installation
  - ai-agents
sources:
  - id: agent-skills
    resource: https://agentskills.io
    title: Agent Skills
---

# Project location selection

## Problem

Agent hosts discover skills from different project-relative paths, while user-profile paths have a broader and less visible effect. An installer that selects a location after writing, or writes to several locations, can surprise the project owner and create divergent copies.

## Strategy

1. Publish the supported project-level locations in a stable order, with the portable default first.
2. If an explicit relative override is supplied, validate its containment and select it without prompting.
3. Otherwise, look for one prior installer-owned skill identity in the published project-level order and reuse the first match.
4. Otherwise, show the project-level choices and let the user accept the default, select a listed option, or provide a contained relative path.
5. Validate the final path before staging or copying skill content.
6. Install only into the final selected location and report that location after a successful transaction.

The selected location list is project-level and ordered; user-profile locations remain outside implicit selection.[^agent-skills]

## Invariants

* The compatibility list is ordered, de-duplicated, and limited to project-level locations.
* One invocation has one destination decision.
* No write occurs until destination validation succeeds.
* A prior installation is reused only when its expected identity confirms installer ownership.
* User-profile locations require an explicit, separately designed workflow if they are supported at all.

## Alternatives and tradeoffs

Writing every compatible location can improve discovery coverage but creates duplicate state and makes replacement, rollback, and ownership ambiguous. Selecting one location requires a prompt or override but gives the project owner a visible, reversible decision. User-profile installation can serve several projects, but its broader scope makes it unsuitable for implicit project installation.

## Failure modes

* An absolute or escaping path could write outside the project if containment is not checked after resolution.
* A stale or unrelated directory could be overwritten if ownership is inferred from its location alone.
* Multiple writes could leave hosts reading different skill revisions.
* A failed copy could leave a partial skill directory without staging and rollback.

[^agent-skills]: Agent Skills
