# command-variant-parity Specification

## Purpose

Keep equivalent published, remote, local, offline, and test command variants
synchronized.

## Requirements

### Requirement: Keep equivalent command options synchronized

Every supported command variant SHALL accept the same documented options and
aliases for an equivalent
capability. A variant-specific invocation prefix or target-project argument
does not permit different option semantics.

#### Scenario: Force an installation in a local variant

- **WHEN** a user invokes a local installation variant with `--force` or `-f`
- **THEN** it performs the same explicit replacement behavior as the published
  installation command

#### Scenario: Select a skill directory in a local variant

- **WHEN** a user invokes a local installation variant with `--skills-dir`
- **THEN** it selects the same contained project skill directory behavior as
  the published installation command

### Requirement: Keep equivalent diagnostics synchronized

Every supported command variant SHALL report equivalent validation failures,
safe defaults, and recovery guidance for the same capability. Variant-specific
paths or invocation prefixes may differ, but the required user action SHALL
not.

#### Scenario: Conflicting user-owned directory

- **WHEN** an installation variant encounters an unrelated target skill
  directory without force
- **THEN** it preserves the directory and states the exact force option that
  enables replacement

### Requirement: Test and document every command interface change

Every command-interface change SHALL include an invocation test for every
supported variant and update the applicable user-facing documentation.

#### Scenario: Add an installation option

- **WHEN** a change adds or alters an installation option
- **THEN** tests cover the published and local installation paths and the
  documentation describes the option for each supported invocation
