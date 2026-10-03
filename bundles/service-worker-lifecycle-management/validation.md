---
type: Validation
title: Service Worker Lifecycle Management validation
description: Portable acceptance scenarios for registration, periodic update checks, version-aware activation, and controlled retirement of an application-owned service worker.
tags:
  - service-workers
  - progressive-web-apps
  - pwa
  - lifecycle-management
sources:
  - id: service-worker-register
    resource: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register
    title: ServiceWorkerContainer register method
  - id: service-worker-unregister
    resource: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/unregister
    title: ServiceWorkerRegistration unregister method
  - id: controller-change
    resource: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controllerchange_event
    title: ServiceWorkerContainer controllerchange event
  - id: service-worker-update
    resource: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update
    title: ServiceWorkerRegistration update method
---

# Service Worker Lifecycle Management

## Scope

These scenarios assess observable lifecycle behavior without prescribing a programming language, worker library, user-interface toolkit, cache implementation, or test framework. The platform's registration, controller-change, and unregistration semantics supply the lifecycle context.[^service-worker-register][^controller-change][^service-worker-unregister]

## Scenario: Unsupported platform

### Given

A client on a platform without service-worker support or required registration security conditions.

### When

The application starts.

### Then

It remains usable without attempting an unsupported registration and does not claim offline readiness.

## Scenario: First installation

### Given

A supported client, no existing registration for the documented scope, and a trusted worker script.

### When

The application starts its registration lifecycle.

### Then

It creates one registration for the documented scope, reports registration failure without breaking the application if it cannot complete, and announces offline readiness only after the adopted readiness condition is met. It does not offer a reload for the first installation when no worker controls the client.

## Scenario: Due update check

### Given

A registered worker and no durable record of a successful update check within the adopted minimum interval.

### When

The client starts or its periodic check runs.

### Then

It requests an update check and records a successful check only after the request succeeds.[^service-worker-update]

## Scenario: Recent and failed checks

### Given

A registered worker and a periodic update-check schedule.

### When

A check is considered before the minimum interval has elapsed, or a due check fails.

### Then

The recent check is skipped. A failed due check remains due for a later retry and does not erase an already installed worker's readiness.

## Scenario: Matching release identity

### Given

A built release and a controlled page with a waiting candidate that reports the same release identity as the page.

### When

The application observes the candidate and confirms it is still waiting.

### Then

The page visibly identifies the release, and the page and worker use the same identity. Under the adopted safe-activation policy, the application activates the candidate without an update prompt or page reload.

## Scenario: Deferred update

### Given

An active controller, a waiting candidate with a different or unverifiable release identity, and a user who has not accepted the update.

### When

The application observes the candidate.

### Then

It exposes one clear update decision, continues under the active controller, and does not reload or claim the candidate is active.

## Scenario: Accepted update

### Given

A waiting candidate and a user who accepts the update.

### When

The application requests activation.

### Then

It preserves in-progress state and waits for a controller change before reloading or transitioning the client once. If no candidate is waiting, it refreshes or reports the absence of a pending activation without reporting a successful update.

## Scenario: Authorized retirement

### Given

An authorized retirement request, an application-owned registration and cache namespace, and unrelated registrations and caches on the same origin.

### When

The application retires its worker.

### Then

It stops future registration of the retiring worker, requests unregistration only for the application-owned registration, removes only application-owned cached data after a successful request, and verifies later that no replacement registration controls the retired scope. Unrelated registrations and caches remain unchanged.

## Scenario: Retirement failure

### Given

An authorized retirement request whose unregistration operation fails or cannot be confirmed.

### When

The application handles the result.

### Then

It preserves caches unless its independent ownership policy permits removal, remains usable, and reports the failure and next safe action.

[^service-worker-register]: [ServiceWorkerContainer register method](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register)

[^service-worker-unregister]: [ServiceWorkerRegistration unregister method](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/unregister)

[^controller-change]: [ServiceWorkerContainer controllerchange event](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controllerchange_event)

[^service-worker-update]: [ServiceWorkerRegistration update method](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update)
