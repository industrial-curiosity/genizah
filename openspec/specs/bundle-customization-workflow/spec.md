# bundle-customization-workflow Specification

## Purpose

Adapt a confirmed specification bundle to a target implementation through a
traceable interview.

## Requirements

### Requirement: Provide a portable customization skill

The catalog SHALL provide a downloadable customization skill that activates for
an explicit or requested bundle adaptation, accepts a local or downloaded
bundle path, and does not require host-specific tools, private configuration,
or machine-local paths.

#### Scenario: Use on an independent project

- **WHEN** a user installs the skill and supplies a bundle path in another
  project
- **THEN** the skill SHALL perform its workflow without a dependency on the
  catalog author's local environment

### Requirement: Interview only unresolved implementation choices

The customization skill SHALL inspect available target-project facts before
asking questions, load only concepts relevant to the request, and ask one
focused question at a time for unresolved choices. It SHALL preserve applicable
bundle invariants and record an explicit deviation when a chosen trade-off
weakens one.

#### Scenario: Discoverable project fact

- **WHEN** a target-project fact is available from repository files
- **THEN** the skill SHALL use that fact instead of asking the user for it

#### Scenario: Deliberate invariant departure

- **WHEN** a user selects an approach that weakens a bundle invariant
- **THEN** the skill SHALL explain the trade-off and record the departure in
  the customized specification

### Requirement: Produce a reviewable customized specification

The customization skill SHALL return a target implementation profile and a
customized specification draft for review. The output SHALL separate discovered
facts, user decisions, and unresolved questions; name implementation choices;
retain relevant provenance; link the source bundle; and preserve applicable
acceptance scenarios.

#### Scenario: No requested file write

- **WHEN** a user has not supplied a path and explicitly requested file changes
- **THEN** the skill SHALL return the profile and draft in the conversation
  without writing the target repository
