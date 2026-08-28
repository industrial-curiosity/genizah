---
type: Design
title: Spec Bundle Repository
description: Architecture for an OKF-based repository of technology-neutral specification bundles with generated tag indexes.
tags:
  - ai-agents
  - okf
  - specification-bundles
  - knowledge-catalog
status: draft
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification
---

<!-- markdownlint-disable MD025 -->

# Spec Bundle Repository Design

## Purpose

Repurpose this repository as a library of technology-neutral specification
bundles for AI agents. An agent can discover a relevant bundle, use its
algorithms and strategies as reference material, and customize the specification
for a current use case instead of generating a new design from scratch.

Bundles must be useful when read directly from a checkout. The same repository
structure must also support future CLI and MCP consumers without changing the
bundle format.

The repository uses Open Knowledge Format (OKF) 0.2 because OKF defines a
human-readable and agent-readable directory of Markdown concepts with YAML
frontmatter, progressive-disclosure indexes, provenance, and a conventional
`references/` directory.[^okf-spec]

[^okf-spec]: Open Knowledge Format specification

## Goals

- Store coherent algorithms and strategies as self-contained bundles.
- Keep canonical specifications as technology-neutral as possible.
- Make bundle metadata directly readable and strictly parseable.
- Support discovery by tag without a monolithic machine catalog.
- Record explanations, evidence, provenance, and external documentation in OKF
  concepts.
- Permit optional implementation examples only as illustrative, non-normative
  material; sample tests are never acceptance or conformance tests.
- Provide a reusable template and generator for starting new bundles.
- Provide a downloadable agent skill for adapting a bundle to a target
  implementation through a structured user interview.
- Validate changed bundles on every pull-request update.
- Generate deterministic tag indexes and detect stale generated files.

## Non-goals

- A supported CLI or MCP server in the initial version.
- A package, SDK, or runtime dependency for consuming specifications.
- A global JSON or YAML catalog containing every bundle.
- A fixed taxonomy of algorithms, strategies, or implementation technologies.
- Remote availability checking for external links during local or CI builds.
- Preserving the staged .NET map-generator package as a distributable library.

## Repository Structure

```text
index.md
bundles/
  versioned-procedural-map-generation/
    index.md
    specification.md
    strategies/
      deterministic-replay.md
      version-owned-inputs.md
      template-composition-and-selection.md
      placement-and-reachability.md
    validation.md
tags/
  index.md
  deterministic-generation/
    index.md
  maps/
    index.md
  procedural-maps/
    index.md
templates/
  bundle/
    index.md
    specification.md
    validation.md
    strategies/
      strategy.md
    references/
      index.md
scripts/
  build-index.py
  generate-bundle.py
tests/
  test_build_index.py
  test_generate_bundle.py
  test_repository_content.py
  test_skill.py
  test_workflow.py
.agents/
  skills/
    customize-spec-bundle/
      SKILL.md
      references/
        interview-coverage.md
        output-contract.md
      evals/
        evals.json
.github/
  workflows/
    validate-bundles.yml
```

The root `index.md` is a short orientation layer. It identifies the repository
as OKF 0.2, links to `bundles/` for direct browsing, links to `tags/` for
discovery, and cites the canonical OKF specification. It does not grow into a
complete bundle inventory.

Each immediate child of `bundles/` is an independently distributable knowledge
bundle. Its directory name is its stable bundle identifier.

## Authoritative Bundle Index

Each bundle's `index.md` is the sole authored source for bundle discovery
metadata. It uses the OKF bundle-root `okf_version` frontmatter field and a
repository-specific, strictly parsed Markdown body:

<!-- markdownlint-disable MD013 -->

```markdown
---
okf_version: "0.2"
---

# Versioned Procedural Map Generation

A technology-neutral specification for deterministic, replayable map generation.

## Authors

* @therightstuff
* industrial-curiosity

## Tags

* deterministic-generation
* procedural-maps
* seeded-randomness
* maps
* seeds
* procedural
* versioning

## Specifications

* [Core specification](specification.md) - Required behavior and invariants.

## Strategies

* [Deterministic replay](strategies/deterministic-replay.md) - Preserving stable output across versions.
```

<!-- markdownlint-enable MD013 -->

The index contract is:

- Exactly one H1 supplies the display name.
- The first paragraph after the H1 supplies the description.
- `Authors`, `Tags`, and `Specifications` are required H2 sections.
- `Authors` contains one or more unordered-list items.
- An author is an opaque identity string. Entries may be personal names, GitHub
  usernames, organization names, email addresses, or any mixture of those
  forms. The tooling trims surrounding whitespace but does not classify,
  normalize, or impose OKF actor syntax on authors.
