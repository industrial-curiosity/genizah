---
type: Plan
title: Spec Bundle Repository Implementation Plan
description: Task-by-task implementation plan for repurposing the map-generator package as an OKF specification-bundle repository.
tags:
  - ai-agents
  - okf
  - specification-bundles
  - implementation-plan
status: complete
sources:
  - id: repository-design
    resource: ../specs/2026-08-25-spec-bundle-repository-design.md
    title: Spec Bundle Repository Design
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification
---

<!-- markdownlint-disable MD025 -->

# Spec Bundle Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repurpose the current .NET package repository as an OKF-based library
of technology-neutral specification bundles with distributed tag discovery,
authoring automation, a customization-interview skill, and pull-request
validation.

**Architecture:** Authored bundle metadata lives only in each
`bundles/<id>/index.md`. A Python standard-library builder validates bundles and
materializes small generated indexes under `tags/`; a separate generator copies
a strict template into new bundle directories. A portable repo skill interviews
users before adapting bundle specifications, and a read-only GitHub Actions
workflow validates changed bundles and proves generated indexes are committed.

**Tech Stack:** Python 3.13 standard library, Markdown with constrained YAML
frontmatter, OKF 0.2, `unittest`, and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-25-spec-bundle-repository-design.md`

## Global Constraints

- Bundle specifications and strategies remain technology-neutral.
- Every bundle index targets `okf_version: "0.2"` and follows the repository's
  strict heading/list contract.
- Authors are non-empty opaque strings. Names, GitHub usernames, organizations,
  email addresses, and mixed lists are valid.
- Tags are unique lowercase kebab-case strings; one-word tags are valid and
  encouraged when they improve discovery.
- Every non-reserved bundle Markdown concept has `type`, `title`, `description`,
  `tags`, and `sources`, including at least one external documentation URL.
- Bundle indexes are authoritative; everything under `tags/` is generated.
- Generated output is deterministic and is never partially written after a
  validation failure.
- Python tooling uses only the standard library and supports the documented
  Markdown/YAML subset rather than arbitrary YAML.
- The initial bundle authors are exactly `@therightstuff` and
  `industrial-curiosity`.
- Implementation samples are optional and illustrative only. They are never
  required bundle content, acceptance tests, or conformance evidence. The
  initial bundle retains no staged C# source or tests.
- The customization skill is portable: no IDE-specific tools, user-home paths,
  or external personal skills appear in its body.
- CI has read-only contents permission, runs on every pull-request code update,
  and never commits, pushes, comments, or uses secrets.
- Git writes are intentionally absent. Do not stage, commit, push, tag, or open
  a pull request without a separate explicit user instruction.

---

## File Structure

<!-- markdownlint-disable MD013 -->

| Path | Responsibility |
| --- | --- |
| `scripts/build-index.py` | Parse bundle indexes, validate selected concepts, render the complete tag tree, and support build/check modes. |
| `scripts/generate-bundle.py` | Validate a new bundle ID, copy the bundle template without overwriting, and replace ID/title tokens. |
| `templates/bundle/` | Minimum invalid-until-authored OKF bundle skeleton. |
| `tests/test_build_index.py` | Parser, validation, safe-generation, deterministic-output, and selective-validation tests. |
| `tests/test_generate_bundle.py` | Bundle scaffolding, token replacement, and no-overwrite tests. |
| `tests/test_repository_content.py` | Initial-bundle technology-neutral and sample-free content checks. |
| `tests/test_skill.py` | Portable skill structure, trigger, resource, and output-contract checks. |
| `tests/test_workflow.py` | GitHub Actions trigger, permissions, version pinning, changed-bundle, and Git-drift contract checks. |
| `bundles/versioned-procedural-map-generation/` | First technology-neutral, implementation-sample-free bundle. |
| `tags/` | Generated root tag listing and one index directory per tag. |
| `.agents/skills/customize-spec-bundle/` | Downloadable interview/adaptation skill, references, and eval prompts. |
| `.github/workflows/validate-bundles.yml` | Read-only pull-request validation and generated-index drift check. |
| `index.md` | Short OKF root navigation to bundles, tags, authoring docs, and the skill. |
| `README.md` | GitHub orientation and primary local commands. |
| `docs/bundle-format.md` | Detailed bundle/index/concept/reference authoring contract. |

<!-- markdownlint-enable MD013 -->

### Task 1: Parse and validate authoritative bundle indexes

**Files:**

- Create: `scripts/build-index.py`
- Create: `tests/__init__.py`
- Create: `tests/test_build_index.py`

**Interfaces:**

- Produces: `BundleMetadata`, `ValidationIssue`,
  `parse_bundle_index(index_path, bundle_root)`, and
  `validate_bundle_identifier(bundle_id)`.
- Consumed by: concept validation, tag generation, selective CI validation, and
  `scripts/generate-bundle.py` behavior tests.

- [x] **Step 1: Write failing index-parser tests**

Create temporary repositories in `BundleIndexParsingTests`. The first valid
fixture must mix the supported author forms and include both compound and
one-word tags:

```python
VALID_INDEX = '''---
okf_version: "0.2"
---

# Replayable Maps

Deterministic procedural map generation with version-owned inputs.

## Authors

* Jane Example
* @therightstuff
* industrial-curiosity
* maps@example.com

## Tags

* procedural-maps
* maps

## Specifications

* [Core specification](specification.md) - Normative behavior.
'''

