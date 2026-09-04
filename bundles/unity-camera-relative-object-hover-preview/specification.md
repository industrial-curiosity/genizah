---
type: Specification
title: Unity Camera-Relative Object Hover Preview specification
description: Define a delayed, non-interactive Unity scene-object preview that preserves source state and screen proportion across camera lenses.
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

## Purpose

A Unity scene object in a world or tabletop layout can be too small to inspect. An eligible source object needs a temporary readable presentation that does not move, resize, disable, reveal, or otherwise alter the source object.

## Invariants

* A preview is created only while one eligible source object remains continuously hovered for the configured delay.
* The preview preserves the source object's visual identity, including its rendered appearance, orientation, and physical dimensions.
* The source object remains at its original position and keeps its interaction and application state.
* The preview is non-interactive and cannot replace the source object as the hover target.
* Leaving the source object, changing targets, or leaving the enclosing presentation state removes any pending or visible preview immediately.
* Changing the active output camera while the source object remains hovered cancels any pending or visible preview; a replacement preview may begin only after the same source object has remained hovered for the configured delay against the new camera.
* The baseline preview distance is measured along the selected Unity camera's forward axis and is configured for one baseline camera lens.
* For a camera with a different vertical field of view, the system adjusts the preview distance so that an unchanged physical object occupies the same vertical screen proportion as it does at the baseline lens.

## Requirements

* The system accepts a source Unity `GameObject`, an eligibility predicate, a hover delay, a baseline camera vertical field of view, a baseline preview distance, and the active output camera vertical field of view.
* After continuous hover of an eligible source object for the configured delay, the system creates one preview attached to the active output camera.
* The preview has no collider, selection behavior, or independent hover behavior.
* When the active output camera uses the baseline vertical field of view, the preview distance equals the configured baseline distance.
* When the active output camera uses another vertical field of view, the preview distance equals the baseline distance multiplied by the tangent of half the baseline field of view divided by the tangent of half the active field of view.
* The system removes the preview and cancels any pending delay when the source object ceases to be eligible, the hover target changes, the hover ends, or the presentation is reset or cleaned up.
* The system cancels any pending or visible preview when the active output camera changes. It starts a replacement only after the source object remains continuously hovered for the configured delay with that camera active.

## Customization points

* Eligible object states and source-identity rules.
* Hover delay, baseline vertical field of view, and baseline preview distance.
* Preview cloning or rendering, camera attachment, and cleanup lifecycle.
* The screen axis used for proportionality when the game uses a non-vertical presentation metric.

## Evidence

Unity defines camera field of view as a vertical angle in degrees, which supports expressing the placement calculation in terms of vertical half-angle tangents.[^camera-fov]

[^camera-fov]: Unity Camera.fieldOfView reference
