---
type: Agent Skill
name: bundle-authoring
description: Use when creating, naming, or reviewing a specification bundle or its discovery tags; confirm consumer-facing identity before authoring.
---

# Author a specification bundle

## Bundle identity

Before creating or renaming a bundle, inspect the source material and propose
two to four generalized names that describe the reusable core offering rather
than a source implementation, algorithm, or incidental storage form. Give a
short reason for each suggestion, recommend one when the evidence supports it,
and invite the user to supply an alternative.

Before writing a bundle index or regenerating discovery indexes, propose the
candidate discovery tags with a short searchability and accuracy rationale.
Ask the user to confirm or revise both the selected name and tag set. Do not
silently choose either consumer-facing identity when the user has not confirmed
it.

## Discovery tags

Derive bundle-index tags from the core offering: the primary capability,
domain, and distinguishing guarantees stated by the title, description, and
normative specification. Cover each relevant discovery dimension when it
meaningfully helps a consumer find the bundle.

Do not tag a supporting algorithm, data structure, validation technique, or
implementation mechanism unless that subject is itself a core offering of the
bundle. Keep tags unique and avoid near-duplicate synonyms that do not improve
discovery.

After changing discovery tags, update the bundle index and regenerate the
derived tag index as specified by the repository's bundle-format guide.

## Normative content

Keep normative specifications, strategies, and validation scenarios independent
of named languages, runtimes, libraries, products, and unrelated projects. Do
not label a bundle or its description as technology-neutral; apply that property
in the content. Name an external project only in a reference or when it is
directly part of the specified behavior.