def test_parses_mixed_authors_and_one_word_tags(self):
    metadata = self.run_parser_fixture("replayable-maps", VALID_INDEX)
    self.assertEqual(metadata["authors"], [
        "Jane Example", "@therightstuff", "industrial-curiosity",
        "maps@example.com",
    ])
    self.assertEqual(metadata["tags"], ["procedural-maps", "maps"])
```

Add focused failures for an invalid directory ID, missing H1, blank
description, missing/reordered required sections, empty authors, exact duplicate
authors, invalid tags, duplicate tags, and a specification bullet without a
local Markdown link.

- [x] **Step 2: Run the parser tests and confirm the expected failure**

Run:

```text
python3 -m unittest tests.test_build_index.BundleIndexParsingTests -v
```

Expected: FAIL because `scripts/build-index.py` and its CLI do not exist.

- [x] **Step 3: Implement the strict index parser**

Define immutable records and exact validation entry points:

```python
@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    line: int
    message: str

@dataclass(frozen=True)
class BundleMetadata:
    bundle_id: str
    title: str
    description: str
    authors: tuple[str, ...]
    tags: tuple[str, ...]
    specification_paths: tuple[Path, ...]
    index_path: Path
    bundle_root: Path

def validate_bundle_identifier(bundle_id: str) -> list[str]:
    if BUNDLE_ID_PATTERN.fullmatch(bundle_id):
        return []
    return ["Bundle identifiers must use lowercase kebab-case."]
```

Implement `parse_bundle_index(index_path: Path, bundle_root: Path) ->
tuple[BundleMetadata | None, list[ValidationIssue]]` with the grammar below.

Implement these exact rules:

- `BUNDLE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")`.
- Frontmatter contains only `okf_version: "0.2"` between the opening and
  closing `---` delimiters.
- Exactly one H1 appears after frontmatter.
- The description is the non-empty paragraph between H1 and `## Authors`, with
  wrapped lines joined by one space.
- Required H2 sections occur once and in this order: `Authors`, `Tags`,
  `Specifications`.
- Author values are trimmed and otherwise preserved; exact duplicates fail.
- Tags match `BUNDLE_ID_PATTERN`; duplicates fail.
- Specification bullets match
  `* [title](relative-path.md) - non-empty description`.
- Additional H2 sections are allowed and parsed only for their local links.

Add `--root PATH` to make repository fixtures testable. Centralize terminal
errors in `main()` so parser helpers return issues instead of printing. Start
the file with `#!/usr/bin/env python3` and mark it executable.

- [x] **Step 4: Run the parser tests**

Run:

```text
python3 -m unittest tests.test_build_index.BundleIndexParsingTests -v
```

Expected: PASS with all valid metadata preserved and every malformed fixture
reported with its file and source line.

- [x] **Step 5: Review checkpoint**

Review only `scripts/build-index.py` and the parser test class. Confirm there is
no tag-writing behavior yet and no Git write has been performed.

### Task 2: Validate concepts and generate distributed tag indexes

**Files:**

- Modify: `scripts/build-index.py`
- Modify: `tests/test_build_index.py`

**Interfaces:**

- Consumes: `BundleMetadata` and `ValidationIssue` from Task 1.
- Produces: `validate_bundle_concepts(metadata)`,
  `render_tag_tree(bundles)`, `compare_tag_tree(root, desired)`, and
  `write_tag_tree(root, desired)`.
