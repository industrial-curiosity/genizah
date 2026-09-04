# agent-skill-installation Specification

## Purpose

Install Genizah discovery and customization skills safely from a selected
catalog source.

## Requirements

### Requirement: Select one contained project skill location

The installer SHALL select exactly one supported skill location inside the
target project before writing files. It SHALL default to the portable project
skill location, accept an explicit contained relative location, reuse an
existing Genizah-owned installation when no location is supplied, and reject
absolute, escaping, or symbolic-link-containing destinations.

#### Scenario: Explicit contained location

- **WHEN** a user supplies a supported contained relative skill location
- **THEN** the installer writes only to that location without prompting

#### Scenario: Unsafe location

- **WHEN** a selected location is absolute, escapes the target project, or has
  a symbolic-link ancestor
- **THEN** the installer fails before fetching, staging, backing up, or writing
  catalog skills

### Requirement: Install validated catalog skill trees transactionally

The installer SHALL obtain the required catalog skill files, stage them outside
the destination, validate each skill's exact catalog identity, and replace
target directories only after validation succeeds. If replacement fails, it
SHALL remove newly installed directories and restore every backed-up directory.

#### Scenario: Invalid catalog skill identity

- **WHEN** a fetched or local catalog skill lacks the exact expected identity
- **THEN** the installer fails without changing the target project

#### Scenario: Replacement failure

- **WHEN** moving a staged skill into the selected destination fails after a
  prior directory was backed up
- **THEN** the installer restores the backed-up directory and removes newly
  installed directories

### Requirement: Preserve unrelated skill directories by default

The installer SHALL replace an existing target directory only when it has the
exact Genizah ownership identity, unless the user explicitly requests force.
It SHALL leave unrelated directories unchanged by default.

#### Scenario: Unrelated target directory

- **WHEN** a target skill directory exists without the exact Genizah ownership
  identity and force is not requested
- **THEN** the installer leaves the directory unchanged and refuses installation

### Requirement: State the force recovery path for replacement refusals

The installer SHALL identify the target and state that rerunning with `--force`
or `-f` replaces it when it refuses an unrelated target directory. The default
invocation SHALL remain non-destructive.

#### Scenario: User opts into replacement

- **WHEN** a user reruns an otherwise refused installation with `--force` or
  `-f`
- **THEN** the installer replaces the conflicting target directory with the
  validated catalog skill tree

### Requirement: Install the required catalog skill set

The installer SHALL obtain and validate the `genizah` discovery skill and the
`customize-spec-bundle` skill, including required linked references, before it
writes either skill. The published variant SHALL use the committed catalog
source and SHALL not clone, vendor, or retain a catalog snapshot in the target
project.

#### Scenario: Catalog skills are unavailable

- **WHEN** either required skill tree cannot be obtained or validated
- **THEN** the installer SHALL identify the requested catalog path and leave
  the target project unchanged

### Requirement: Preserve catalog-source semantics across variants

Published and remote installation variants SHALL obtain the committed remote
catalog. Local, offline, and test variants SHALL use their explicit local or
stubbed source without a network request. Every variant SHALL install the same
required skill identities and use the same location-selection and transactional
installation behavior.

#### Scenario: Local development installation

- **WHEN** a user invokes local initialization for a target project
- **THEN** it SHALL derive the catalog checkout from its local command context,
  avoid network access, and install the same validated skill trees as published
  initialization

### Requirement: Start discovery only after installation succeeds

After a successful installation, the installer SHALL report the selected skill
location and the exact prompt or command that starts discovery. A local skill
installation SHALL invoke the corresponding local search path so discovery is
usable before publication.

#### Scenario: Successful local installation

- **WHEN** local initialization completes successfully
- **THEN** its reported discovery handoff SHALL use the local search invocation
  rather than the published package invocation

### Requirement: Require confirmation before customization

The installed discovery skill SHALL inspect target-project facts, derive search
terms, present ranked candidates, and recommend a candidate. It SHALL wait for
the user to select or confirm a bundle before loading selected concepts or
starting customization.

#### Scenario: Recommendation not confirmed

- **WHEN** the discovery skill has recommended a bundle but the user has not
  selected or confirmed one
- **THEN** it SHALL not load bundle concepts or begin the customization
  interview

#### Scenario: Confirmed bundle

- **WHEN** the user confirms a selected bundle
- **THEN** the discovery skill SHALL load only that bundle's concepts required
  for customization and begin the customization workflow
