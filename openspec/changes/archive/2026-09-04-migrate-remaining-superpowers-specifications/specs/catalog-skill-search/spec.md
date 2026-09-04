# Catalog Skill Search Delta

## ADDED Requirements

### Requirement: Read the authoritative catalog without project mutation

Published and remote search variants SHALL read the committed generated tag
tree from the authoritative catalog and SHALL not clone it or write to the
current project. Local, offline, and test variants SHALL use their explicit
local or stubbed source without changing query semantics or output shape.

#### Scenario: Local search

- **WHEN** a user invokes the local search variant with query terms
- **THEN** it SHALL use the local catalog source without a network request and
  return the same result schema as published search

### Requirement: Score and expose catalog matches completely

For each normalized query term, search SHALL record at most one match per
bundle, prefer an exact tag match to a partial tag match, and rank candidates
by descending weighted score, descending matched-term count, descending
full-match count, then ordinal bundle identifier. Each result SHALL include
normalized terms and each candidate's identifier, title, description, tags,
full matches, partial matches, matched-term count, and score.

#### Scenario: Ranking candidates

- **WHEN** candidates have equal weighted scores but different matched-term or
  full-match counts
- **THEN** search SHALL order them by the documented tie breakers before bundle
  identifier

### Requirement: Return valid empty results and reject unusable sources

Search SHALL return a valid JSON result with an empty candidate list when no
bundle matches. It SHALL reject unreadable, malformed, stale-substitute, or
otherwise unusable required catalog data with a nonzero diagnostic that
identifies the requested source path.

#### Scenario: No matching bundle

- **WHEN** no catalog tag matches normalized query terms
- **THEN** search SHALL emit one valid JSON result whose candidate list is
  empty

#### Scenario: Referenced tag page cannot be used

- **WHEN** a required generated tag page cannot be read or parsed
- **THEN** search SHALL fail without returning inferred, partial, or alternate
  catalog results
