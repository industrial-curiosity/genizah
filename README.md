---
type: Guide
title: Genizah specification bundle catalog
description: Discover, install, and adapt self-contained specification bundles with an AI agent.
tags:
  - specification-bundles
  - ai-agents
  - okf
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification
---

<!-- markdownlint-disable MD025 -->

# Genizah

Genizah is a catalog of self-contained specification bundles: algorithms,
strategies, and acceptance scenarios that an AI agent can adapt to a concrete
implementation. Bundles are not runtime dependencies. The directory and concept
format use Open Knowledge Format (OKF) 0.2 for progressive disclosure,
provenance, and references.[^okf-spec]

![Genizah](https://industrialcuriosity.com/images/genizah/genizah.jpeg)

## Use Genizah

From the project where you want to use a bundle, install the discovery and
customization skills:

```sh
npx --yes genizah init
```

The installer asks where your agent loads project skills, then installs the
`genizah` and `customize-spec-bundle` skills there. It only installs those skill
files; bundles remain in this catalog until you choose one.

Ask your agent to search and integrate a bundle:

```text
Use the genizah skill to search for a spec bundle for this project and
integrate the bundle I confirm.
```

The skill inspects the project, runs a deterministic tag search, and recommends
a bundle. It always waits for your confirmation before loading a bundle and
starting customization.

If you already know the bundle you want, browse [`bundles/`](bundles/) directly.
For discovery without the installer, start with the generated [`tags/`](tags/)
tree.

## Contribute a specification bundle

Create an intentionally incomplete scaffold with a lowercase kebab-case
identifier:

```bash
python3 scripts/generate-bundle.py example-bundle
```

Replace every template marker. Add the concepts, evidence, and references that
an agent needs to adapt the bundle without guessing. The [bundle authoring
contract](docs/bundle-format.md) defines the required metadata, evidence,
optional references, and review expectations.

### Choose useful tags

Tags drive Genizah's deterministic search. Choose a small, non-overlapping set
that describes the bundle's core offering:

- Include its primary capability and domain.
- Add a distinguishing guarantee only when it is central to the bundle.
- Use lowercase kebab-case tags and avoid synonyms or alternate spellings.
- Do not tag incidental algorithms, data structures, validation, testing, or
  implementation details.

For example, a bundle about reproducible procedural maps could use
`procedural-maps`, `deterministic-generation`, and `seeded-randomness`; it
would not need tags for every random-number algorithm or test technique it
mentions. Add the tags to the bundle index, then let the index builder generate
the `tags/` tree.

### Validate your contribution

Regenerate the builder-owned tag indexes after changing a bundle or its tags:

```bash
python3 scripts/build-index.py
```

Before committing, verify that the generated tree is current without writing
files:

```bash
python3 scripts/build-index.py --check
```

Run these commands from the repository root. From elsewhere, for example, run
`python3 /work/spec-bundles/scripts/build-index.py --root /work/spec-bundles --check`.

### Test Genizah locally before publishing

From the target project directory, install skills from your local Genizah
checkout instead of the published package:

```sh
npm --prefix ../genizah/tooling/npm run local:init -- .
```

The local installer knows its catalog path and configures the installed
`genizah` skill to use the local deterministic search command. Then use the
same agent prompt as above to test discovery and customization before pushing.
Adjust `../genizah` when your checkout is elsewhere.

## Learn the format

Use the short [root index](index.md) for agent-oriented navigation and the
detailed [bundle format guide](docs/bundle-format.md) when authoring or
reviewing bundles. The normative format reference is the
<!-- markdownlint-disable-next-line MD013 -->
[Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

## Other interfaces

The Python scripts provide local generation and validation. This repository has
no MCP server. An MCP client with file access can read `index.md`, discover via
`tags/`, and load linked concepts. Future CLI or MCP tools can use these files
without changing the bundle format.

[^okf-spec]: Open Knowledge Format specification
