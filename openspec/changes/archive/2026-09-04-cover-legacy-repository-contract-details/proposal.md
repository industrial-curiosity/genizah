# Cover Legacy Repository Contract Details

## Why

The canonical specification-bundle-repository specification preserves its
major behavior but omits several durable constraints from the legacy repository
design. Those omissions leave evidence, forward compatibility, interrupted
generation, and pull-request validation behavior without a complete canonical
requirements source.

## What Changes

- Add canonical requirements for the strict OKF bundle and evidence contract.
- Require consumers and validation to tolerate documented extension points.
- Require safe, complete index replacement when generation is interrupted.
- Make pull-request validation selection, cancellation, and remediation
  reporting explicit.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `specification-bundle-repository`: Add the omitted durable repository-format,
  generation-safety, and pull-request-validation requirements.

## Impact

The catalog's canonical OpenSpec contract, index builder, validation workflow,
and their tests may need conformance updates. The public CLI interface and its
command variants are unaffected.
