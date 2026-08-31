---
type: Strategy
title: Staged replacement strategy
description: Stage, synchronize, and atomically replace a destination on the same file system.
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

# Same-Directory Staged Replacement

## Decision

Use a uniquely named staging file in the destination directory. Write the complete new representation there, synchronize it, and then perform the platform's atomic same-file-system replacement. This separates construction of the new state from publication of that state.

## Requirements

* Choose a staging name that cannot collide with another active writer.
* Place the staging file in the destination's directory or another location guaranteed to share its file system.
* Close or otherwise finalize the staged file before replacement when required by the platform.
* Synchronize staged contents before publication.
* Preserve selected destination attributes before or during staging according to the consumer's policy.
* Use a replacement primitive whose atomicity and overwrite behavior are documented for the target platform.
* Clean up the staging file in both success and failure paths.

## Tradeoffs

Same-directory staging avoids cross-file-system moves and makes replacement atomic on platforms that provide atomic rename-like replacement. It consumes temporary storage and can leave an orphan if the process terminates before cleanup; callers needing stronger orphan management should add a bounded recovery policy without weakening the destination atomicity guarantee.

## Evidence

The Python reference uses a uniquely created temporary file in the destination directory, optionally copies metadata from an existing destination, synchronizes the staged file, and replaces the destination.[^python-reference]

[^python-reference]: [Safe atomic file writes for JSON and YAML in Python 3](https://gist.github.com/therightstuff/cbdcbef4010c20acc70d2175a91a321f)
