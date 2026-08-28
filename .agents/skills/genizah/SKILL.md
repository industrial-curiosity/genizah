---
type: Agent Skill
name: genizah
genizah_catalog_skill: true
description: Use when searching for specs or spec bundles, or integrating them.
---

# Genizah specification discovery

1. Inspect the target project and the user's request before choosing search terms.
2. Run `npx --yes genizah search TERM...` with terms grounded in the observed target facts.
3. Present ranked candidates and recommend one based on target facts and candidate
   descriptions. Candidates with equal scores are tied: make that clear and do
   not treat their stable display order as a preference. Do not treat a
   recommendation as a selection.
4. Wait for the user to select or explicitly confirm a bundle. Do not load bundle concepts or begin customization before that confirmation.
5. After confirmation, load the selected bundle's index and only the GitHub-hosted concepts required by `customize-spec-bundle`.
6. Hand the confirmed bundle and discovered target facts to `customize-spec-bundle`, which continues with one unresolved question at a time.
