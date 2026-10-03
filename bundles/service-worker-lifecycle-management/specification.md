---
type: Specification
title: Service Worker Lifecycle Management specification
description: Portable requirements for installing, updating, and retiring a progressive web application's service-worker registration.
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

## Purpose

Define a predictable lifecycle for the scoped background worker that can intercept a progressive web application's requests. The lifecycle must make installation, deferred activation, and retirement visible and reversible to the application owner and its users.

## Terms

* A *registration* associates one worker script with one application scope.
* A *candidate* is an installed worker that is not yet the active controller for the current client.
* *Activation* makes a candidate the controller for future client requests in its scope.
* *Retirement* ends an application-owned registration and removes only the cached data owned by that registration.

## Requirements

* The application declares the worker script and its intended scope as trusted deployment configuration. It never derives either value from untrusted input.
* The application attempts registration only where the platform supports it and its security requirements are met. A browser that cannot register the worker remains usable without worker-provided features.
* The application maintains at most one registration for each intended scope and does not intentionally create overlapping scopes. Registration uses the documented scope and treats an existing matching registration as an update opportunity rather than a second installation.[^service-worker-register]
* Registration failure leaves the application usable and reports a diagnostic that identifies the lifecycle stage without disclosing sensitive data.
* The application exposes the offline-ready state after its worker can serve the promised offline behavior. It does not claim offline readiness merely because registration was requested.
* After registration, the application evaluates whether an update check is due and reevaluates while the client remains active. It limits explicit checks to an adopted minimum interval measured from the last successful check. It records success durably; a failed check remains due for a later retry and does not make an installed worker appear unavailable.[^service-worker-update]
* Each release gives the page and its worker the same release identity. The page displays that identity in a secondary location, and a waiting worker can report its identity to the page. A missing or invalid reply never establishes that their identities match.
* The application observes both a candidate already waiting at startup and a candidate installed later. It does not present an update decision during the first installation when no worker controls the client.
* If a candidate reports the same release identity as the page, the application may activate it without prompting or reloading, provided its documented compatibility and data-safety policy makes that transition safe. It rechecks that the candidate is still waiting before requesting activation.
* If a candidate's identity differs from the page's or cannot be verified, the application makes one clear update decision available to a client already controlled by another worker. The decision states that accepting it may reload or otherwise replace the running client. The application does not automatically reload that client.
* By default, a candidate requiring a client transition does not replace the active controller until the user accepts the update. An adopter may choose immediate activation only when its documented compatibility and data-safety policy makes interruption safe.
* On accepted activation, the application preserves in-progress state, requests activation from the candidate, waits for the controller to change, and only then reloads or transitions the client once. If no candidate is waiting, it refreshes or reports that no activation is pending; it does not claim that an update was applied.[^controller-change]
* Retirement is an explicit, authorized lifecycle operation. Before or with retirement, the application stops registering the retiring worker in future releases.
* Retirement targets only registrations whose scope and identity are owned by the application. It never unregisters another application's worker or deletes cache entries outside its documented ownership boundary.
* After a successful retirement request, the application removes only application-owned caches, records the result, and verifies on a subsequent navigation or lifecycle check that the retired scope has no replacement registration. A concurrent registration can otherwise supersede an unregistration request.[^service-worker-unregister]
* A retirement failure preserves caches unless their independent ownership policy permits removal, leaves the application usable, and reports the next safe action.

## Customization choices

An adopter must record these choices:

* Worker script identity, scope, trusted origin, and supported-browser behavior.
* Offline-ready promise, registration timing, and user-visible status locations.
* Update-check schedule, minimum interval, durable success record, and failure retry behavior.
* Release identity generation, display location, candidate identity exchange, and unverifiable-identity behavior.
* Whether activation requires confirmation, how the prompt can be deferred or dismissed, and the narrow conditions for immediate activation.
* In-progress state preservation, activation timeout, reload or transition behavior, and no-candidate outcome.
* Retirement authority, app-owned registration identity, app-owned cache boundary, completion verification, and user-facing result.

Choices may add safeguards or application-specific states, but they cannot weaken scope ownership, user visibility of disruptive activation, controlled retirement, or preservation of unrelated data.

## Evidence

Registering a worker creates or updates the registration for its scope; a scope maps to a single registration, and overlapping scopes are discouraged.[^service-worker-register] An explicit update check attempts to fetch the worker script and installs it if it differs from the current script.[^service-worker-update] The controller-change event marks the point at which a new active worker takes control.[^controller-change] An unregister request can be overtaken by a new registration, so retirement needs a later verification step.[^service-worker-unregister]

[^service-worker-register]: [ServiceWorkerContainer register method](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register)

[^service-worker-unregister]: [ServiceWorkerRegistration unregister method](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/unregister)

[^controller-change]: [ServiceWorkerContainer controllerchange event](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controllerchange_event)

[^service-worker-update]: [ServiceWorkerRegistration update method](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update)
