---
type: Agent Skill
name: bundle-authoring
description: Use when creating or reviewing a specification bundle or its discovery tags; keep normative content technology-neutral and select tags for the core offering, not supporting mechanics.
---

# Author a specification bundle

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
