# Cover Legacy Repository Contract Details Tasks

## 1. Restore bundle-format contract coverage

- [x] 1.1 Update catalog validation to enforce strict OKF bundle-index
  frontmatter, opaque-author normalization, source evidence, and claim-level
  attribution without remote requests.
- [x] 1.2 Add regression tests for invalid strict-frontmatter, author,
  source-evidence, and source-attribution cases.
- [x] 1.3 Verify that unknown optional index sections and unknown concept types
  remain accepted while required metadata and containment checks still fail
  invalid bundles.

## 2. Preserve generated-index safety

- [x] 2.1 Compare generated-index replacement with the interruption-safety
  requirement and implement a complete-output-before-replacement strategy if
  needed.
- [x] 2.2 Add a regression test that interrupts replacement and proves the tag
  tree remains a complete prior or desired generated tree.

## 3. Complete pull-request validation behavior

- [x] 3.1 Update the pull-request workflow to cover the required events,
  cancellation scope, changed-path selection, full-validation triggers, and
  generated-index cleanup for deleted bundles.
- [x] 3.2 Add or update workflow tests that cover changed, renamed, and deleted
  bundle paths, full-validation triggers, success reporting, and actionable
  failure remediation.

## 4. Document and verify the contract

- [x] 4.1 Update README.md and docs/spec.md to reflect the restored
  repository-format and validation architecture requirements where they affect
  contributors.
- [x] 4.2 Run the catalog validation, Python test, workflow test, Markdown,
  and strict OpenSpec validation suites; record any remaining conformance gap
  before archive.
