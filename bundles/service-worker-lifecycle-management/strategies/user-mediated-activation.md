---
type: Strategy
title: User-mediated service-worker activation
description: Compare a waiting worker with the current page and ask for a user decision when activation requires a client transition.
tags:
  - service-workers
  - progressive-web-apps
  - pwa
  - lifecycle-management
sources:
  - id: service-worker-register
    resource: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register
    title: ServiceWorkerContainer register method
  - id: controller-change
    resource: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controllerchange_event
    title: ServiceWorkerContainer controllerchange event
---

# User-mediated service-worker activation

## Problem

Activating an update changes which worker controls future requests. Reloading before that change can show stale assets; activating without notice can interrupt data entry or an in-progress task. A waiting worker from the same release may need activation without changing the page.

## Strategy

1. Register the worker and check for updates on the adopted schedule. Record only successful checks so a failed check can be retried.
2. Observe a candidate already waiting or installed later. If no worker controls the page, treat it as initial installation and leave the update decision hidden.
3. Compare the candidate's reported release identity with the current page. Treat an absent or invalid reply as an unverifiable identity.
4. If the identities match and the adopted safety policy permits it, confirm that the candidate still waits and activate it without a prompt or reload.
5. For a different or unverifiable identity, present one durable, accessible update decision that explains the effect of accepting it. Keep the active controller in place until the user accepts, unless the adopter's documented immediate-activation policy applies.
6. On acceptance, preserve in-progress state, request candidate activation, and wait for the controller-change signal.
7. After that signal, reload or make the documented state transition exactly once.
8. If the candidate disappears, activation fails, or the signal does not arrive by the adopted timeout, preserve the current client and present a truthful retry or refresh action.

## Invariants

* The update decision identifies a candidate update; it does not promise activation before controller change.
* Only one update prompt represents one candidate state at a time.
* A missing identity reply cannot justify silent activation under the matching-release policy.
* A reload caused by the update follows controller change, not the activation request.
* A failed or abandoned activation leaves a usable client and does not erase unsaved state solely to retry.

## Customization choices

* Prompt placement, wording, accessibility behavior, and whether a deferred prompt reappears.
* Release identity format, how the page and worker share it, and how long to wait for a candidate reply.
* Periodic check schedule, minimum interval, and where successful checks are recorded.
* Immediate-activation eligibility, including data-loss and compatibility criteria.
* Activation request mechanism, timeout, retry policy, and post-activation transition.
* How an active client identifies a candidate when registration is managed by application tooling.

## Alternatives and tradeoffs

Immediate activation reduces time spent on an old version but can disrupt an active task and create a mixed-version session. Waiting for consent preserves user control and gives the application time to protect unsaved state, at the cost of serving the old controller longer. A nonblocking prompt generally balances these goals when the application cannot prove immediate activation is safe.

## Failure modes

* A prompt shown for every lifecycle event can produce duplicate controls and conflicting activation requests.
* Reloading immediately after the activation request can race the controller change and retain old controlled assets.
* Treating a registration request as offline readiness can mislead users before the worker has installed its required resources.
* Allowing untrusted worker identities or overly broad scope can let a worker control unintended requests.

## Evidence

The registration API creates or updates a registration for a scope and matches documents to the most-specific applicable scope.[^service-worker-register] The controller-change event fires when a new active worker gains control, making it the reliable boundary before a reload or state transition.[^controller-change]

[^service-worker-register]: [ServiceWorkerContainer register method](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register)

[^controller-change]: [ServiceWorkerContainer controllerchange event](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controllerchange_event)
