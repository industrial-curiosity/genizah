---
type: Specification
title: Durable atomic file writes specification
description: A portable contract for safely and durably replacing file contents.
tags:
  - atomic-writes
  - file-writing
  - file-systems
  - durability
  - durable-file-system-safety
  - safe-writes
sources:
  - id: python-reference
    resource: https://gist.github.com/therightstuff/cbdcbef4010c20acc70d2175a91a321f
    title: Safe atomic file writes for JSON and YAML in Python 3
---

<!-- markdownlint-disable MD013 MD025 -->

# Durable Atomic Replacement Contract

## Problem

Provide an operation that replaces a destination file with supplied contents without exposing a partially written destination. A successful operation must make the new contents durable according to the selected storage durability policy. A failed operation must leave the previously committed destination intact whenever the underlying file system provides the required atomic replacement guarantee.

The operation accepts file contents, a destination path, and a write mode. The default mode is replacement. Append mode is optional only when the implementation can define its atomic and durable semantics explicitly; it must not be silently treated as replacement.

## Required behavior

1. Stage the new contents in a file on the same file system as the destination.
2. Write all supplied contents to the staged file.
3. Make the staged file's contents durable before committing it, using the platform's supported synchronization operation.
4. Commit by one atomic replacement operation that changes the destination from its previous state to the staged file.
5. Report success only after the commit operation succeeds.
6. Remove an uncommitted staged file on every failure path when removal is possible.
7. Never expose the staging path as the destination path.

If the destination already exists, preserve the attributes required by the selected policy. The default policy preserves the destination's portable permission and ownership attributes when the platform permits those operations; timestamp and platform-specific attributes may be included by configuration. If the destination does not exist, use the implementation's documented creation policy.

The operation must support text or binary content according to the caller's content type. It must reject unsupported modes before modifying the destination.

## Invariants

* An observer sees either the previously committed file or the fully committed new file, never a partially written file at the destination path.
* A successful replacement does not depend on moving a staged file across file systems.
* A failed staging, synchronization, or commit operation does not claim success.
* A failed operation does not intentionally delete or truncate the previously committed destination.
* A staged file is not left behind after a completed operation or a handled failure, unless cleanup itself fails and that failure is reported or made observable according to the error policy.
* The operation's durability guarantee is explicitly documented; flushing application buffers alone is insufficient to claim storage durability.
* The committed file's encoding and content equal the supplied content under the selected content contract.

## Customization points

* Whether append mode is supported, and the exact semantics of an append transaction.
* Which permission, ownership, timestamp, and platform-specific attributes are preserved.
* Whether a missing parent directory is rejected or created.
* The storage durability level promised by synchronization, including whether the containing directory is synchronized after replacement.
* How permission failures, synchronization failures, replacement failures, and cleanup failures are represented.
* Whether replacement follows symbolic links or rejects them, based on the security policy of the consuming system.
* The content abstraction and encoding rules for text and binary data.

## Failure behavior

The implementation must distinguish a failed operation from a successful operation whose cleanup produced a warning. If the destination may have changed but the commit result is indeterminate, the result must be reported as indeterminate rather than successful, and the caller must be given enough information to reconcile the destination.

The implementation must not use an unconditional broad exception handler that hides staging, synchronization, replacement, or cleanup failures. Cleanup errors must retain the original failure as the primary cause while remaining observable.

## Evidence

The supplied Python reference stages a file in the destination directory, copies existing metadata, flushes and synchronizes the staged file, atomically replaces the destination, and removes the staged file in a cleanup path.[^python-reference]

[^python-reference]: [Safe atomic file writes for JSON and YAML in Python 3](https://gist.github.com/therightstuff/cbdcbef4010c20acc70d2175a91a321f)
