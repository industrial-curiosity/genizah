---
type: Specification
title: Directory Checksums specification
description: Define deterministic digest inputs for a directory tree without depending on physical directory enumeration order.
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

## Purpose

Define a reproducible digest for a directory tree so consumers can detect a
change to its relevant structure, metadata, or regular-file content.

## Inputs

* A root directory.
* A digest algorithm and output representation.
* A byte encoding, record framing, and stable name comparison rule.
* A metadata projection that names the entry attributes included in the
  fingerprint.
* One policy for symbolic links and every other supported non-regular entry
  kind.

## Output

Return the digest of the root's canonical recursive record sequence, or return
one diagnosable failure when the tree cannot be read or cannot satisfy the
configured entry-kind policy.

## Invariants

* The fingerprint is derived from bytes. Text names and metadata are encoded
  with the configured unambiguous byte encoding before they affect a digest.
* Every encoded field has a type marker and a length or another unambiguous
  boundary. Different logical record sequences cannot be concatenated into the
  same digest input merely by shifting a field boundary.
* A directory record contains its selected metadata followed by one record for
  every included immediate entry, sorted by the configured stable total order
  of entry names.
* An entry record contains its name, kind, selected metadata, and, for a
  regular file or directory, the fingerprint required by its kind.
* A regular-file fingerprint is derived from the file's raw bytes.
* A directory fingerprint is derived recursively from its own canonical record
  sequence. A child digest is recorded as bytes, not as an ambiguously
  concatenated display string.
* Directory enumeration order, concurrent completion order, locale settings,
  and unspecified collection order do not affect the result.
* Symbolic links are never followed unless the configured link policy
  explicitly requires it. A non-following policy records the link's own
  configured identity rather than its target's recursive content.
* A fingerprint only represents one observed tree state. An implementation
  either reads a consistent snapshot or fails if it detects a relevant change
  while reading.

## Processing flow

1. Classify the root without following links and reject it unless it is a
   directory.
2. Create the root directory record with the configured metadata projection.
3. Enumerate immediate entries, classify each without following links, and
   filter or reject entries according to the entry-kind policy.
4. Sort included entries by the configured stable name comparison.
5. For each entry in that order, encode its name, kind, and projected metadata.
   Hash raw bytes for a regular file, recurse for a directory, and apply the
   configured leaf policy for every other included kind.
6. Digest the framed root record sequence and return its configured output
   representation.

## Customization points

* Digest algorithm, output representation, byte encoding, field framing, and
  name comparison rule.
* Metadata fields, normalization, unavailable-field policy, and whether root
  metadata is included.
* Inclusion policy for hidden entries, symbolic links, sockets, devices,
  named pipes, and platform-specific entry kinds.
* Link identity representation and whether a link target is recorded, followed,
  or rejected.
* Snapshot, locking, retry, and concurrent-mutation policy.
* Error taxonomy, resource limits, path-reporting policy, and whether empty
  directories have a distinct record.

## Evidence

The motivating implementation hashes regular-file content and recursively
combines sorted directory-entry names and metadata; it does not prescribe a
portable record encoding or metadata set.[^source-implementation]

[^source-implementation]: simple-recursive-checksum source repository