- CLI: `build-index.py [--root PATH] [--check] [--bundles [ID ...]]`.

- [x] **Step 1: Write failing concept-validation tests**

Add fixtures that exercise the repository's constrained OKF frontmatter:

```python
VALID_CONCEPT = '''---
type: Strategy
title: Deterministic replay
description: Freeze every operation that consumes pseudo-random state.
tags:
  - determinism
sources:
  - id: pcg-paper
    resource: https://www.pcg-random.org/paper.html
    title: The PCG Paper
---

# Deterministic replay

The generator must version its random algorithm and consumption order.[^pcg-paper]

[^pcg-paper]: The PCG Paper
'''
```

Add failures for missing `type`, `title`, `description`, `tags`, `sources`, an
external `https://` resource, a missing local link, a `../` link that escapes
the bundle, and an unresolved `REPLACE_` or `{{TOKEN}}` template marker.

- [x] **Step 2: Write failing tag-generation and safety tests**

Cover two bundles sharing `maps`, deterministic ordinal ordering, repeated
authors in rendered entries, `tags/index.md`, one generated tag directory per
tag, `--check` drift without writes, a stale marked tag directory, an untracked
new generated directory, and refusal to replace or delete an unmarked
`tags/<tag>/index.md`.

Assert the exact generated entry:

<!-- markdownlint-disable MD013 -->

```markdown
* [Replayable Maps](../../bundles/replayable-maps/) - Deterministic procedural map generation with version-owned inputs. Authors: Jane Example, @therightstuff, industrial-curiosity, maps@example.com.
```

<!-- markdownlint-enable MD013 -->

- [x] **Step 3: Run the new tests and confirm failure**

Run:

<!-- markdownlint-disable MD013 -->

```text
python3 -m unittest tests.test_build_index.ConceptValidationTests tests.test_build_index.TagGenerationTests -v
```

<!-- markdownlint-enable MD013 -->

Expected: FAIL because concept validation and tag rendering are not implemented.

- [x] **Step 4: Implement concept and link validation**

Implement a line-oriented frontmatter reader for the documented subset. It must
return top-level scalar keys, block-list tags, source IDs, and source resources;
it must not claim general YAML support.

```python
def validate_bundle_concepts(metadata: BundleMetadata) -> list[ValidationIssue]:
    """Validate every non-reserved Markdown concept below one bundle."""

def resolve_bundle_link(
    bundle_root: Path,
    document_path: Path,
    raw_target: str,
) -> tuple[Path | None, str | None]:
    """Resolve local links and reject paths outside bundle_root."""
```

Ignore `http://`, `https://`, `mailto:`, and fragment-only links during local
existence checks. Treat a leading `/` as bundle-root-relative. Resolve every
candidate path before comparing it with the resolved bundle root. Validate
reserved `index.md` files using the index grammar rather than the concept
frontmatter grammar.

- [x] **Step 5: Implement deterministic rendering and safe writes**

Use this exact generated marker:

```python
GENERATED_MARKER = "<!-- Generated by scripts/build-index.py. Do not edit. -->"
```

`render_tag_tree()` returns `dict[Path, str]` relative to `tags/`. Sort tag
names, bundle IDs, and generated entries with Python's default ordinal string
ordering. Write each file to a temporary sibling and replace it with
`os.replace()` only after all validation passes.

Before removing stale generated directories, require their `index.md` to begin
with `GENERATED_MARKER` and require the directory to contain only that file.
Report any unmarked collision and write nothing.

Define CLI semantics precisely:

- No `--bundles` flag: validate all bundle concepts.
- `--bundles` with zero or more IDs: fully validate only existing named IDs,
  but parse every bundle index and regenerate the complete tag tree.
- `--check`: compare desired and actual generated files, report changed/missing/
  stale paths, and never write.
- Exit `0` only for a valid, current check or a successful build; exit `1` for
  validation errors, collisions, or drift.

- [x] **Step 6: Run the builder tests**

Run:

```text
python3 -m unittest tests.test_build_index -v
```

Expected: PASS, including safe handling of stale generated directories and
non-writing check mode.

- [x] **Step 7: Review checkpoint**

Confirm all terminal errors originate in `main()`, helper functions are
side-effect-free except `write_tag_tree()`, and no file outside the supplied
repository root can be read or written through bundle metadata.

### Task 3: Add the bundle template and safe generator

**Files:**

