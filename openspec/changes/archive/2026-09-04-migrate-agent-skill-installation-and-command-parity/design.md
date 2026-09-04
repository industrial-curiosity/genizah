## Context

The legacy Superpowers SDD record documents a completed implementation of a
catalog skill installer, catalog search, local development commands, and their
tests. OpenSpec is now the project planning system, so the durable behavioral
contract must move into capability specifications. The published command and
its local counterpart recently diverged on `--force`, demonstrating that the
contract must explicitly cover every supported execution variant.

## Goals / Non-Goals

**Goals:**

- Establish OpenSpec as the active requirements source for catalog skill
  installation and catalog search.
- Define testable parity requirements for published, remote, local, offline,
  and test command variants.
- Require safe defaults and exact recovery instructions for recoverable
  refusals.
- Preserve the legacy record as migration provenance until this change is
  completed and archived.

**Non-Goals:**

- Reimplement completed installer or search behavior solely for migration.
- Delete the legacy Superpowers record during planning.
- Verify live catalog reachability as part of an offline specification
  migration.

## Decisions

### Migrate requirements, not task reports

Three capability specifications capture enduring system behavior: installation,
search, and command-variant parity. Historical reports, review notes, and
point-in-time verification evidence remain in the legacy record because they
do not define future behavior.

Alternative: copy every legacy document into OpenSpec. Rejected because it
would turn a requirements source into an investigation archive and duplicate
obsolete task boundaries.

### Treat command variants as one public interface

Published and local command paths may differ in their invocation prefix or
catalog source, but every documented option and alias with the same capability
has the same behavior and diagnostic contract. A command-interface change
therefore requires a wrapper sweep, documentation update, and invocation test
for every supported variant.

Alternative: document each wrapper independently. Rejected because interface
drift becomes undetectable until a user switches execution mode.

### Put recovery instructions at the failure boundary

The default behavior preserves existing user-owned files. When an explicit
override is available, the failure itself names the exact rerun flag and its
effect. Stable flag documentation belongs in the README; failure-specific
recovery belongs in runtime output.

Alternative: send users to generic help. Rejected because the relevant
recovery is known at the failure boundary and users should not need to infer
it.

## Risks / Trade-offs

- [Legacy requirements are incomplete or superseded] → Treat the current
  implementation and its tests as additional evidence, and record only
  behavior that remains intentional.
- [Variants gain new interfaces over time] → OpenSpec configuration and the
  command-variant-parity spec require an explicit sweep and tests.
- [Migration is mistaken for completed implementation] → Keep the change
  active until all tasks, including conformance verification, are complete.

## Migration Plan

1. Add project-wide OpenSpec context and artifact rules for interface parity
   and actionable recovery.
2. Create the three capability specs from the legacy requirements and current
   command contract.
3. Verify the current implementation against the specs and close any gaps.
4. Mark the change tasks complete, assess delta-spec sync, and archive the
   completed change using the OpenSpec archive workflow.

Rollback consists of removing the new active change and restoring the prior
OpenSpec configuration from version control; the legacy record is not changed
during migration.

## Open Questions

None.
