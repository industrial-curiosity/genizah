## ADDED Requirements

### Requirement: Return deterministic catalog search results
The catalog search command SHALL normalize duplicate search terms, evaluate
generated catalog indexes, and return matching candidates in deterministic
order. Full matches SHALL rank ahead of partial matches without changing the
relative order of otherwise equal candidates.

#### Scenario: Full and partial matches
- **WHEN** a query has both full and partial catalog matches
- **THEN** the result lists full matches before partial matches and preserves
  candidate order within each match class

### Requirement: Emit machine-readable search output
The published catalog search command SHALL emit one JSON document to standard
output and SHALL reject missing search terms or unsupported search options with
a nonzero failure.

#### Scenario: Search with terms
- **WHEN** a user invokes the published search command with one or more terms
- **THEN** standard output contains one JSON result document

#### Scenario: Search without terms
- **WHEN** a user invokes the published search command without a term
- **THEN** the command fails with an actionable missing-term diagnostic

### Requirement: Fail clearly for unusable catalog data
The catalog search command SHALL reject catalog HTTP failures and malformed
generated catalog content instead of returning inferred or partial results.

#### Scenario: Catalog index is malformed
- **WHEN** a fetched catalog index does not have the expected generated format
- **THEN** the command fails with a diagnostic that identifies the unusable
  catalog data
