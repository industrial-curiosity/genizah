---
okf_version: "0.2"
---

# Directory Checksums

A portable contract for deriving one deterministic digest from a directory's
names, selected entry metadata, regular-file bytes, and nested directories.

## Authors

* Adam Fisher

## Tags

* checksums
* directory-checksums
* recursive-checksums
* file-integrity
* filesystem-integrity

## Specifications

* [Core specification](specification.md) - Defines the observable directory-fingerprint contract.

## Validation

* [Acceptance scenarios](validation.md) - Defines portable checks for fingerprint stability and change detection.

## Strategies

* [Canonical recursive digest](strategies/canonical-recursive-digest.md) - Defines stable traversal and unambiguous digest input encoding.

## References

* [Source implementation](references/simple-recursive-checksum.md) - Records the implementation that motivated this bundle.
