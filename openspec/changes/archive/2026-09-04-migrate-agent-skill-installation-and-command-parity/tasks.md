## 1. Migrate the requirements source

- [x] 1.1 Review the legacy Superpowers SDD record against the three OpenSpec
  capability specs and correct any missing durable requirement.
- [x] 1.2 Verify that `openspec/config.yaml` supplies command-variant parity
  and actionable-recovery constraints to proposal, spec, design, and task
  artifacts.

## 2. Synchronize installation command interfaces

- [x] 2.1 Extract the shared installation-option contract so published and
  local initialization paths parse `--skills-dir`, `--force`, and `-f` with
  identical validation and semantics.
- [x] 2.2 Apply the shared contract to every supported installation wrapper
  without changing each wrapper's required target-project invocation.
- [x] 2.3 Preserve transactional installation, exact ownership validation,
  symbolic-link containment checks, and non-destructive default replacement
  behavior while applying the shared contract.

## 3. Cover and document command variants

- [x] 3.1 Add regression tests for published and local initialization paths
  covering `--skills-dir`, `--force`, and `-f`.
- [x] 3.2 Add regression tests that prove an unrelated target is preserved by
  default and that every supported force variant replaces it only when invoked.
- [x] 3.3 Update README command examples and failure guidance so published and
  local invocations describe the same options and recovery path.

## 4. Verify and archive the completed migration

- [x] 4.1 Run the Node installer, local-wrapper, catalog-search, and package
  validation suites; run the repository bundle and generated-index checks
  required by the migrated installation bundle.
- [x] 4.2 Compare the completed change's delta specs with main OpenSpec specs,
  sync approved requirements, and confirm all tasks are complete.
- [x] 4.3 Archive this change through the OpenSpec archive workflow and retain
  the legacy Superpowers record as historical provenance unless its removal is
  explicitly approved.
