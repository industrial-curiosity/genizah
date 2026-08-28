# Genizah Agent Skill Installation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide `npx genizah init` to install Genizah discovery and customization skills, `npx genizah search` to deterministically search the GitHub catalog, and a local development installer usable before the catalog is pushed.

**Architecture:** A dependency-free Node package in `tooling/npm/` owns the CLI, installation transaction, and catalog client. The installation transaction fetches the two skill trees from the GitHub catalog before staging them. A new bundle defines skill-directory selection. The installed discovery skill invokes the CLI, waits for the user to confirm a recommendation, then delegates to the installed customization skill using only the confirmed GitHub-hosted bundle concepts.

**Tech Stack:** Node.js 18+ standard library, `node:test`, Python `unittest`, Markdown/OKF bundle documents, GitHub raw-content endpoints.

**Spec:** `docs/superpowers/specs/2026-08-28-genizah-agent-skill-installation-design.md`

## Global Constraints

- The catalog is `industrial-curiosity/genizah`; do not clone or vendor it into target projects.
- The npm package lives entirely under `tooling/npm/` and has no runtime dependencies.
- `search` writes JSON only to standard output; errors go to standard error with a nonzero exit code.
- `init` writes only below a relative skill location contained by its current working directory.
- `.agents/skills` is the default project-level location; the user selects alternatives before writes.
- A recommendation never starts customization before the user confirms a selected bundle.
- Bundle specifications omit implementation technologies and unrelated projects.
- Feature implementation and documentation precede the comprehensive test and validation task.
- Until the initial catalog commit is pushed, GitHub operations use mocked `fetch`; do not perform a live reachability check.

---

## File Structure

| Path | Responsibility |
| --- | --- |
| `bundles/ai-agent-skill-installation/` | Portable installation requirements, strategy, validation, and compatibility reference. |
| `tooling/npm/package.json` | Package metadata, Node version floor, executable, and publishable file set. |
| `tooling/npm/bin/genizah.mjs` | Thin executable that maps CLI failures to stderr and exit codes. |
| `tooling/npm/bin/local-init.mjs` | Local-development executable that derives the catalog checkout from itself and installs into a named target project. |
| `tooling/npm/lib/cli.mjs` | Parses `init` and `search` commands and dispatches their dependencies. |
| `tooling/npm/lib/skill-locations.mjs` | Declares supported project-level locations and validates selected paths. |
| `tooling/npm/lib/install-skills.mjs` | Selects a location, fetches catalog skill trees, and transactionally installs them. |
| `tooling/npm/lib/catalog-search.mjs` | Fetches and parses the GitHub tag tree, ranks candidates, and builds JSON. |
| `tooling/npm/test/` | Node unit and integration tests using temporary directories and stubbed `fetch`. |
| `tests/test_agent_skill_installation_bundle.py` | Repository-level checks for the new bundle and generated tag entries. |
| `README.md` and `docs/bundle-format.md` | User-facing installation and discovery documentation. |
| `.github/workflows/validate-bundles.yml` | Runs the npm package tests on pull requests. |

## Task 1: Add the Agent Skill Installation Bundle

**Files:**

- Create: `bundles/ai-agent-skill-installation/index.md`
- Create: `bundles/ai-agent-skill-installation/specification.md`
- Create: `bundles/ai-agent-skill-installation/strategies/project-location-selection.md`
- Create: `bundles/ai-agent-skill-installation/validation.md`
- Create: `bundles/ai-agent-skill-installation/references/agentskills-support.md`
- Create: `tests/test_agent_skill_installation_bundle.py`
- Modify: `tags/index.md`
- Create: `tags/agent-skills/index.md`
- Create: `tags/agent-installation/index.md`

**Interfaces:**

- Consumes: the repository bundle format and the bundled compatibility reference.
- Produces: the `ai-agent-skill-installation` bundle and generated discovery tags used by the package design.

- [x] **Step 1: Author the bundle and reference**

Create an OKF index titled **AI Agent Skill Installation**. Tag its core offering with `agent-skills`, `agent-installation`, and `ai-agents`. Add a specification requiring choice-before-write, one selected destination, a portable default, override support, prior-install reuse, contained relative paths, and actionable reporting. Add a strategy that distinguishes known project-level locations from user-profile locations. Add validation scenarios for default, selected, noninteractive, repeat, invalid-path, and no-partial-install behavior.

