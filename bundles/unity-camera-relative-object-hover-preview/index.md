---
okf_version: "0.2"
---

# Unity Camera-Relative Object Hover Preview

A Unity interaction contract for temporarily presenting an eligible scene object at a readable, camera-relative size without changing the source object or its state.

## Authors

* Adam Fisher

## Tags

* unity
* object-preview
* hover-preview
* card-preview
* zoom-preview

## Specifications

* [Core specification](specification.md) - Defines delayed, state-preserving Unity object previews with lens-adjusted placement.

## Validation

* [Acceptance scenarios](validation.md) - Defines Unity-specific checks for eligibility, cleanup, dimensions, and screen proportion.

## Strategies

* [Lens-adjusted presentation](strategies/strategy.md) - Defines the camera-distance calculation and preview lifecycle ownership.
