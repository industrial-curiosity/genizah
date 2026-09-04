---
type: Guide
title: Bundle format and authoring guide
description: Define the technology-neutral OKF bundle, concept, evidence, reference, tag, template, and validation contract for this repository.
tags:
  - specification-bundles
  - authoring
  - okf
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification
---

<!-- markdownlint-disable MD025 -->

# Bundle format and authoring guide

Each immediate child of [`bundles/`](../bundles/) is one independently
distributable, technology-neutral bundle. Its `index.md` is authoritative;
generated [`tags/`](../tags/) files never replace it. The structure follows OKF
0.2: Markdown concepts with YAML frontmatter, indexes, provenance, and
references.[^okf-spec]

## Bundle index grammar

Every `bundles/BUNDLE_ID/index.md` uses exactly this frontmatter and no other
frontmatter fields:

```yaml
---
okf_version: "0.2"
---
```

After the frontmatter, the index has exactly one non-empty H1. Its first
non-empty paragraph is the bundle description. The following H2 sections are
required exactly once and in this order: `Authors`, `Tags`, and
`Specifications`.

```markdown
# Bundle display name

One concise technology-neutral description.

## Authors

* Example Person

## Tags

* example-tag

## Specifications

* [Core specification](specification.md) - Defines the portable contract.
```

`Authors` has at least one unordered-list item. Each author is an opaque,
non-empty identity string: a personal name, GitHub username, organization
name, email address, or a mixed list of these forms is valid. Surrounding
whitespace is trimmed; the builder neither normalizes identities nor permits
exact duplicate entries.

`Tags` has at least one unique lowercase kebab-case value matching
`[a-z0-9]+(?:-[a-z0-9]+)*`. One-word tags such as `maps` are valid, alongside
compound tags such as `procedural-maps`.

Choose discovery tags from the bundle's core offering: its primary capability,
domain, and distinguishing guarantees. Cover those dimensions where they help
discovery, but do not add tags solely for supporting algorithms, data
structures, or implementation mechanics unless the bundle itself is primarily
about that subject.

`Specifications` has at least one unordered-list entry in this exact shape:
`* [Title](relative-path.md) - short non-empty description`. The linked file
must exist, be Markdown, and resolve inside the bundle. Optional H2 sections
such as `Validation`, `Strategies`, and `References` use the same linked-entry
form; all indexed local links must remain inside the bundle and exist.

## Concepts, explanations, and evidence

Every Markdown file in a bundle other than reserved `index.md` and `log.md` is
an OKF concept. It requires frontmatter with non-empty `type`, `title`,
`description`, `tags`, and `sources` fields. Each source requires `id` and
`resource`; `title` is recommended when it improves source recognition. At
least one resource must be an absolute external HTTPS documentation URL. Use a
claim-level footnote whose label matches the source ID whenever prose relies on
that source.

```yaml
---
type: Strategy
title: Stable candidate selection
description: Select equivalent candidates from a documented stable order.
tags:
  - determinism
sources:
  - id: source-id
    resource: https://example.com/documentation
    title: Source title
---
```

Concept bodies state the problem or decision, requirements or algorithm,
evidence, assumptions, invariants, tradeoffs, failure modes, and customization
choices. Common types are `Specification`, `Strategy`, `Validation`, and
`Reference`; consumers must tolerate other types.[^okf-spec]

Canonical specifications and strategies stay technology-neutral. A validation
concept should use portable acceptance scenarios instead of a framework's test
API or a package-specific integration recipe.

## References

An optional `references/` directory contains supporting material unless a
specification explicitly says otherwise. It can contain an OKF `Reference`
concept, local code samples, and links to precise public repository resources.
A raw non-Markdown example does not need frontmatter, but an indexed
`Reference` concept must explain its purpose, provenance, relevant external
documentation, and license when known.