- Create: `templates/bundle/index.md`
- Create: `templates/bundle/specification.md`
- Create: `templates/bundle/validation.md`
- Create: `templates/bundle/strategies/strategy.md`
- Create: `templates/bundle/references/index.md`
- Create: `scripts/generate-bundle.py`
- Create: `tests/test_generate_bundle.py`

**Interfaces:**

- Produces CLI:
  `generate-bundle.py [--root PATH] BUNDLE_ID [--title DISPLAY_TITLE]`.
- Consumed by README authoring instructions and CI tests.

- [x] **Step 1: Write failing generator tests**

Use a temporary repository containing a copied `templates/bundle/`. Cover
default title derivation, explicit `--title`, invalid IDs, missing template,
existing destination, no partial directory after failure, and progress output
listing every created path.

```python
def test_generates_named_bundle_without_overwriting(self):
    result = self.run_generator("sample-bundle", "--title", "Sample Bundle")
    self.assertEqual(result.returncode, 0)
    index = self.root / "bundles/sample-bundle/index.md"
    self.assertIn("# Sample Bundle", index.read_text(encoding="utf-8"))
    self.assertNotIn("{{BUNDLE_ID}}", index.read_text(encoding="utf-8"))
```

- [x] **Step 2: Run the generator tests and confirm failure**

Run:

```text
python3 -m unittest tests.test_generate_bundle -v
```

Expected: FAIL because the template and generator do not exist.

- [x] **Step 3: Create the strict template**

Use only two automatically replaced tokens: `{{BUNDLE_ID}}` and
`{{BUNDLE_TITLE}}`. Use explicit unresolved markers such as
`REPLACE_WITH_DESCRIPTION`, `REPLACE_WITH_AUTHOR`, `REPLACE_WITH_TAG`,
`REPLACE_WITH_SOURCE_URL`, and `REPLACE_WITH_EVIDENCE` everywhere an author must
supply real content. Task 2's validator must reject those markers.

Every concept template contains complete OKF field names and these body
sections:

```markdown
# {{BUNDLE_TITLE}}

## Problem

REPLACE_WITH_DESCRIPTION

## Invariants

* REPLACE_WITH_INVARIANT

## Customization points

* REPLACE_WITH_CUSTOMIZATION_POINT

## Evidence

REPLACE_WITH_EVIDENCE[^source]

[^source]: REPLACE_WITH_SOURCE_TITLE
```

The validation template uses `Given`, `When`, and `Then` headings; the strategy
template adds `Alternatives`, `Tradeoffs`, and `Failure modes`. The references
index explains that raw files require a linked `Reference` concept.

- [x] **Step 4: Implement the generator**

Use `argparse`, `pathlib`, and `shutil.copytree`. Validate the identifier before
creating anything. Reject an existing target with one error that names the path
and tells the user to choose another ID or remove it themselves. Do not add an
overwrite flag. Start the file with `#!/usr/bin/env python3` and mark it
executable.

```python
def derive_title(bundle_id: str) -> str:
    return " ".join(part.capitalize() for part in bundle_id.split("-"))

def generate_bundle(root: Path, bundle_id: str, title: str) -> list[Path]:
    template = root / "templates" / "bundle"
    destination = root / "bundles" / bundle_id
    # Validate every precondition, then copy once and replace known tokens.
```

After success, print the created files in sorted order and print:

```text
Next: replace every REPLACE_ marker, then run python3 scripts/build-index.py
```

- [x] **Step 5: Run template and generator tests**

Run:

```text
python3 -m unittest tests.test_generate_bundle tests.test_build_index -v
```

Expected: PASS, including builder rejection of an unedited generated bundle.

### Task 4: Author the versioned procedural map-generation bundle

**Files:**

- Create: `bundles/versioned-procedural-map-generation/index.md`
- Create: `bundles/versioned-procedural-map-generation/specification.md`
- Create: `bundles/versioned-procedural-map-generation/validation.md`
- Create: `bundles/versioned-procedural-map-generation/strategies/deterministic-replay.md`
- Create: `bundles/versioned-procedural-map-generation/strategies/version-owned-inputs.md`
- Create: `bundles/versioned-procedural-map-generation/strategies/template-composition-and-selection.md`
- Create: `bundles/versioned-procedural-map-generation/strategies/placement-and-reachability.md`

**Interfaces:**

- Produces: the first independently downloadable, validator-clean bundle.
- Consumed by: generated tag indexes, skill eval prompts, README examples, and
  future CLI/MCP consumers.

