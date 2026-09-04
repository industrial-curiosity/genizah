# Cover Legacy Repository Contract Details Design

## Context

The existing canonical specification preserves the major bundle-repository
contract but condenses several durable details from the legacy design. This
change restores those details as additive requirements without changing the
catalog's public command interfaces.

## Goals / Non-Goals

**Goals:**

- Make the OKF index and concept-evidence contract canonical and testable.
- Preserve extensibility for optional index sections and concept types.
- Require interruption-safe generated-index replacement.
- Specify complete pull-request validation selection and reporting behavior.

**Non-Goals:**

- Change bundle content, the public CLI, or command-variant behavior.
- Copy implementation history or completed task reports from the legacy record.
- Add remote validation of external source links.

## Decisions

### Add requirements instead of expanding existing summaries

The change adds atomic requirements for the omitted details rather than
rewriting broad existing requirements. This preserves the current contract and
makes each restored behavior independently testable.

Alternative: replace the existing repository requirements with the legacy
design's full prose. Rejected because it would mix durable behavior with
historical implementation detail.

### Preserve link validation as structural only

Evidence requirements require source metadata, claim attribution, and an
absolute HTTPS source. The builder validates their shape and presence without
retrieving external resources.

Alternative: validate remote link reachability. Rejected because it would add
nondeterministic network behavior to local and pull-request validation.

### Treat an interrupted replacement as a recoverable safety boundary

The index builder completes generated output before replacing owned paths, so
an interruption leaves the prior generated tree intact or a complete new tree.

Alternative: update generated paths in place. Rejected because interruption
could leave a partial tag index.

## Risks / Trade-offs

- [Current implementation differs from the restored contract] → Apply work
  SHALL compare the builder, workflow, and tests with every new scenario and
  add the smallest conformance changes.
- [More specific requirements increase validation work] → Keep each scenario
  limited to observable catalog behavior and avoid prescribing internals.

## Migration Plan

1. Apply the delta specification to the canonical repository capability.
2. Compare the index builder, generator, workflow, and tests with each
   restored requirement.
3. Implement and validate any conformance gaps before archiving the change.

Rollback removes this unarchived change; the canonical specification remains
unchanged until archive synchronization.

## Open Questions

None.
