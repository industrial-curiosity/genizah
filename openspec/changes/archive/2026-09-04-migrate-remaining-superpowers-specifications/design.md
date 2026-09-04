# Migrate Remaining Superpowers Specifications Design

## Context

The archived installer migration established three canonical capabilities, but
the earlier Superpowers designs remain the only normative record for the bundle
repository and parts of discovery. This change migrates durable behavior, not
historical task checklists, reports, or point-in-time verification evidence.

## Goals / Non-Goals

**Goals:**

- Make OpenSpec the canonical requirements source for catalog authoring,
  validation, customization, installation, and search.
- Preserve deterministic, safe behavior across published, remote, local,
  offline, and test command variants.
- Separate durable requirements from legacy implementation history.

**Non-Goals:**

- Change the bundle format, command interface, or published package in this
  artifact-only migration.
- Duplicate legacy plans, completed task reports, or obsolete implementation
  details in canonical specifications.
- Archive or delete legacy Superpowers documents before implementation and
  conformance verification are complete.

## Decisions

### Use capability specifications for enduring contracts

The repository format and customization workflow become separate capabilities;
installer and search omissions become additive delta requirements. This keeps
each capability independently discoverable and prevents the installer from
becoming the owner of catalog authoring rules.

Alternative: a single migration specification. Rejected because it would mix
authoring, agent workflow, installation, and query contracts.

### Define variants by behavior, not transport

Published and remote commands may fetch the committed catalog, while local,
offline, and test variants may use an explicit local source or stub. Equivalent
operations retain their options, semantics, diagnostics, ranking, and response
shape; only the invocation prefix and source transport differ.

Alternative: define every wrapper independently. Rejected because it permits
silent drift when one interface changes.

### Keep generated catalog files safely replaceable

The index builder validates the whole desired output before replacing marked
generated files. It refuses unmarked collisions, preserving user-authored
files and requiring an explicit recovery action rather than deleting them.

Alternative: regenerate individual files in place. Rejected because validation
or interruption could leave a partial or destructive catalog state.

## Risks / Trade-offs

- [Legacy language is broader than current implementation] → Apply work SHALL
  compare each requirement with source and tests before declaring conformance.
- [A migration may over-preserve historical details] → Keep requirements
  behavior-focused and leave task sequencing and historic evidence in the
  legacy record.
- [New command variants may drift] → Maintain the existing parity capability
  and add variant-level tests whenever their interface changes.

## Migration Plan

1. Add the new and delta specifications in this change.
2. Compare implementation, tests, and user documentation with every scenario.
3. Implement and test any conformance gaps using the apply workflow.
4. Archive the change only after canonical specifications are synchronized and
   the legacy documents remain available as provenance.

Rollback removes this unarchived change; canonical OpenSpec specifications and
the legacy record remain unchanged until archive.

## Archive Synchronization Notes

When this change is archived, set the canonical capability purposes to:

- `agent-skill-installation`: Install Genizah discovery and customization
  skills safely from a selected catalog source.
- `catalog-skill-search`: Deterministically discover specification bundles from
  a catalog source.
- `specification-bundle-repository`: Author, validate, and discover
  technology-neutral specification bundles.
- `bundle-customization-workflow`: Adapt a confirmed specification bundle to a
  target implementation through a traceable interview.

## Open Questions

None.
