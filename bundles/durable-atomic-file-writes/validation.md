---
type: Validation
title: Durable atomic file writes validation
description: Portable acceptance scenarios for durable atomic file replacement.
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

<!-- markdownlint-disable MD013 MD024 MD025 -->

# Durable Atomic Replacement Acceptance Scenarios

## Problem

Verify that a file-write operation provides its documented atomicity, durability, replacement, metadata, and cleanup guarantees across success and failure paths.

## Scenario: replace an existing file

### Given

* A destination file contains committed old content.
* The caller supplies different new content.
* The destination and staging location are on one file system.

### When

* The caller performs a replacement write and the operation reports success.

### Then

* Reading the destination returns exactly the new content.
* No read of the destination during the operation returns a partial prefix, suffix, or mixture of old and new content.
* The destination remains present at its original path.

## Scenario: preserve selected attributes

### Given

* A destination file exists with attributes included in the selected preservation policy.

### When

* The caller successfully replaces its contents.

### Then

* The selected attributes of the committed file match the recorded pre-write attributes, subject to documented platform limitations.

## Scenario: reject unsupported mode

### Given

* The caller supplies a mode outside the implementation's documented mode set.

### When

* The caller starts the operation.

### Then

* The operation fails before modifying the destination.
* The failure identifies the unsupported mode.

## Scenario: failure before commit

### Given

* A destination file contains committed old content.
* Staging or synchronization is forced to fail before replacement.

### When

* The caller performs the write.

### Then

* The operation reports failure.
* The destination still contains the old content.
* The staged file is removed when cleanup is possible.

## Scenario: cleanup failure

### Given

* The operation fails and removal of the staged file also fails.

### When

* The caller receives the operation result.

### Then

* The original staging, synchronization, or replacement failure remains identifiable as the primary failure.
* The cleanup failure is observable.
* The result is not reported as a successful write.

## Scenario: durable success

### Given

* The platform provides a documented synchronization operation for file contents.

### When

* The operation reports success.

### Then

* Synchronization of the staged file completed before replacement.
* The implementation's documented durability policy is satisfied, including directory synchronization when that policy requires it.

## Evidence

These scenarios are derived from the supplied Python reference's staging, metadata-copy, synchronization, replacement, and cleanup behavior.[^python-reference]

[^python-reference]: [Safe atomic file writes for JSON and YAML in Python 3](https://gist.github.com/therightstuff/cbdcbef4010c20acc70d2175a91a321f)
