# Specification Bundle Repository Delta

## ADDED Requirements

### Requirement: Author self-contained, technology-neutral bundles

The catalog SHALL store each bundle in a stable lowercase-kebab-case directory
whose `index.md` is the sole authored discovery metadata. The index SHALL have
one display-name H1, a description paragraph, and non-empty `Authors`, `Tags`,
and `Specifications` sections. Tags SHALL be unique lowercase-kebab-case
values, and every indexed local link SHALL remain inside its bundle.

#### Scenario: Invalid bundle index

- **WHEN** a bundle has a missing required section, duplicate or invalid tag,
  or an indexed link that escapes the bundle
- **THEN** catalog validation SHALL reject the bundle and identify the source
  location of the violation

### Requirement: Preserve concept provenance and normative boundaries

Every non-reserved Markdown concept in a bundle SHALL declare `type`, `title`,
`description`, `tags`, and `sources` metadata. Specifications and validation
concepts SHALL be authoritative; implementation examples and their tests SHALL
be explicitly illustrative and non-normative.

#### Scenario: Bundle with implementation samples

- **WHEN** a bundle contains an implementation sample or sample test
- **THEN** a consumer SHALL not treat that material as an acceptance or
  conformance requirement unless an authoritative specification says so

### Requirement: Generate deterministic tag discovery indexes

The catalog SHALL derive committed tag indexes from bundle indexes rather than
from a monolithic catalog file. Generated tag directories and entries SHALL use
one documented ordinal ordering and identify each matching bundle by name,
description, and authors.

#### Scenario: Rebuild unchanged catalog metadata

- **WHEN** catalog metadata has not changed
- **THEN** regenerating tag indexes SHALL produce byte-identical output

### Requirement: Validate and safely replace generated indexes

The index builder SHALL validate the complete desired tag tree before writing.
It SHALL report independent validation failures with source locations, write
nothing on validation failure, and replace or remove only generated paths that
carry its ownership marker. An unmarked collision SHALL fail without deletion.

#### Scenario: User-authored collision

- **WHEN** the desired generated tag path contains an unmarked file or
  directory
- **THEN** the builder SHALL preserve that path and fail with actionable
  collision guidance

### Requirement: Provide safe bundle scaffolding

The bundle generator SHALL create the complete documented template for a valid
lowercase-kebab-case identifier, reject an existing destination without
overwriting or merging it, and identify remaining template tokens as
publication-blocking validation errors.

#### Scenario: Existing bundle destination

- **WHEN** an author requests generation into an existing bundle directory
- **THEN** the generator SHALL leave the directory unchanged and report the
  rejected destination

### Requirement: Validate catalog changes in pull requests

Pull-request validation SHALL run the builder and its automated tests, validate
affected bundles, regenerate the complete tag tree, and fail when generated
indexes have drifted. The workflow SHALL use read-only repository contents and
SHALL not use secrets, commit, or push.

#### Scenario: Pull request leaves stale generated indexes

- **WHEN** a pull request changes bundle metadata without committing the
  resulting tag-index changes
- **THEN** validation SHALL fail and identify the generated paths that require
  update
