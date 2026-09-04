# Migrate Remaining Superpowers Specifications

## Why

The previous OpenSpec migration preserved installer safety, search basics, and
command-variant parity, but left the repository's bundle format, index-builder,
customization workflow, and several installer and search contracts only in the
legacy Superpowers record. Future changes therefore lack one canonical,
testable requirements source.

## What Changes

- Add canonical requirements for the OKF-based specification-bundle repository,
  generated tag discovery, deterministic validation, and safe index generation.
- Add canonical requirements for the bundle-customization interview and its
  output contract.
- Complete the installer specification with catalog-source, installed-skill,
  and user-visible handoff requirements.
- Complete the catalog-search specification with its source, ranking, response,
  empty-result, and failure contracts across published and local variants.

## Capabilities

### New Capabilities

- `specification-bundle-repository`: Bundle format, generated tag-index, and
  validation requirements for the catalog.
- `bundle-customization-workflow`: Portable bundle adaptation interview and
  customized-specification output requirements.

### Modified Capabilities

- `agent-skill-installation`: Add catalog-source, installed-skill, and
  discovery-to-customization handoff requirements.
- `catalog-skill-search`: Add complete deterministic ranking, response, source,
  empty-result, and failure requirements for command variants.

## Impact

This is a specification migration. It affects OpenSpec planning artifacts and
may identify implementation, test, or documentation gaps during apply; it does
not itself change the public command interface.