- `Tags` contains one or more unique lowercase kebab-case values.
- `Specifications` contains at least one local Markdown link.
- Additional content groups, such as `Strategies`, `Validation`, and
  `References`, use OKF index entries: a Markdown link followed by a short
  description.

## Concept Contract

Every non-reserved Markdown file inside a bundle is an OKF concept. In addition
to OKF's required `type`, repository concepts require `title`, `description`,
`tags`, and `sources` frontmatter.

Concept bodies use structural Markdown and explain:

- The problem or decision the concept addresses.
- The relevant algorithm, strategy, or requirement.
- Why the approach works and the evidence supporting it.
- Assumptions, invariants, tradeoffs, and failure modes.
- Which decisions an adopting agent is expected to customize.

Factual claims derived from a source use OKF claim-level footnotes whose labels
match `sources[].id`. Supporting concepts include at least one absolute link to
external documentation. The build validates the presence and shape of evidence
metadata but does not attempt to determine whether a claim is true or fetch
remote resources.

The initial repository uses these producer-defined concept types:

- `Specification` for normative, technology-neutral behavior and invariants.
- `Strategy` for algorithms, alternatives, rationale, and tradeoffs.
- `Validation` for portable acceptance scenarios and conformance checks.
- `Reference` for implementation examples, external code, or additional
  technical material.

Consumers must tolerate additional OKF types, as required by OKF's extensible
model.[^okf-spec]

## References

The `references/` directory is optional and non-normative unless a
specification explicitly states otherwise. It may contain:

- OKF `Reference` concepts that point to public repository files or directories.
- Local code samples in any programming language.
- Excerpts or adapted examples whose licenses permit redistribution.
- Run instructions or explanatory documents for an implementation example.

Raw non-Markdown files do not require OKF frontmatter. Every raw example is
linked from an OKF `Reference` concept that explains its relevance, provenance,
external documentation, and license when known. Links to public code should
identify the most precise stable resource available.

Implementation samples are illustrative only. They are never required bundle
content, normative requirements, acceptance tests, or conformance evidence.
Tests distributed with a sample illustrate that implementation and do not need
to be run, ported, or retained by an adopting agent. Normative `Specification`
and `Validation` concepts remain authoritative. A bundle with no useful
supporting material may omit `references/` entirely. The initial bundle does
so and retains no staged C# source or tests.

## Tag Discovery

There is no monolithic `catalog.json`. Tag discovery is distributed across
small generated OKF indexes:

```text
tags/
  index.md
  deterministic-generation/index.md
  maps/index.md
  procedural-maps/index.md
  seeded-randomness/index.md
```

`tags/index.md` lists the available tag directories. Each
`tags/<tag>/index.md` links to every bundle declaring that tag and repeats only
the information needed to evaluate the result: bundle name, description, and
authors.

<!-- markdownlint-disable MD013 -->

```markdown
# Procedural maps

* [Versioned Procedural Map Generation](../../bundles/versioned-procedural-map-generation/) - A technology-neutral specification for deterministic, replayable map generation. Authors: @therightstuff, industrial-curiosity.
```

<!-- markdownlint-enable MD013 -->

Tag directories and entries are sorted using a single documented ordinal
ordering. The generated tree is committed so agents can use it without running
tooling.

## Bundle Template and Generator

`templates/bundle/` contains the complete minimum authored structure for a new
bundle: a strict bundle index, a core specification, a validation concept, one
strategy concept, and a references index. Template concept files demonstrate
the repository's required OKF frontmatter, evidence fields, and claim-level
source attribution.

The standard-library generator copies the template into a named bundle folder:

```text
python3 scripts/generate-bundle.py <bundle-id>
python3 scripts/generate-bundle.py <bundle-id> --title "Bundle display name"
```

The generator validates that the identifier is lowercase kebab-case and that
the destination does not exist. It never merges with or overwrites an existing
bundle. It derives a display title from the identifier when `--title` is
omitted, replaces documented template tokens, prints each created path, and
finishes by showing the validation and index-generation command the author
should run after replacing the template guidance.

Generated template content is intentionally not treated as a valid published
bundle until the author supplies real descriptions, evidence, sources,
customization points, and acceptance scenarios. The validator reports these
remaining template tokens as actionable errors.

## Customization Interview Skill