- [x] **Step 1: Create the authoritative bundle index**

Set authors to exactly:

```markdown
## Authors

* @therightstuff
* industrial-curiosity
```

Set tags to:

```markdown
## Tags

* deterministic-generation
* procedural-maps
* seeded-randomness
* maps
* seeds
* procedural
* determinism
* versioning
* generation
* templates
* graphs
```

Link the specification, validation concept, and four strategy concepts with
one-sentence descriptions.

- [x] **Step 2: Run validation to expose the missing concepts**

Run:

```text
python3 scripts/build-index.py --check
```

Expected: FAIL with missing-path errors for every linked concept and no writes
under `tags/`.

- [x] **Step 3: Write the technology-neutral specification**

Use `type: Specification`. Define inputs, outputs, invariants, customization
points, failure behavior, and the generation flow. Preserve these requirements:

- A seed carries entropy plus a generator version.
- The selected version owns every replay-affecting input and algorithm.
- Configuration is validated and frozen before random state is consumed.
- Template graphs are acyclic; candidate lists have stable ordering.
- Shapes, transforms, layers, selectors, and connectors are data-defined.
- Reachability is validated from an explicit start location.
- Caller-seed execution does not silently allocate a replacement seed.

Use these exact external sources in OKF frontmatter and claim footnotes:

- `https://www.pcg-random.org/paper.html`
- `https://learn.microsoft.com/en-us/dotnet/api/system.random?view=net-10.0`
- `https://yaml.org/spec/1.2.2/`
- `https://owasp.org/www-community/attacks/Path_Traversal`
- `https://xlinux.nist.gov/dads/HTML/breadthfirst.html`
- `https://xlinux.nist.gov/dads/HTML/depthfirst.html`

State explicitly that the Microsoft documentation demonstrates both same-seed
replay and the risk of different sequences across runtime versions; it is
evidence for version-owning the random algorithm, not a mandate to use .NET.

- [x] **Step 4: Write the four focused strategy concepts**

Assign evidence as follows:

- `deterministic-replay.md`: PCG paper and Microsoft `System.Random`
  documentation; explain algorithm identity, state consumption order, stable
  candidate ordering, and replay test vectors.
- `version-owned-inputs.md`: YAML 1.2.2 and OWASP Path Traversal; explain
  immutable version folders, relative references, canonicalized confinement,
  include-cycle detection, and schema customization.
- `template-composition-and-selection.md`: NIST depth-first search; explain
  graph validation, recursion-cycle rejection, selector matching, ordinal sort,
  and deterministic selection.
- `placement-and-reachability.md`: NIST breadth-first search; explain mask
  transforms, occupancy, connector edges, start-cell rules, and graph
  reachability without prescribing grid storage.

Each strategy distinguishes invariants from choices the customization skill
must ask about.

- [x] **Step 5: Write portable acceptance scenarios**

Use `type: Validation` and Given/When/Then groups covering:

- Same version, seed, inputs, and algorithm produce the same ordered output.
- A version change may intentionally change output without corrupting replay of
  an older version.
- Unknown seed versions fail before loading inputs.
- Escaping and missing references fail before generation.
- Include and template cycles fail with a traceable cycle path.
- Selector candidate order is stable before random selection.
- Disabled transforms are never applied.
- Unreachable required features cause one generation failure.
- A caller-provided invalid seed is not silently replaced.

Use the OKF specification URL as the external source for the validation
document's evidence and provenance structure.

- [x] **Step 6: Keep the initial bundle free of implementation samples**

Do not copy the staged C# source or tests into the bundle. Confirm the bundle
contains no `references/csharp/`, C# files, or sample-test material. Portable
requirements and acceptance scenarios belong in the normative specification
and validation concepts.

- [x] **Step 7: Generate and validate tag indexes**

Run:

```text
python3 scripts/build-index.py
python3 scripts/build-index.py --check
```

Expected: both commands exit `0`; `tags/index.md` and all eleven tag directories
exist, and every generated entry attributes `@therightstuff` and
`industrial-curiosity`.

### Task 5: Build the portable customization-interview skill

**Files:**

- Create: `.agents/skills/customize-spec-bundle/SKILL.md`
- Create: `.agents/skills/customize-spec-bundle/references/interview-coverage.md`
- Create: `.agents/skills/customize-spec-bundle/references/output-contract.md`
- Create: `.agents/skills/customize-spec-bundle/evals/evals.json`
- Create: `tests/test_skill.py`

