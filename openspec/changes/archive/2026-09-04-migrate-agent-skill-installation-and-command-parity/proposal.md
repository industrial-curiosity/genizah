## Why

The completed Superpowers SDD record contains the durable requirements for
installing catalog skills and searching the catalog, but OpenSpec has no
equivalent source of truth. Recent divergence between published and local
command paths also showed that command-interface requirements need explicit,
testable coverage.

## What Changes

- Migrate the enduring agent-skill installation requirements from the legacy
  Superpowers record into OpenSpec.
- Migrate the catalog-search requirements into OpenSpec.
- Define command-variant parity for published, remote, local, offline, and
  test command paths.
- Require safe refusal defaults with exact opt-in recovery guidance.
- Configure future OpenSpec artifacts to apply the same requirements.

## Capabilities

### New Capabilities

- `agent-skill-installation`: Safe, transactional installation of catalog
  skills into a selected project location.
- `catalog-skill-search`: Deterministic catalog search with machine-readable
  results.
- `command-variant-parity`: Consistent public command interfaces, behavior,
  diagnostics, and recovery paths across supported execution variants.

### Modified Capabilities

None.

## Impact

- `openspec/config.yaml` provides cross-cutting requirements to future
  artifacts.
- New OpenSpec specifications replace the legacy Superpowers SDD record as the
  active requirements source.
- npm CLI entry points, local development wrappers, documentation, and tests
  must conform to the migrated requirements when changed.