Implementation samples are optional and illustrative only. They are never
required bundle content, normative requirements, acceptance tests, or
conformance evidence. Tests included with a sample illustrate that sample; an
author or adapting agent is not required to run, port, or preserve them. The
bundle's `Specification` and `Validation` concepts remain authoritative. The
initial versioned-map bundle intentionally contains no implementation samples.

## Tags and generated discovery

Bundle-discovery tags are declared only in a bundle index;
`scripts/build-index.py` derives the complete `tags/` tree from those
declarations. Concept `tags` remain required concept metadata, but they do not
populate `tags/`. Tag directories are sorted by tag string, and entries within
each tag are sorted by bundle ID, both using Python's native string ordering
(Unicode code-point ordinal ordering). Each generated file carries a marker
identifying the builder. Do not edit generated tag indexes by hand; change a
bundle index and run the builder instead.

The builder refuses to overwrite unmarked tag files or remove unmarked tag
directories. This preserves local material if generated output would collide
with it.

The builder stages the complete generated tree before replacing the current
tree. If replacement is interrupted, it restores the complete prior tree rather
than leaving partially generated tag indexes.

## Start a new bundle

The [`templates/bundle/`](../templates/bundle/) directory is the minimum
authoring skeleton: a strict index, a core specification, validation,
strategy, and references index. Create a copy with a lowercase kebab-case ID:

```bash
python3 scripts/generate-bundle.py example-bundle
```

To supply a display name explicitly:

```bash
python3 scripts/generate-bundle.py example-bundle --title "Example Bundle"
```

The generator replaces `{{BUNDLE_ID}}` and `{{BUNDLE_TITLE}}`, but leaves
`REPLACE_*` content as an authoring checklist. Generated content is deliberately
invalid until those markers, metadata, explanations, evidence, customization
points, and acceptance scenarios are replaced. The generator never merges with
or overwrites an existing destination. The references placeholder can be
removed, together with its index entry, when the bundle has no useful
supporting material.

Commands assume the repository root. From elsewhere, for example, run
`python3 /work/spec-bundles/scripts/build-index.py --root /work/spec-bundles --check`.

## Build and review

Run the builder after authoring or modifying a bundle:

```bash
python3 scripts/build-index.py
```

This validates all bundle indexes and concepts, then regenerates the complete
tag tree. To validate without writing and report generated-index drift, run:

```bash
python3 scripts/build-index.py --check
```

For a focused content check, name changed existing bundles:

```bash
python3 scripts/build-index.py --bundles example-bundle
```

Focused mode still parses every bundle index and computes the complete tag
tree, but limits full concept validation to the named existing bundles. A
removed bundle needs no concept validation; the next full tag generation
removes its derived entries.

Pull requests run the Python tests, validate added or modified bundles, run a
full validation when repository tooling or the format contract changes, rebuild
the complete tag tree, and fail when the result would change tracked or
untracked tag output. Run `python3 scripts/build-index.py` and then
`python3 scripts/build-index.py --check` locally before opening a pull request.

## Adapt a bundle

For agent-assisted discovery, install the Genizah skills with
`npx --yes genizah init`, or use
`npm --prefix ../genizah/tooling/npm run local:init -- .` from a target project
before the catalog is published. The local command reads the checkout directly,
installs the `genizah` skill with a local search command, and does not use the
network. It accepts the same `--skills-dir`, `--force`, and `-f` options as the
published installer. See the [CLI guide](../tooling/npm/README.md) for
skill-directory selection, JSON search output, confirmation, and the
customization handoff.

The downloadable
[`customize-spec-bundle` skill](../.agents/skills/customize-spec-bundle/) helps
an agent inspect a target implementation, interview its user one unresolved
decision at a time, and produce a traceable target profile plus customized
specification. It does not make filesystem changes unless the user explicitly
requests a path and write operation. See the [skill instructions](../.agents/skills/customize-spec-bundle/SKILL.md).

[^okf-spec]: Open Knowledge Format specification
