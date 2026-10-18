---
type: Strategy
title: Progressive registration and provider boundaries
description: Adapt the registration contract to product needs while keeping unnecessary steps and provider coupling out of the user journey.
tags:
  - user-registration
  - passwordless
---

# Progressive registration and provider boundaries

## Start with the shortest valid journey

Use a method choice only when multiple enabled choices help the person. A
contact entered directly can select its delivery method. Do not force a separate
registration/sign-in decision: resolve the account after proof. A suitable
default contact journey is contact entry, code entry, then the intended activity.

Offer optional profile completion after activation. Generate an editable device
label rather than requesting one before proof. Keep a visible way to correct a
mistyped destination, resend when allowed, or choose another eligible method.
Retain safe inputs when a person takes those actions.

Authenticator enrollment needs provisioning and confirmation, so it has a
different initial journey from delivered codes. A contactless path also needs
an account identifier and recovery setup. Explain these steps before starting;
do not pretend all three methods have the same setup cost.

## Write a concrete consumer profile

Resolve these decisions before implementation. Choices may change the journey
but cannot weaken the [registration contract](../specification.md).

| Decision | Required record |
| --- | --- |
| Product entry | Enabled methods, default presentation, guest continuation if offered |
| Activation | Required consent or fields, reason for each, optional profile fields |
| Identity | Stable account ID, public identifier if any, contact normalization and uniqueness |
| Authentication | Each method's role at registration, sign-in, additional proof, and recovery |
| Delivered codes | Format, expiry, attempt cap, resend policy, cooldown, message transport |
| Authenticator | Parameters, supported provisioning format, clock window, enrollment expiry |
| Recovery | Recovery proof, last-method protection, notifications, session revocation |
| Continuation | Credential storage, expiry, cancellation, allowed return destinations |
| Operations | Providers, timeouts, idempotency, retry budgets, outage and spending controls |
| Retention | Expiry and deletion of attempts, secrets, delivery metadata, and audit events |

Email depends on mailbox security; mobile delivery can be affected by number
takeover, while authenticator loss requires planned recovery. Select
methods and additional proof according to the product's assurance needs. The
bundle's provider independence does not make the methods interchangeable in
every security policy.

## Separate provider work from account decisions

Keep these logical responsibilities separate, without requiring separate
services or any particular deployment architecture:

* **Attempt coordination:** owns state, purpose binding, limits, and continuation.
* **Delivery:** accepts destination, message, expiry, and an operation identifier;
  returns accepted, rejected, or unknown, plus permitted diagnostic metadata.
* **OTP verification:** owns protected material, expiry, guesses, and atomic
  proof consumption. This may be local or delegated to a selected service.
* **Account commitment:** enforces uniqueness and produces a durable outcome.
* **Session handoff:** establishes authority only from that committed outcome.

Map provider-specific errors to the contract's outcomes. Authenticate delivery
callbacks, correlate them with the original operation, and handle duplicates.
A delivery callback never counts as proof of control. External OTP verification
must preserve purpose binding and single use; a generic provider success alone
is insufficient to select or activate an account.

Replacing a delivery provider should not require changing account identifiers
or reenrolling authenticators. When a provider owns active challenges, either
drain those challenges through their original provider or cancel and reissue
them explicitly. Do not silently reinterpret an old challenge under a new
provider. If secrets cannot be transferred safely, authenticator-provider
replacement needs authorized reenrollment with continuity for existing users.

## Measure friction without collecting secrets

Measure completion and abandonment by method and step, time to completion,
delivery failure, resend frequency, recovery completion, and repeated data
entry. Use aggregates and short-lived correlation identifiers; exclude codes,
contact values, provisioning secrets, and continuation credentials.

Set product-specific targets before rollout. Compare improvements against the
same activation policy so a shorter flow cannot appear successful merely by
dropping required proof. The acceptance scenarios validate behavior; usability
sessions and these measurements assess whether the adaptation reduces friction.
