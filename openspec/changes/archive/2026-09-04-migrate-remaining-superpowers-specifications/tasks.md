# Migrate Remaining Superpowers Specifications Tasks

## 1. Catalog repository contract

- [x] 1.1 Compare bundle indexes, concepts, templates, and the index builder
  with the specification-bundle-repository requirements; implement any
  conformance gaps without weakening safe collision handling.
- [x] 1.2 Add or update Python tests for invalid metadata, deterministic index
  generation, unmarked collisions, generator no-overwrite behavior, and
  pull-request index-drift validation.

## 2. Bundle customization workflow

- [x] 2.1 Compare the downloadable customization skill and its references with
  the bundle-customization-workflow requirements; implement any missing
  portability, interview, provenance, or output-contract behavior.
- [x] 2.2 Add or update skill tests and evaluation fixtures for discovered
  facts, explicit invariant departures, and no-write-by-default output.

## 3. Installer and search completion

- [x] 3.1 Compare published, remote, local, offline, and test installer paths
  with the agent-skill-installation requirements; implement source and discovery
  handoff gaps while retaining shared location and transaction behavior.
- [x] 3.2 Compare published, remote, local, offline, and test search paths
  with the catalog-skill-search requirements; implement source, ranking,
  response, empty-result, and failure-diagnostic gaps.
- [x] 3.3 Add invocation and regression tests for every supported command
  variant affected by the installer or search changes, including no-network
  local behavior and identical documented semantics and diagnostics.

## 4. Documentation and verification

- [x] 4.1 Update README.md and docs/spec.md to reflect any user-facing or
  architectural changes introduced by this change; if docs/spec.md is absent,
  document the applicable architecture in its established replacement.
- [x] 4.2 Record concrete canonical-purpose text for archive synchronization.
- [x] 4.3 Run the Node, Python, catalog-index, Markdown, and strict OpenSpec
  validation suites; record any remaining conformance gap before archiving.
