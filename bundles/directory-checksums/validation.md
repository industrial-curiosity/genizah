---
type: Validation
title: Directory Checksums validation
description: Verify stable directory fingerprints and observable reactions to structural, metadata, and content changes.
tags:
  - checksums
  - directory-checksums
  - recursive-checksums
  - file-integrity
  - filesystem-integrity
sources:
  - id: source-implementation
    resource: https://github.com/therightstuff/simple-recursive-checksum
    title: simple-recursive-checksum source repository
---

# Directory Checksums

## Scope

These scenarios test observable outcomes without prescribing a filesystem API,
digest library, runtime, or storage format. They extend the source
implementation's unchanged-tree and changed-content checks with explicit
ordering and entry-policy expectations.[^source-implementation]

## Scenario: Unchanged tree

### Given

A stable directory tree and one complete fingerprint configuration.

### When

The directory is fingerprinted twice without a relevant change.

### Then

Both fingerprints are identical.

## Scenario: Enumeration-order independence

### Given

A directory containing at least three included entries, supplied by two
enumerators in different physical orders.

### When

Each enumeration is fingerprinted using the same configuration.

### Then

Both fingerprints are identical because entries are ordered by the configured
stable name comparison before their records are processed.

## Scenario: Regular-file content change

### Given

A stable directory tree containing a regular file.

### When

The file's raw bytes change and all other included fingerprint inputs remain
unchanged.

### Then

The directory fingerprint differs from the original fingerprint.

## Scenario: Entry rename

### Given

A stable directory tree containing one included entry.

### When

The entry is renamed without changing its included content or metadata.

### Then

The directory fingerprint differs because an entry name is a framed input.

## Scenario: Selected metadata change

### Given

A configuration that includes a mutable metadata field and a tree containing
an entry for which that field is available.

### When

Only that metadata field changes.

### Then

The directory fingerprint differs. If the field is absent from the metadata
projection, the implementation must instead document that it is not expected
to affect the fingerprint.

## Scenario: Symbolic link

### Given

A directory containing a symbolic link and a configuration whose policy does
not follow links.

### When

The directory is fingerprinted.

### Then

The implementation does not recurse into the link target and applies the
configured leaf-identity rule, or returns the configured unsupported-kind
failure.

## Scenario: Concurrent mutation

### Given

A directory whose included file changes while the directory is being read.

### When

The directory is fingerprinted.

### Then

The implementation returns a digest for a documented consistent snapshot or a
diagnosable concurrent-mutation failure; it does not claim an undocumented
mixture of states is reproducible.

## Evidence

The motivating implementation verifies that an unchanged directory is stable,
that a nested content change alters the result, and that symbolic links do not
cause a traversal error.[^source-implementation]

[^source-implementation]: simple-recursive-checksum source repository