**Interfaces:**

- Consumes: a local or downloaded bundle directory and an optional target
  repository.
- Produces: a target implementation profile and customized specification draft
  in conversation; writes files only after the user supplies a path and asks.

- [x] **Step 1: Write failing deterministic skill tests**

Test the required frontmatter, resources, portability, and eval inventory:

```python
def test_skill_description_covers_every_entry_point(self):
    frontmatter, body = self.read_skill()
    description = frontmatter["description"].lower()
    for trigger in ("apply", "adapt", "customize"):
        self.assertIn(trigger, description)
    self.assertIn("explicit", body.lower())

def test_skill_has_no_machine_or_host_specific_paths(self):
    text = self.skill_path.read_text(encoding="utf-8")
    for forbidden in ("/Users/", "~/.agents/", ".cursor/", "Composer"):
        self.assertNotIn(forbidden, text)
```

Also require both referenced Markdown files, at least seven eval cases, a
non-empty `type: Agent Skill`, `name`, and `description`, and no missing
resource links.

- [x] **Step 2: Run the skill tests and confirm failure**

Run:

```text
python3 -m unittest tests.test_skill -v
```

Expected: FAIL because the skill directory does not exist.

- [x] **Step 3: Write the interview and output references**

`interview-coverage.md` is an OKF `Guide` concept. It requires the agent to:

- Read discoverable target-repository facts before asking the user.
- Extract bundle invariants, choices, alternatives, failures, and validation
  scenarios.
- Ask one unresolved question at a time.
- Cover domain, language/runtime, integration, data/persistence, determinism,
  compatibility, security, scale/performance, operations, failure policy,
  testing, and excluded scope only when relevant.
- Stop when every applicable customization point has a recorded fact, user
  decision, explicit deviation, or unresolved blocker.

`output-contract.md` is an OKF `Guide` concept. Define these exact sections:

```markdown
# Target implementation profile

## Discovered facts
## User decisions
## Bundle invariants retained
## Deliberate deviations
## Unresolved questions

# Customized specification draft

## Purpose
## Target environment
## Requirements
## Selected strategies
## Failure behavior
## Acceptance scenarios
## Provenance
```

- [x] **Step 4: Write the concise portable skill**

Use frontmatter:

```yaml
---
type: Agent Skill
name: customize-spec-bundle
description: >-
  Use when a user asks to apply, adapt, or customize a specification bundle for
  a concrete implementation, or explicitly invokes this skill.
---
```

The body uses imperative, host-agnostic instructions. It tells the agent when to
read each bundled reference, separates discovered facts from user decisions,
forbids silently weakening invariants, and requires user review before writing
the customized spec to disk.

- [x] **Step 5: Add eval prompts**

Create `evals/evals.json` with these cases and expected assertions:

- New project with no repository: asks target questions one at a time.
- Existing repository: reads discoverable language/runtime facts before asking.
- Conflicting latency and determinism requirements: explains the tradeoff.
- User rejects an invariant: records a deliberate deviation.
- User stops answering: returns unresolved questions without inventing choices.
- Unknown optional concept type: tolerates it and continues progressive loading.
- Optional implementation sample with tests: treats both as illustrative and
  non-normative, does not run or port the tests as required work, and derives
  conformance from the validation concept.

- [x] **Step 6: Run skill tests and perform the repo-scope coherence review**

Run:

```text
python3 -m unittest tests.test_skill -v
```

Expected: PASS.

Then scan frontmatter and headings for every repo skill under `.agents/skills/`.
Expected: `customize-spec-bundle` has no overlapping repo-scope skill owner, its
description covers all body triggers, and its body contains no cross-scope
references.

- [x] **Step 7: Run the qualitative skill evals**

Run each case from `evals/evals.json` in a fresh agent context with only the
skill, the case's bundle fixture, and its target context loaded. Record whether
the output satisfies every assertion: progressive bundle loading, repository
inspection before questions, one question at a time, fact/decision separation,
explicit deviation handling, illustrative-sample boundaries, and the
output-contract headings.

Expected: every case passes without invented target choices. If a case fails,
revise the skill or its bundled references, rerun `tests.test_skill`, and repeat
that case before continuing.

### Task 6: Write repository orientation and contribution documentation

**Files:**

- Replace: `README.md`
- Create: `index.md`
- Create: `docs/bundle-format.md`
- Modify: `.gitignore`
- Preserve: `LICENSE`

**Interfaces:**