`.agents/skills/customize-spec-bundle/` is a portable, downloadable agent skill.
Downloading that directory is sufficient to use it; the skill body does not
refer to host-specific tools, machine-local skill paths, or private repository
configuration.

The skill activates when a user asks an agent to apply, adapt, or customize a
spec bundle for a concrete implementation, or when the user explicitly invokes
the skill. It accepts a local bundle path or a downloaded bundle directory.

The skill follows this workflow:

1. Read the bundle index and then load only the concepts relevant to the target
   request.
2. Treat implementation samples and their tests as optional, illustrative,
   non-normative material; never use them as requirements or conformance tests.
3. Inspect an available target repository before asking questions whose answers
   can be discovered from its files.
4. Extract the bundle's invariants, customization points, alternatives, failure
   conditions, and validation scenarios into an interview checklist.
5. Ask the user one focused question at a time about unresolved target choices.
6. Cover the target domain, language and runtime, integration boundaries, data
   and persistence, determinism and compatibility, security, scale and
   performance, operations, failure policy, test strategy, and excluded scope
   when those topics are relevant to the bundle.
7. Explain tradeoffs when a choice weakens a bundle invariant, and record an
   explicit deviation instead of silently changing the source strategy.
8. Present a target implementation profile and a customized specification draft
   for user review.

The final profile records discovered facts separately from user decisions and
clearly identifies unresolved questions. The customized specification preserves
applicable bundle invariants and acceptance scenarios, names selected
implementation choices, links back to the source bundle, retains relevant OKF
provenance, and lists deliberate deviations. The skill returns these artifacts
in the conversation by default and writes them to a target repository only when
the user supplies a path and requests file changes.

`references/interview-coverage.md` owns the reusable question domains and
completion criteria. `references/output-contract.md` owns the exact target
profile and customized-spec structure. The `SKILL.md` remains concise and tells
the agent when each reference must be loaded.

The skill's `evals/evals.json` is tested with prompts covering a new project, an
existing repository with discoverable answers, conflicting target constraints,
an explicit departure from a bundle invariant, incomplete user answers, and a
bundle with unknown optional concept types, and a bundle containing optional
sample code and tests. Skill implementation includes a repo-scope coherence
scan, trigger-description review, and iterative evaluation before it is
declared downloadable.

## Index Builder

The initial builder is one Python 3 standard-library script with no package
dependencies:

```text
python3 scripts/build-index.py
python3 scripts/build-index.py --check
python3 scripts/build-index.py --bundles bundle-a bundle-b
```

The default command validates all bundles and regenerates all tag indexes.
`--check` performs the same validation and generation in memory, reports drift,
and does not write. `--bundles` limits full concept validation to the named
existing bundles while still parsing every bundle index needed to regenerate a
complete tag tree. A removed bundle has no content to validate, but full tag
generation removes its derived entries.

The parser supports the documented repository subset of Markdown and YAML. It
does not claim to be a general-purpose OKF, Markdown, or YAML implementation.
Future tooling may replace the parser while preserving the repository contract.

### Validation Rules

The builder validates:

- Every immediate bundle directory contains `index.md`.
- Bundle identifiers are unique lowercase kebab-case values.
- Required index headings occur exactly once and in the required order.
- Titles and descriptions are non-empty.
- Author lists are non-empty and contain no exact duplicates after trimming.
- Tag lists are non-empty, normalized, and duplicate-free.
- Specification links are present and resolve to files inside the bundle.
- All indexed local links exist and cannot escape the bundle root.
- Non-reserved Markdown concepts contain frontmatter and a non-empty `type`.
- Required repository metadata and external evidence links are present.
- Existing generated tag indexes exactly represent current bundle metadata.

Unknown optional index sections and unknown OKF concept types remain valid so
the repository can evolve without breaking consumers.

### Failure Behavior

Validation accumulates independent errors and reports each with its source path
and line number. The builder constructs the complete desired tag tree in memory
and writes nothing if validation fails.

Generated files contain a marker naming `scripts/build-index.py`. The builder
may replace or remove only files and tag directories carrying that marker. It
must not delete an unmarked file or directory under `tags/`; a collision is a
validation error requiring explicit resolution.

Output is written deterministically. Temporary output is completed before
generated files are replaced so an interrupted run does not leave a partially
generated tag index.

## Pull-request Validation

`.github/workflows/validate-bundles.yml` runs for pull-request `opened`,
`reopened`, and `synchronize` events without a path filter. It uses read-only
contents permission, consumes no secrets, and cannot commit or push changes.
Concurrency is scoped to the pull-request number so a newer commit cancels an
obsolete validation run.

