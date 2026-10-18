---
type: Validation
title: Low-friction registration acceptance scenarios
description: Portable acceptance checks for user effort, OTP methods, recovery, concurrency, and provider independence.
tags:
  - user-registration
  - authentication
---

# Low-friction registration acceptance scenarios

Validate the [contract](specification.md) against the consumer's declared
profile. Execute every common scenario and each scenario for enabled methods.
Record a disabled method as not applicable, with its profile decision, rather
than claiming it passed. Use controllable time, delivery outcomes, concurrency,
and session failures. These are acceptance requirements, not a claim that any
implementation has already passed them.

## Entry, identity, and user effort

* **Minimal registration:** Given a new contact, enter it and a valid delivered
  code. Reach the intended activity signed in, without a mandatory password,
  second contact, username, device label, or optional profile form. Check any
  extra activation field against its declared justification.
* **Returning account:** Repeat with an existing verified contact. Reach that
  account without a duplicate. If additional proof is required, verify that
  contact proof alone grants only continuation to that proof.
* **Privacy before proof:** Compare new, existing, disabled, and unknown account
  attempts. Responses, method lists, status, and measured timing do not reveal
  account existence or stored destinations. Generic failures still provide a
  usable next action.
* **Independent contacts:** Submit both email and mobile but verify only one.
  Only that contact becomes verified or usable for authentication. Overlapping
  submitted fields never merge accounts or replace existing account data.
* **Normalization and races:** Submit equivalent contacts under the declared
  normalization rules in concurrent attempts. At most one account owns the
  unique normalized contact. Distinct contacts outside those equivalence rules
  stay distinct; phone country context is visible and correctable.
* **Accessible entry:** Complete the journey by keyboard and with assistive
  output. Paste a code with a leading zero. Check autofill where supported,
  announced errors, focus, destination correction, and visible resend state.

## Delivered codes

Run these scenarios separately for email and mobile.

* **Lifecycle:** Correct active proof succeeds. Incorrect, expired, cancelled,
  exhausted, consumed, wrong-destination, wrong-purpose, and wrong-attempt
  proof fails without granting account or session authority.
* **Resend ordering:** Trigger multiple resends and reorder their delivery.
  Repeated codes retain original expiry, or replacements invalidate prior
  codes, according to the profile. Instructions identify the usable code.
* **Limits:** Exhaust send and verification budgets with simultaneous requests,
  replacement codes, and method changes. Limits hold across those operations;
  cooldown expiry restores only the declared allowance.
* **Delivery failure:** Reject, delay, duplicate, or lose acknowledgment of a
  send. The attempt remains resumable, no account activates from delivery, and
  retries remain bounded. Duplicate or forged delivery callbacks cannot grant
  authority. An alternative method does not bypass required additional proof.
* **Destination correction:** Change a mistyped contact. The old challenge
  fails, non-secret progress remains, and the new contact needs its own proof.

## Authenticator setup and use

* **Interoperability:** Verify configured parameters against independently
  established expected values, including times beyond 2038. Complete both scannable and manual
  setup with at least two independently implemented compatible authenticators,
  without a required vendor account.
* **Enrollment boundary:** Displaying a secret leaves it pending. Only a valid
  generated code enables it. Expired, cancelled, and superseded setup secrets
  cannot activate. Adding a credential to an existing account requires its
  authorized reauthentication, not knowledge of its contact.
* **Clock and replay:** Accept only the configured time window; reject outside
  it. Submit one time-step proof concurrently to multiple attempts and after
  enrollment. It authorizes at most one fresh operation. Retrying the original
  operation returns only its authorized prior outcome.
* **Authenticator-only registration:** If enabled, obtain an account identifier,
  confirmed authenticator, and usable recovery before completion. No contact is
  falsely verified. If disabled, the interface explains the enabled entry path.
* **No resend:** The code interface explains local code generation and clock
  correction, and offers no email/mobile resend for an authenticator challenge.

## Continuation, completion, and recovery

* **Reload and network change:** Resume a pending attempt after reload or a
  network-address change using its protected credential. Public attempt IDs,
  expired credentials, and cancelled attempts cannot resume authority.
* **Commit interruption:** Interrupt before and after proof consumption, account
  commitment, and session issuance. Retry concurrently. There is one account
  association, no second use of proof, and a recoverable result after commitment.
* **Lost session response:** Complete registration but lose the response or
  make session issuance unavailable. The authorized continuation resumes handoff
  within its lifetime. A consumed code alone cannot retrieve a session. Check
  rotation of pre-authentication authority and rejection of unsafe return URLs.
* **Replacement and recovery:** Lose an authenticator, exercise the declared
  recovery method, and replace it. Reject unverified substitutes and replayed
  recovery credentials. Keep the working method until replacement succeeds;
  reject removal of the last method without replacement or account closure.
  Verify required notifications and credential/session revocation.
* **Abuse and cleanup:** Generate unauthenticated abuse against a known account.
  Controls bound cost and guesses without permanent attacker-induced disabling.
  Expired reservations become reusable and retained data is deleted on schedule.
  Audit and analytics contain no codes, secrets, or continuation credentials.

## Provider substitution

Replace email and mobile delivery adapters independently with alternative
contract-compatible implementations. Repeat delivery, resend, failure, and
completion scenarios without changes to account identifiers or the user
journey. Replace delegated verification where offered and confirm purpose
binding and proof consumption remain enforced. Verify the declared drain or
cancellation policy for in-flight challenges during a provider change.
