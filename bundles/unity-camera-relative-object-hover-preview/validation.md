---
type: Validation
title: Unity Camera-Relative Object Hover Preview validation
description: Verify Unity object eligibility, cancellation, source preservation, and lens-adjusted preview placement.
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

## Scope

These scenarios validate observable Unity interaction behavior without prescribing a particular input package or test framework. Field of view is treated as a vertical angle, matching the cited camera reference.[^camera-fov]

## Scenario: Eligible object creates a preview after the delay

### Given

An eligible Unity scene object is hovered continuously and the configured hover delay has not yet elapsed.

### When

The delay elapses while the same object remains hovered.

### Then

Exactly one non-interactive preview is attached to the active output camera, and the source object remains unchanged.

## Scenario: Ineligible object does not create a preview

### Given

A Unity scene object is not eligible for preview, such as a disabled, hidden, or excluded object.

### When

It remains hovered longer than the configured delay.

### Then

No preview is created.

## Scenario: Baseline camera uses the configured distance

### Given

The active output camera vertical field of view equals the configured baseline field of view.

### When

An eligible object creates a preview.

### Then

The preview is placed at the configured baseline distance and retains the source object's physical dimensions, rendered appearance, and orientation.

## Scenario: Narrower lens preserves screen proportion

### Given

The active output camera has a narrower vertical field of view than the baseline camera.

### When

An eligible object creates a preview.

### Then

The preview is farther from the active camera by the specified half-angle tangent ratio and retains its source dimensions.

## Scenario: Hover transition cleans up immediately

### Given

A visible preview or pending preview delay belongs to one source object.

### When

The pointer leaves that object, hovers another target, or the enclosing presentation is reset or cleaned up.

### Then

The pending delay is cancelled and the visible preview is removed immediately.

## Scenario: Output-camera change restarts the hover delay

### Given

A source object remains hovered while a preview is pending or visible for one output camera.

### When

Another output camera becomes active.

### Then

The pending delay or visible preview is removed immediately. A replacement preview is created only after the same source object remains hovered for the configured delay with the new output camera active.

## Evidence

The vertical-field-of-view definition establishes the shared angular basis for the baseline and active-camera comparison.[^camera-fov]

[^camera-fov]: Unity Camera.fieldOfView reference
