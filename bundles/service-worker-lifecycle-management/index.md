---
okf_version: "0.2"
---

# Service Worker Lifecycle Management

A portable contract for installing, updating, and retiring a progressive web application's service-worker registration without unexpectedly changing a running application.

## Authors

* industrial-curiosity

## Tags

* service-workers
* progressive-web-apps
* pwa
* lifecycle-management

## Specifications

* [Core specification](specification.md) - Defines portable installation, update, and retirement requirements.

## Validation

* [Acceptance scenarios](validation.md) - Defines observable lifecycle outcomes and failure behavior.

## Strategies

* [User-mediated activation](strategies/user-mediated-activation.md) - Keeps an installed update separate from activation until an explicit decision.
