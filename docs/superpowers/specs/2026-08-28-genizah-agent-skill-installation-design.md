---
type: Design
title: Genizah Agent Skill Installation
description: Design for a minimal npm installer, GitHub-backed bundle discovery, and confirmed bundle customization.
tags:
  - ai-agents
  - agent-skills
  - npm
  - specification-bundles
sources:
  - id: panopticon-bootstrap
    resource: https://github.com/industrial-curiosity/panopticon-ay-eye/blob/main/panopticon/bootstrap.py
    title: Panopticon bootstrap installer
  - id: panopticon-agent-skills-support
    resource: https://github.com/industrial-curiosity/panopticon-ay-eye/blob/main/docs/agentskills-support.md
    title: Panopticon Agent Skills support matrix
---

# Genizah Agent Skill Installation Design

## Purpose

Let a project install Genizah agent skills with `npx genizah init`. The
installed skill searches the GitHub-hosted Genizah catalog, recommends a bundle
from the target project's context, waits for the user's selection, and starts
the existing customization interview.

## Goals

- Install only the skills required for discovery and customization.
- Prompt for a compatible project-level skill directory before writing files.
- Use the catalog's committed `tags/` tree for deterministic search.
- Return JSON from search for agent consumption.
- Keep the npm package self-contained under `tooling/npm/` and dependency-free
  at runtime.
- Fetch only the selected bundle concepts needed during customization.

## Non-goals

- Cloning or vendoring the catalog into a target project.
- Maintaining a catalog snapshot in the npm package.
- Automatically selecting or customizing a bundle without user confirmation.
- Supporting user-profile skill directories in the first iteration.

## Installation bundle

Create `bundles/ai-agent-skill-installation/`.
It contains a core specification, a location-selection strategy, acceptance
scenarios, and `references/agentskills-support.md` derived from Panopticon's
agent-skill support document.

The specification requires an installer to:

- Choose the destination before writing skill files.
- Offer documented project-level locations, with `.agents/skills` first.
- Accept an explicit noninteractive destination override.
- Reuse a prior Genizah installation location when no override is supplied.
- Make no implicit copy to a second skill directory.
- Restrict destination paths to relative paths contained by the current project.
- Report the chosen location and the exact prompt that starts the installed
  skill.


## Npm package

Create a self-contained package in `tooling/npm/` with a `genizah` executable.
It uses Node's standard library and declares no runtime dependencies. At
installation time it fetches the two skill trees from the GitHub catalog:

- `genizah`, which orchestrates discovery, recommendation,
  confirmation, and customization.
- `customize-spec-bundle`, including its linked reference documents.

`npx genizah init` runs in the target project. `--skills-dir RELATIVE_PATH`
selects a destination without prompting. Without that option, `init` first
finds an existing Genizah installation location, then prompts with the supported
project-level paths. A blank response selects `.agents/skills`.

The command rejects absolute paths and paths resolving outside the current
project. It fetches and validates both skill trees before writing them below the
one selected directory, then prints the agent prompt to begin discovery.

Before the catalog is available remotely, a local development command supports
testing installation from another project checkout:

```sh
npm --prefix ../genizah/tooling/npm run local:init -- .
```

The command resolves the target argument from the invoking project's directory
and derives the catalog root from the script's own location. It reads the same
skill paths directly from that local checkout, makes no network request, and
uses the normal location-selection and transactional-installation behavior.
The installed local skill invokes `local:search` from that checkout instead of
`npx`, so discovery remains usable before publication.

## Search contract

`npx --yes genizah search TERM...` reads the committed tag tree in
`industrial-curiosity/genizah` from GitHub. It does not clone the repository or
write to the current project. It emits JSON only to standard output.

For every normalized lowercase query term, a bundle receives one match at most:

- A full match occurs when the term equals one of the bundle's tags.
- A partial match occurs when the term is contained by one of the bundle's tags
  and no full match exists for that term.

The command ranks candidates by weighted score (full match = 2, partial match =
1), then matched-term count, then full-match count, then bundle ID using ordinal
string comparison. JSON includes the normalized terms and each candidate's
bundle ID, title, description, tags, full matches, partial matches, matched-term
count, and score.

The command fails clearly when the catalog's tag index or a referenced tag page
cannot be read or parsed. It does not substitute another catalog source.

## Installed skill workflow

The discovery skill accepts a target-project path and a user request. It
inspects target-project facts, derives search terms, and calls `npx --yes
genizah search`. It shows the ranked candidates and recommends one based on the
observed target context plus candidate descriptions.

It then waits for the user to select or confirm a bundle. Only after that
confirmation does it load the selected bundle's index and the concepts needed by
the `customize-spec-bundle` workflow from the GitHub catalog. It uses those
concepts to start the existing one-unresolved-question-at-a-time customization
interview. The recommendation never replaces confirmation.

## Failure behavior

- An invalid destination fails before writing skill files.
- An interrupted copy leaves no partially installed skill directory.
- A failed catalog request identifies the requested catalog path and does not
  use stale or alternative data.
- No matching bundles returns a valid empty-candidate JSON response.
- A missing selected bundle stops customization before project-specific choices
  are collected.

## Acceptance scenarios

- A default interactive installation writes both skills only under
  `.agents/skills`.
- A selected compatible location receives both skills and the default location
  remains untouched.
- A noninteractive relative override selects one location; absolute and escaping
  overrides fail without writes.
- A local development installation from another project uses the local catalog
  checkout and makes no network request.
- The same catalog tag tree and query terms produce byte-identical JSON output.
- Full tag matches outrank otherwise equivalent partial matches.
- The agent asks for user confirmation after recommendation and before loading a
  selected bundle for customization.
- The agent starts customization using only the confirmed bundle's required
  catalog concepts.
