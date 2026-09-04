# Agent Skill Installation Delta

## ADDED Requirements

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
