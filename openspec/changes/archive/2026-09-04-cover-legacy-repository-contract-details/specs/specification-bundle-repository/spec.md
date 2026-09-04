# specification-bundle-repository Delta

## ADDED Requirements

### Requirement: Preserve the strict OKF index and evidence contract

Each bundle index SHALL declare `okf_version: "0.2"` as its only frontmatter
field. The catalog SHALL accept opaque, non-empty author identities after
trimming and reject duplicate author entries. Each non-reserved Markdown
concept SHALL include at least one source, including an absolute HTTPS source.
Every factual claim derived from a declared source SHALL use a claim-level
footnote whose label matches that source's identifier. Validation SHALL check
the required metadata and attribution structure without fetching remote
resources or judging factual truth.

#### Scenario: Source-backed concept has incomplete evidence

- **WHEN** a non-reserved concept lacks a declared source, an absolute HTTPS
  source, or attribution for a claim derived from a source
- **THEN** catalog validation SHALL reject the concept and identify the source
  location of the violation without making a network request

### Requirement: Tolerate documented extension points

The catalog validator and consumers SHALL accept unknown optional bundle-index
sections and unknown OKF concept types. An unknown extension SHALL not weaken
validation of required index sections, required concept metadata, or indexed
local-link containment.

#### Scenario: Bundle uses an unknown extension

- **WHEN** a valid bundle contains an unknown optional index section or an
  unknown concept type
- **THEN** catalog validation SHALL accept the extension while enforcing every
  applicable required repository contract

### Requirement: Preserve complete generated indexes across interruption

The index builder SHALL finish writing the complete desired generated output
before replacing generated paths it owns. If replacement is interrupted, the
published `tags/` tree SHALL remain either the complete prior generated tree or
the complete desired generated tree; it SHALL not contain a partial generation.

#### Scenario: Index replacement is interrupted

- **WHEN** index generation is interrupted after temporary output is complete
  and before all owned generated paths are replaced
- **THEN** the `tags/` tree SHALL remain a complete prior or desired generated
  tree and SHALL contain no partially generated index

### Requirement: Select and report pull-request validation comprehensively

The pull-request workflow SHALL run for opened, reopened, and synchronized
pull requests without a path filter. It SHALL cancel obsolete runs for the same
pull request, derive affected bundles from added, modified, renamed, and
deleted paths under `bundles/`, and validate every bundle when repository
format tooling or its validation workflow changes. It SHALL report the affected
bundle or generated path and the exact local remediation command for every
failure, and report validated bundles and current tag indexes on success.

#### Scenario: Pull request removes a bundle

- **WHEN** a pull request deletes a bundle directory
- **THEN** the workflow SHALL regenerate the complete tag tree, remove the
  deleted bundle's derived entries, and fail with the exact remediation command
  if generated-index changes remain