- Consumes: final builder, generator, bundle, tags, and skill paths.
- Produces: concise human/agent orientation plus detailed authoring rules.

- [x] **Step 1: Rewrite README as an OKF guide**

Add OKF frontmatter with `type: Guide`, the canonical OKF specification as a
source, and one H1. Keep the body at orientation level:

- Repository purpose and direct-agent workflow.
- Browse `bundles/` directly or discover through `tags/`.
- Generate a bundle with `python3 scripts/generate-bundle.py example-bundle`.
- Validate/build with `python3 scripts/build-index.py`.
- Check drift with `python3 scripts/build-index.py --check`.
- Download/install `.agents/skills/customize-spec-bundle/` from the repository
  path and invoke it with a bundle plus target implementation.
- Link `docs/bundle-format.md`, the initial bundle, the skill, and OKF.

Attribute the sample and repository examples to `@therightstuff` and
`industrial-curiosity`.

- [x] **Step 2: Create the root OKF index**

Use only `okf_version: "0.2"` frontmatter. Link to `bundles/`, `tags/`,
`docs/bundle-format.md`, the bundle generator, and the customization skill. Do
not enumerate every bundle.

- [x] **Step 3: Write the detailed bundle-format concept**

Use `type: Guide` and cite the canonical OKF specification. Document the exact
index grammar, author identity rules, tag rules, concept fields, evidence links,
reference files, generated-tag ownership, template markers, builder modes,
generator no-overwrite behavior, and PR checks.

- [x] **Step 4: Update ignore rules and verify docs**

Replace .NET-only `bin/` and `obj/` patterns with:

```gitignore
.DS_Store
__pycache__/
*.py[cod]
```

Run:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/build-index.py --check
```

Expected: PASS with no generated drift.

### Task 7: Add pull-request validation with changed-bundle selection

**Files:**

- Create: `.github/workflows/validate-bundles.yml`
- Create: `tests/test_workflow.py`

**Interfaces:**

- Consumes: PR base/head SHAs and `build-index.py --bundles`.
- Produces: read-only PR checks and actionable workflow summaries.

- [x] **Step 1: Write failing workflow contract tests**

Read the workflow as text and assert all non-negotiable controls:

```python
def test_workflow_runs_on_each_pr_code_update(self):
    text = self.workflow.read_text(encoding="utf-8")
    for event in ("opened", "reopened", "synchronize"):
        self.assertIn(event, text)
    self.assertNotIn("paths:", text)

def test_workflow_is_read_only_and_checks_git_drift(self):
    text = self.workflow.read_text(encoding="utf-8")
    self.assertIn("contents: read", text)
    self.assertIn("git status --porcelain", text)
    self.assertNotIn("git push", text)
```

Also assert `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, Python
`3.13`, `fetch-depth: 0`, `persist-credentials: false`, PR-number concurrency,
the base/head SHA contexts, unit-test discovery, and `build-index.py` invocation.

- [x] **Step 2: Run the workflow tests and confirm failure**

Run:

```text
python3 -m unittest tests.test_workflow -v
```

Expected: FAIL because the workflow does not exist.

- [x] **Step 3: Implement the read-only workflow**

Use this job-level shape:

```yaml
name: Validate bundles

on:
  pull_request:
    types: [opened, reopened, synchronize]

permissions:
  contents: read

concurrency:
  group: validate-bundles-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

Checkout the PR head SHA with full history and credentials disabled. Set up
Python 3.13. Run all `unittest` tests first.

In one `shell: python` step, use `subprocess.run()` with argument arrays to:

1. Run `git diff --name-status -z BASE_SHA HEAD_SHA -- bundles/`.
2. Collect unique existing bundle IDs for added, copied, modified, renamed, and
   type-changed paths; retain deletion information only for the summary.
3. Detect changes below `scripts/`, `templates/`, `tests/`, `.agents/skills/`,
   `docs/bundle-format.md`, and the workflow itself.
4. Run `python3 scripts/build-index.py` for a full validation when a contract or
   tool path changed; otherwise run `python3 scripts/build-index.py --bundles`
   followed by the existing changed bundle IDs.
5. Run `git status --porcelain=v1 --untracked-files=all -- tags/` and fail when
   any output remains.

The step owns `write_failure_summary(reason)` and `fail(reason)`. It writes an
`::error::` command, the affected bundle/path list, and
`python3 scripts/build-index.py` as remediation before exiting non-zero. On
success, append the validated bundle list and current-index confirmation to
`GITHUB_STEP_SUMMARY`.

- [x] **Step 4: Run workflow and full tests**

Run:

```text
python3 -m unittest tests.test_workflow -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: PASS. Local tests verify the repository's workflow contract; GitHub
will perform final workflow compilation when the workflow is pushed later under
separate user authorization.

