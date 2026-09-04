## ADDED Requirements

### Requirement: Select one contained project skill location
The installer SHALL select exactly one supported skill location inside the
target project before writing files. It SHALL default to the portable project
skill location, accept an explicit contained relative location, reuse an
existing Genizah-owned installation when no location is supplied, and reject
absolute, escaping, or symbolic-link-containing destinations.

#### Scenario: Explicit contained location
- **WHEN** a user supplies a supported contained relative skill location
- **THEN** the installer writes only to that location without prompting

#### Scenario: Unsafe location
- **WHEN** a selected location is absolute, escapes the target project, or has
  a symbolic-link ancestor
- **THEN** the installer fails before fetching, staging, backing up, or writing
  catalog skills

### Requirement: Install validated catalog skill trees transactionally
The installer SHALL obtain the required catalog skill files, stage them outside
the destination, validate each skill's exact catalog identity, and replace
target directories only after validation succeeds. If replacement fails, it
SHALL remove newly installed directories and restore every backed-up directory.

#### Scenario: Invalid catalog skill identity
- **WHEN** a fetched or local catalog skill lacks the exact expected identity
- **THEN** the installer fails without changing the target project

#### Scenario: Replacement failure
- **WHEN** moving a staged skill into the selected destination fails after a
  prior directory was backed up
- **THEN** the installer restores the backed-up directory and removes newly
  installed directories

### Requirement: Preserve unrelated skill directories by default
The installer SHALL replace an existing target directory only when it has the
exact Genizah ownership identity, unless the user explicitly requests force.
It SHALL leave unrelated directories unchanged by default.

#### Scenario: Unrelated target directory
- **WHEN** a target skill directory exists without the exact Genizah ownership
  identity and force is not requested
- **THEN** the installer leaves the directory unchanged and refuses installation

### Requirement: State the force recovery path for replacement refusals
The installer SHALL identify the target and state that rerunning with `--force`
or `-f` replaces it when it refuses an unrelated target directory. The default
invocation SHALL remain non-destructive.

#### Scenario: User opts into replacement
- **WHEN** a user reruns an otherwise refused installation with `--force` or
  `-f`
- **THEN** the installer replaces the conflicting target directory with the
  validated catalog skill tree
