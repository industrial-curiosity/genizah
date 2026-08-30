---
type: Reference
title: simple-recursive-checksum source implementation
description: Record the public implementation that inspired the recursive directory fingerprinting strategy.
tags:
  - checksums
  - directory-checksums
  - recursive-checksums
  - file-integrity
  - filesystem-integrity
sources:
  - id: source-repository
    resource: https://github.com/therightstuff/simple-recursive-checksum
    title: simple-recursive-checksum source repository
---

# simple-recursive-checksum source implementation

The public source repository provides the implementation evidence for this
bundle. It hashes regular-file contents and recursively combines directory
metadata, sorted entry names, and child fingerprints.[^source-repository]

Its implementation and tests are illustrative provenance, not a required
sample or conformance test. This bundle makes the strategy portable by requiring
adopters to choose canonical encodings, metadata, ordering, and entry-kind
policies explicitly.

The source repository declares the ISC license.[^source-repository]

[^source-repository]: simple-recursive-checksum source repository
