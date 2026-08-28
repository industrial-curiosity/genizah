---
type: Agent Skill
name: customize-spec-bundle
genizah_catalog_skill: true
description: Use when a user asks to apply, adapt, or customize a specification bundle for a concrete implementation, or explicitly invokes this skill.
---

# Customize a specification bundle

Produce a traceable target implementation profile and customized specification
without inventing target choices or silently weakening the source bundle.

## Workflow

1. Read the bundle index first. Confirm the bundle directory and identify its
   normative specification, validation, strategies, references, and any
   optional concepts.
2. Load only the concepts relevant to the current decision. Start with
   normative requirements and validation, then progressively load strategies or
   references when they inform an unresolved choice. Tolerate unknown optional
   concept types: preserve their identity and continue unless their contents
   are needed.
3. Implementation samples are optional. When present, treat code, tests, and
   run instructions as illustrative and non-normative. Do not run or port
   sample tests as a required customization step, infer requirements from them,
   or use them as conformance evidence; validation concepts define conformance.
   Load a sample only when the user asks for it or it materially informs an
   unresolved implementation choice, and label any resulting guidance as
   illustrative.
4. Inspect discoverable target facts before asking the user. If a target
   repository is available, read its relevant code, configuration,
   documentation, and tests. Record evidence-backed discovered facts separately
   from user decisions.
5. Read [interview coverage](references/interview-coverage.md) when building the
   adaptation checklist. Extract the bundle's invariants, customization points,
   alternatives, failure conditions, and validation scenarios; track every
   applicable item to closure.
6. Ask one unresolved question per turn. Do not ask for facts that can be
   discovered, combine unrelated decisions, choose defaults on the user's
   behalf, or infer an answer from silence.
7. When target constraints conflict with a bundle invariant, explain the
   tradeoff. Keep the source invariant visible and record any rejected or
   weakened invariant as a deliberate deviation with rationale and provenance.
8. Stop interviewing when each applicable item is a discovered fact, user
   decision, deliberate deviation, or unresolved blocker. If the user stops
   answering, preserve unresolved questions and blockers instead of inventing
   choices.
9. Read the [output contract](references/output-contract.md) before presenting
   results. Use its headings exactly and keep discovered facts, user decisions,
   retained invariants, deviations, and unresolved questions distinct.

Return both artifacts in the conversation by default. An explicit invocation
authorizes the interview, not a filesystem change. Write to disk only after
user review and only when the user supplies an explicit path and an explicit
request to write there.
