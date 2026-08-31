---
type: Strategy
title: Canonical recursive digest
description: Create a deterministic digest by sorting directory entries and framing each recursive contribution.
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

# Canonical recursive digest

## Problem

A direct digest of directory enumeration is unstable when enumeration order is
unspecified. Concatenating variable-length names, metadata, and child digests
without framing can also make distinct tree records indistinguishable as digest
input.

## Strategy

Represent each directory as an ordered sequence of self-describing records.
First classify and filter its immediate entries, then sort their encoded names
with the configured stable total order. For each entry, encode a record tag,
name, kind, selected metadata, and an explicit payload:

* A regular-file payload is the digest of its raw bytes.
* A directory payload is the digest of its recursively constructed record
  sequence.
* A symbolic-link or special-entry payload follows the explicitly selected
  entry-kind policy.

Use fixed-width lengths, a canonical length encoding, or another injective
framing scheme before feeding record fields to the digest. Do not rely on a
delimiter that could appear in a field value.

The source implementation demonstrates the essential traversal pattern:
sorted immediate names, entry metadata, regular-file checksums, and recursive
directory checksums.[^source-implementation]

## Invariants

* Every included immediate entry contributes exactly one ordered record.
* A directory's record includes its own identity before its child records when
  root or directory metadata is configured as relevant.
* Classification and link policy are explicit before recursion begins.
* All ordering happens before records are consumed by the digest.
* Record framing preserves both field identity and field boundaries.

## Customization points

* Whether canonical names are bytewise, normalized text, or another documented
  representation.
* The metadata projection and portable substitutes for unavailable attributes.
* Whether file payloads are direct raw-byte contributions or nested file
  digests, provided the resulting record grammar remains unambiguous.
* The treatment of unreadable entries, broken links, hard links, and special
  files.

## Alternatives and tradeoffs

* Hashing only regular-file bytes is portable and cheap but cannot detect a
  rename, empty-directory change, or selected metadata change.
* Including broad platform metadata detects more state changes but reduces
  equality across copies, machines, and privilege contexts.
* A single streaming digest minimizes memory use; materializing canonical
  records first can simplify inspection and diagnostic output.

## Failure modes

* Using physical enumeration order produces different results for the same
  logical directory.
* Text conversion changes a name or metadata value before it is hashed.
* A delimiter-only encoding creates an ambiguous record boundary.
* Following a symbolic-link directory unintentionally escapes the intended
  tree or creates a recursion cycle.
* A filesystem change during traversal mixes states without a snapshot or
  detected failure.

[^source-implementation]: simple-recursive-checksum source repository
