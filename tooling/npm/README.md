# Genizah CLI

## Overview

Genizah is a catalog of self-contained specification bundles: algorithms,
strategies, and acceptance scenarios that an AI agent can adapt to a concrete
implementation. The CLI installs the `genizah` and
`customize-spec-bundle` skills into your project; bundles stay in the catalog
until you choose one.

## Example

Install the skills in the project where you want to use a bundle, then ask your
agent to find and integrate one:

```text
Use the genizah skill to search for a spec bundle that does
<whatever you're thinking of> for this project and integrate the bundle I
confirm.
```

The skill inspects the project, recommends a bundle, and waits for your
confirmation before it starts customization.

## Installation

Install the Genizah discovery and customization skills in a project:

```sh
npx --yes genizah init
```

The command lets you select one project-level skill location. It defaults to
`.agents/skills` and also supports `.github/skills`, `.claude/skills`,
`.cursor/skills`, `.codex/skills`, `.opencode/skills`, and `.pi/skills`.
Pass `--skills-dir RELATIVE_PATH` to select a contained project path without a
prompt.

If a target skill directory belongs to another tool, `init` leaves it unchanged
and tells you which directory blocked installation. Re-run with `--force` (or
`-f`) only when you intend to replace that directory:

```sh
npx --yes genizah init --force
```

Before the catalog is published, install from a local Genizah checkout while
standing in the target project:

```sh
npm --prefix ../genizah/tooling/npm run local:init -- .
```

`local:init` resolves `.` from the invoking directory, reads the skills from
that checkout, and makes no network request. It accepts the same `--skills-dir`
`--force`, and `-f` options as `init`. The installed `genizah` skill uses the
local catalog for discovery:

To replace a conflicting target skill directory during local development, use
the same force flag as the published command:

```sh
npm --prefix ../genizah/tooling/npm run local:init -- . --force
```

```sh
npm --prefix ../genizah/tooling/npm run local:search -- procedural maps
```

Search the GitHub-hosted catalog with JSON-only output:

```sh
npx --yes genizah search procedural maps
```

The installed `genizah` skill recommends a bundle but waits for confirmation.
After confirmation, it hands the selected bundle to `customize-spec-bundle`
which reviews your code context and asks clarifying questions before generating
customized specs.
