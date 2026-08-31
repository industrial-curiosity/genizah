---
okf_version: "0.2"
---

<!-- markdownlint-disable MD013 -->

# Durable Atomic File Writes

A technology-independent contract for replacing a file's contents atomically while making successful writes durable and preserving required file attributes.

## Authors

* @therightstuff
* industrial-curiosity

## Tags

* atomic-writes
* file-writing
* file-systems
* durability
* durable-file-system-safety
* safe-writes

## Specifications

* [Core specification](specification.md) - Defines the portable contract, invariants, customization points, and failure behavior for durable atomic file replacement.

## Validation

* [Acceptance scenarios](validation.md) - Defines portable checks for atomic visibility, durability, replacement, metadata, modes, and cleanup.

## Strategies

* [Staged replacement](strategies/staged-replacement.md) - Describes a same-directory staging strategy that supports atomic replacement and cleanup without prescribing a language or API.

## References

* [Python reference](references/index.md) - Identifies the supplied Python implementation as informative source material and records its provenance.
