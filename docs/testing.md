# Testing

Run the checks from the repository root.

## Node CLI

Run the complete npm CLI suite with:

```sh
node --test tooling/npm/test/*.test.mjs
```

Node.js is the only prerequisite; the package has no dependencies. The suite
uses temporary target projects and covers published command dispatch, local
wrappers, catalog search, transactional installation, and command-option
parity. Passing output reports every test as successful with no failures.

## Bundle catalog

Run the Python tests and verify the generated tag tree with:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build-index.py --check
```

The second command must report no generated-index drift. Run it after changes
to bundle metadata, catalog indexes, or index-generation logic.

## Package contents

Preview the npm package without publishing it:

```sh
(cd tooling/npm && npm pack --dry-run --json)
```

The output must list only the package's declared distributable files.