The workflow checks out the pull-request head and compares the event's base SHA
with its head SHA. It derives affected bundle identifiers from added, modified,
renamed, and deleted paths below `bundles/`.

The workflow then:

1. Runs the builder's automated tests.
2. Runs the bundle-generator tests and deterministic skill structure and
   trigger tests.
3. Fully validates each added or modified bundle.
4. Validates every bundle when the builder, generator, template, validator
   tests, bundle contract, customization skill, or validation workflow changes.
5. Regenerates the complete tag index tree, including removal of entries for
   deleted bundles.
6. Inspects Git status below `tags/` and fails if tracked or untracked changes
   remain.

Running the real builder followed by the Git status check proves that generated
indexes were updated and committed with the pull request. A check that only
reimplements builder logic inside the workflow would not establish that
invariant.

Each failing step identifies the affected bundle or generated path and writes
the exact local remediation command to the workflow summary. A successful run
lists the validated bundles and confirms that tag indexes were current.

External actions use explicit, fully qualified semantic release tags. Their
current compatible releases are verified from the authoritative upstream
repositories when the workflow is implemented rather than copied from stale
examples.

## Testing

`tests/test_build_index.py` uses Python's standard `unittest` and temporary
repository fixtures. Coverage includes:

- Valid bundles with mixed author identity forms.
- Multiple bundles sharing tags.
- Deterministic tag and bundle ordering.
- Missing or duplicate required sections.
- Invalid bundle identifiers and tags.
- Empty or duplicate author entries.
- Missing, broken, or bundle-escaping local links.
- Missing OKF fields, sources, or external evidence links.
- Unknown optional sections and concept types.
- Stale tracked tag indexes.
- Newly generated untracked tag directories.
- Bundle additions, modifications, renames, and removals.
- Full validation when tooling or format files change.
- Build mode and non-writing check mode producing equivalent desired output.
- Template generation into a named bundle directory.
- Rejection of invalid identifiers and existing destinations without partial
  copies.
- Replacement of template tokens and preservation of source template files.
- Customization-skill trigger coverage and portable output-contract adherence.

## Initial Bundle

The first bundle is `versioned-procedural-map-generation`. It extracts the
reusable knowledge from the staged map-generator design while discarding
technology-specific packaging decisions.

Its authors are `@therightstuff` and `industrial-curiosity`. In addition to
specific compound tags, the bundle includes useful one-word discovery tags such
as `maps`, `seeds`, `procedural`, and `versioning`.

The core specification preserves these invariants:

- A seed identifies both entropy and an immutable generator version.
- The selected version owns every input required for deterministic replay.
- Configuration is validated and frozen before generation begins.
- Template composition may be recursive but must be acyclic.
- Candidate enumeration and selection ordering are deterministic.
- Shapes, transforms, layers, connectors, and selectors are data-defined.
- Generated topology is validated, including required reachability.
- Executing a caller-provided seed is separate from allocating a random seed.

The bundle exposes seed representation, pseudo-random algorithm, configuration
syntax, topology, shapes, selectors, connectors, persistence, and failure policy
as customization points. Its validation concept expresses portable
Given/When/Then acceptance scenarios instead of framework-specific tests.

The staged C# APIs, .NET targets, NuGet packaging, YamlDotNet dependency,
`IndustrialCuriosity` namespace, exact filenames, seven-character codec, and
implementation task sequence are not bundle content. The initial bundle retains
no implementation samples or sample tests. A finished public implementation may
be linked later from an optional, explicitly illustrative `Reference` concept.

## Repository Repurposing

Implementation replaces the current package repository with the spec-bundle
repository. After reusable knowledge is incorporated into the initial bundle,
the .NET solution, root source and test projects, package metadata,
package-oriented README, and technology-specific implementation plan are
removed rather than retained as bundle samples.

The new README remains an orientation layer: purpose, direct agent use, bundle
layout, local validation and generation commands, contribution flow, the
downloadable customization skill, and links to detailed format documentation.
It identifies `@therightstuff` and `industrial-curiosity` where repository and
initial-bundle authorship is shown. It references the canonical OKF specification
rather than reproducing it.

## Future Evolution

A CLI may later list tags, resolve bundles, and download bundle directories. An
MCP server may expose the same discovery and retrieval operations. Both consume
`bundles/` and generated `tags/` directly; neither introduces a new catalog or
changes the authoring contract.

The initial design deliberately leaves runtime distribution, remote search,
semantic ranking, dependency relationships between bundles, and remote link
health checking for later iterations.