### Task 8: Remove the package implementation and verify the repurposed repository

**Files:**

- Delete: `MapGenerator.sln`
- Delete: `src/MapGenerator/GeneratedMap.cs`
- Delete: `src/MapGenerator/MapConfigurationLoader.cs`
- Delete: `src/MapGenerator/MapDefinition.cs`
- Delete: `src/MapGenerator/MapGenerator.cs`
- Delete: `src/MapGenerator/MapGenerator.csproj`
- Delete: `src/MapGenerator/MapSeed.cs`
- Delete: `src/MapGenerator/TemplateCatalog.cs`
- Delete: generated `src/MapGenerator/bin/` and `src/MapGenerator/obj/`
- Delete: `tests/MapGenerator.Tests/MapConfigurationLoaderTests.cs`
- Delete: `tests/MapGenerator.Tests/MapDefinitionTests.cs`
- Delete: `tests/MapGenerator.Tests/MapGenerator.Tests.csproj`
- Delete: `tests/MapGenerator.Tests/MapSeedTests.cs`
- Delete: `tests/MapGenerator.Tests/TemplateCatalogTests.cs`
- Delete: `tests/MapGenerator.Tests/VersionedMapGeneratorTests.cs`
- Delete: generated `tests/MapGenerator.Tests/bin/` and
  `tests/MapGenerator.Tests/obj/`
- Delete: `docs/superpowers/specs/2026-08-23-versioned-map-generator-design.md`
- Delete: `docs/superpowers/plans/2026-08-23-versioned-general-map-generator.md`

**Interfaces:**

- Consumes: the completed technology-neutral bundle from Task 4.
- Produces: a repository whose only product is specification bundles and their
  authoring/discovery tooling.

- [x] **Step 1: Confirm the initial bundle contains no implementation samples**

Run `python3 -m unittest tests.test_repository_content -v` and inspect the
bundle tree. Expected: the bundle has no `references/` directory or C# files,
and its index has no `References` section. No byte-copy preservation gate
applies.

- [x] **Step 2: Delete only the listed legacy artifacts**

Use explicit file deletions; do not recursively remove the repository root,
`docs/superpowers/`, `tests/`, or another broad directory. Remove now-empty
`src/MapGenerator/` and `tests/MapGenerator.Tests/` directories only after
deleting their exact generated `bin/` and `obj/` subdirectories and confirming
they contain no other unlisted files.

- [x] **Step 3: Run complete verification**

Run:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/build-index.py --check
python3 -m unittest tests.test_generate_bundle -v
rg -n "REPLACE_" templates/bundle
test ! -e src
test ! -e tests/MapGenerator.Tests
```

Expected:

- All Python tests pass.
- Generated tag indexes are current.
- The focused generator tests pass, including no-overwrite and no-partial-copy
  cases.
- Template markers are present only in `templates/bundle/`, where they are
  intentional.
- Both legacy project paths are absent.

- [x] **Step 4: Inspect final repository scope**

Run:

```text
rg --files -g '!docs/superpowers/plans/2026-08-25-spec-bundle-repository.md' | sort
```

Expected: only the license, OKF docs, bundle/template/tag trees, Python tooling
and tests, portable skill, workflow, and approved design/plan remain. Confirm no
package publication instructions, root C# project files, or monolithic catalog
exist.

- [x] **Step 5: Final review checkpoint**

Report verification counts, any unavailable external check, the exact files
removed, and that the initial bundle contains no implementation samples. Do not
stage or commit the completed work without explicit user authorization.

## Completion Record

- 2026-08-28: All 44 implementation-plan steps are complete and checked off.
- 2026-08-28: Seven isolated qualitative skill eval cases passed all 21 assertions.
- 2026-08-28: The complete Python and Node test suites passed, generated indexes had no drift, and the npm dry-run package contained only the declared files.
- 2026-08-28: The npm test workflow failure path now emits an annotation and actionable step summary; its regression test passes.
- 2026-08-28: Live GitHub catalog reachability and a hosted GitHub Actions run remain intentionally unverified until the initial catalog commit is available remotely.
