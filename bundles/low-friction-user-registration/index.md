---
okf_version: "0.2"
---

# Low-friction user registration

Register and sign in with minimal input, using email, mobile, or authenticator
one-time passwords, with resumable verification and consumer-selected providers.

## Authors

* industrial-curiosity

## Tags

* user-registration
* authentication
* passwordless
* email-otp
* mobile-otp
* authenticator-otp

## Specifications

* [Registration contract](specification.md) - Defines account creation, verification, authenticator enrollment, session handoff, and recovery.

## Validation

* [Acceptance scenarios](validation.md) - Checks the user journey, all three methods, concurrent requests, interrupted work, and provider substitution.

## Strategies

* [Progressive registration](strategies/progressive-registration.md) - Guides consumer policy choices, provider boundaries, and friction measurement.
