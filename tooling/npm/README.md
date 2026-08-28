# Genizah CLI

Install the Genizah discovery and customization skills in a project:

```sh
npx --yes genizah init
```

The command lets you select one project-level skill location. It defaults to
`.agents/skills` and also supports `.github/skills`, `.claude/skills`,
`.cursor/skills`, `.codex/skills`, `.opencode/skills`, and `.pi/skills`.
Pass `--skills-dir RELATIVE_PATH` to select a contained project path without a
prompt.

Before the catalog is published, install from a local Genizah checkout while
standing in the target project:

```sh
npm --prefix ../genizah/tooling/npm run local:init -- .
```

`local:init` resolves `.` from the invoking directory, reads the skills from
that checkout, and makes no network request. The installed `genizah` skill
uses the local catalog for discovery:

```sh
npm --prefix ../genizah/tooling/npm run local:search -- procedural maps
```

Search the GitHub-hosted catalog with JSON-only output:

```sh
npx --yes genizah search procedural maps
```

The installed `genizah` skill recommends a bundle but waits for confirmation.
After confirmation, it hands the selected bundle to `customize-spec-bundle`.