Copy the supplied Panopticon support document into `references/agentskills-support.md`, preserving its body and source links while adding the repository-required OKF frontmatter (`type`, `title`, `description`, `tags`, and external `sources`). Do not make Panopticon names normative in the specification.

- [x] **Step 2: Regenerate the tag tree**

Run: `python3 scripts/build-index.py`

Expected: the complete generated `tags/` tree includes `agent-skills` and `agent-installation` entries for the new bundle.

## Task 2: Scaffold the Dependency-Free npm Package and Command Dispatcher

**Files:**

- Create: `tooling/npm/package.json`
- Create: `tooling/npm/bin/genizah.mjs`
- Create: `tooling/npm/lib/cli.mjs`
- Create: `tooling/npm/test/cli.test.mjs`

**Interfaces:**

- Consumes: CLI arguments and injected command handlers.
- Produces: `main(arguments, dependencies)` returning an exit status; package executable `genizah`.

- [x] **Step 1: Add package metadata and minimal dispatcher**

Set package name to `genizah`, use ESM, require Node `>=18`, expose `bin/genizah.mjs` as `genizah`, and restrict package contents to `bin/`, `lib/`, `README.md`, and `LICENSE`. Add no dependencies. Implement `init` with optional `--skills-dir RELATIVE_PATH` and `search TERM...`; reject missing search terms and unknown options. Keep command behavior in `lib/cli.mjs`; the bin wrapper only calls `main`, writes a single error message to stderr, and sets a nonzero exit code.

## Task 3: Implement Skill Location Selection and Transactional Installation

**Files:**

- Create: `tooling/npm/lib/skill-locations.mjs`
- Create: `tooling/npm/lib/install-skills.mjs`
- Create: `tooling/npm/test/install-skills.test.mjs`
- Modify: `tooling/npm/lib/cli.mjs`

**Interfaces:**

- Consumes: `skillsDir`, current working directory, terminal input/output, and fetched GitHub catalog skill paths.
- Produces: `{ location, installedSkillNames }` or a clear failure before target-project writes.

- [x] **Step 1: Implement deterministic destination selection**

Define the ordered de-duplicated project-level location list from the new bundle reference: `.agents/skills`, `.github/skills`, `.claude/skills`, `.cursor/skills`, `.codex/skills`, `.opencode/skills`, and `.pi/skills`. Prefer an explicit `--skills-dir`; otherwise reuse the first location containing `genizah/SKILL.md`; otherwise prompt and accept a list number, blank default, or relative literal path. Print the compatibility choices before the prompt.

Resolve every destination against `cwd`; reject absolute input and any resolved location outside `cwd`. Never write a second location during one invocation.

- [x] **Step 2: Implement the installation transaction**

Fetch the discovery skill and customization skill tree from the GitHub catalog before target-project writes. Stage the fetched bytes in a temporary sibling directory. Before replacement, verify that existing destination directories are Genizah-owned by their expected `SKILL.md` identity; refuse to replace unrelated directories. Move existing owned directories to a transaction backup, move staged directories into place, then remove the backup. On any failure, remove newly moved directories and restore the backup. Preserve all unrelated skills in the selected location.

Fetch both skill trees directly from the catalog. The discovery skill calls `npx --yes genizah search`, inspects target facts, recommends without selecting, waits for confirmation, loads only confirmed GitHub bundle concepts, then follows `customize-spec-bundle`.

## Task 4: Implement the Local Development Installer and Documentation

**Files:**

- Create: `tooling/npm/bin/local-init.mjs`
- Modify: `tooling/npm/package.json`
- Modify: `tooling/npm/lib/install-skills.mjs`
- Create: `tooling/npm/README.md`
- Modify: `README.md`
- Modify: `docs/bundle-format.md`

**Interfaces:**

- Consumes: a target-project path passed after `npm run local:init --` and the local package path.
- Produces: the same installation result as normal `init`, sourced from the local checkout without network access.

- [x] **Step 1: Add local source installation**

Add `npm run local:init -- TARGET_PROJECT`. Resolve `TARGET_PROJECT` from
`INIT_CWD`, so this works from another project's cwd:

```sh
npm --prefix ../genizah/tooling/npm run local:init -- .
```

