---
type: Strategy
title: Unity Camera-Relative Object Hover Preview strategy
description: Derive object-preview camera distance from baseline and active lens half-angle tangents while keeping preview ownership local.
tags:
  - unity
  - object-preview
  - hover-preview
  - card-preview
  - zoom-preview
sources:
  - id: camera-fov
    resource: https://docs.unity3d.com/ScriptReference/Camera-fieldOfView.html
    title: Unity Camera.fieldOfView reference
---

# Unity Camera-Relative Object Hover Preview

## Decision

Keep the source object's physical dimensions unchanged and adjust only its camera-space distance. Let `baselineDistance` be the configured preview distance, `baselineFov` the baseline camera's vertical field of view, and `activeFov` the active output camera's vertical field of view. Place the preview at:

```text
baselineDistance * tan(baselineFov / 2) / tan(activeFov / 2)
```

The calculation preserves the object's vertical screen proportion for perspective cameras. Unity field of view is a vertical angle in the cited API, so the inputs use a common angular measure.[^camera-fov]

## Invariants

* Use the output camera that renders the preview, not an inactive logical or authoring camera, as `activeFov`.
* Use the intended player-view lens as `baselineFov`; use its configured distance as `baselineDistance`.
* Attach the preview to the active output camera after calculating its local forward-axis distance.
* Clone source presentation state without cloning source colliders, hit testing, or input behavior.
* One presentation owner tracks the hovered source object, pending delay, and visible preview so every exit path uses the same cleanup operation.
* Treat an output-camera change as a preview-lifecycle transition: clear the pending or visible preview, then begin a new delay only if the same source object remains hovered for the new camera.

## Customization points

* Camera type, projection model, and the policy for unsupported or invalid field-of-view values.
* Whether the game uses vertical, horizontal, or another explicit screen proportion metric.
* Source-state transfer, preview rendering, and preview lifetime hooks.

## Alternatives

* A fixed camera distance is simpler but changes the preview's apparent size when camera lenses differ.
* Scaling the preview to match the source object's world projection retains relative scale but can make detail unreadable.
* Moving or resizing the source object exposes interaction-state and layout coupling that a separate preview avoids.

## Tradeoffs

* Lens-adjusted placement needs both camera lenses at preview creation time.
* The perspective-camera formula needs a separate, explicit policy for orthographic or other non-perspective projections.

## Failure modes

* An inactive or wrong output camera produces an incorrect apparent size.
* Retaining a preview across an output-camera change leaves it attached to the wrong camera or at a stale apparent size.
* A preview that retains a collider or hit target can steal hover input from its source object.
* Missing cleanup leaves a stale preview after an input or presentation-state transition.

## Evidence

The Unity camera API describes field of view as a vertical angle, which supports the strategy's vertical half-angle calculation.[^camera-fov]

[^camera-fov]: Unity Camera.fieldOfView reference