The script derives the catalog root from its own location, reads the two skill
trees directly from that root, uses no network, and delegates location selection
and transaction behavior to the shared installer.

- [x] **Step 2: Document normal and local invocation**

Document normal GitHub installation, the local pre-push command, supported skill
locations, search JSON, confirmation, and customization handoff.

## Task 5: Implement Deterministic GitHub Tag Search

**Files:**

- Create: `tooling/npm/lib/catalog-search.mjs`
- Create: `tooling/npm/test/catalog-search.test.mjs`
- Modify: `tooling/npm/lib/cli.mjs`

**Interfaces:**

- Consumes: `TERM...`, a GitHub `fetch` implementation, and catalog owner/repository/ref constants.
- Produces: a JSON-compatible object `{ terms, candidates }` with stable candidate ordering.

- [x] **Step 1: Implement catalog reads and parsing**

Use `fetch` against `https://raw.githubusercontent.com/industrial-curiosity/genizah/main/tags/index.md`. Parse tag links from that committed index, select every tag with an exact or substring query-term match, fetch only those tag pages, and de-duplicate candidate bundle IDs. Fetch each candidate bundle index to read its complete tag list. Parse only the repository's documented generated-index and bundle-index forms; reject malformed content rather than guessing.

Normalize terms to lowercase, discard duplicate empty terms, and give each term one match per bundle: exact tag equality wins over substring matching. Sort by descending `score`, descending `matchedTermCount`, descending `fullMatches.length`, then ascending `bundleId` with an explicit Unicode code-point comparator. Return the fields defined by the design, with arrays in deterministic order.

- [x] **Step 2: Connect `search` to JSON-only CLI output**

For `genizah search TERM...`, serialize the returned object once with `JSON.stringify(result, null, 2)` followed by a newline. Do not emit progress messages to stdout. Send network, HTTP, and parse failures to stderr through the bin wrapper with the requested catalog path.

## Task 6: Add Tests, CI, and Final Validation

**Files:**

- Create: `tooling/npm/README.md`
- Modify: `README.md`
- Modify: `docs/bundle-format.md`
- Modify: `.github/workflows/validate-bundles.yml`
- Create: `tooling/npm/test/package-contents.test.mjs`
- Modify: `tests/test_workflow.py`

**Interfaces:**

- Consumes: the installed package layout and project workflow.
- Produces: user instructions, CI coverage, and a package-content contract.

- [x] **Step 1: Add the complete test suite**

Add Node tests for CLI dispatch, location selection, transactional installation,
direct GitHub fetches with mocked responses, local source installation without
network access, deterministic ranking and tie-breaking, malformed catalog
content, and package contents. Add Python bundle and workflow tests.

- [x] **Step 2: Extend CI without adding dependencies**

Add a Node setup step using the package's declared supported Node version. Run `node --test tooling/npm/test/*.test.mjs` before bundle validation. Keep the workflow read-only and do not use `npm install`; the package has no dependencies. Extend workflow tests to assert that exact command and setup behavior.

- [x] **Step 3: Run the complete local verification set**

Run: `node --test tooling/npm/test/*.test.mjs && python3 -m unittest discover -s tests -p 'test_*.py' && python3 scripts/build-index.py --check`

Expected: all Node and Python tests pass, and generated tags have no drift.

- [x] **Step 4: Inspect the npm package contents without publishing**

Run from `tooling/npm/`: `npm pack --dry-run`

Expected: package contents include only the declared package files and exclude repository tests, catalog bundles, and generated tags. The dependency-free package has no production dependency graph to audit.

## Plan Review

- Spec coverage: Tasks 1–6 cover the installation bundle, selected-location rules, GitHub-fetched skills, local pre-push installation, search scoring, GitHub-only catalog access, confirmation gate, documentation, CI, and package contents.
- Testing order: tests and verification for all remaining work run in Task 6, after implementation and documentation.
- Placeholder scan: completed; no implementation placeholder remains in task instructions.
- Type consistency: `main`, `installSkills`, and `searchCatalog` are named consistently across the tasks that define and consume them.

## Completion Record

- 2026-08-28: Seven isolated qualitative eval cases passed all 21 assertions.
- 2026-08-28: The complete Node and Python test suites passed; generated indexes had no drift; the npm dry-run package contained only the declared files.
- 2026-08-28: The npm test workflow failure path was updated to emit an annotation and actionable step summary.
