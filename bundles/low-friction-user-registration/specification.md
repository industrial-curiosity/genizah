---
type: Specification
title: Low-friction user registration contract
description: Register accounts through minimal, resumable proof of control with interchangeable OTP methods and providers.
tags:
  - user-registration
  - authentication
  - passwordless
  - email-otp
  - mobile-otp
  - authenticator-otp
---

# Low-friction user registration contract

## Purpose and conformance

Let a person create an account and reach their intended activity without an
unnecessary password, profile form, or separate sign-in step. MUST indicates a
requirement; SHOULD permits a documented reason to depart; MAY is optional.

The bundle defines email delivery, mobile delivery, and authenticator-generated
one-time passwords (OTPs). A consumer MUST declare its enabled methods and
support the applicable requirements for each. Supporting the bundle does not
require enabling every method for every user. All three MUST be independently
selectable in the adaptation design, without requiring a particular delivery
service, authenticator application, identity service, database, or hosting service.

Identity proofing, authorization roles, federation, and general session
management are outside scope. A verified contact establishes control of that
contact at verification time, not a person's legal identity. The session
boundary and safe continuation after registration are within scope.

## Terms and state

* An **account** has a stable internal identifier independent of its contacts.
* A **method** is email OTP, mobile OTP, or a time-based authenticator OTP.
* A **registration attempt** stores pending inputs and progress, identified by
  an opaque identifier and protected by an unguessable continuation credential.
* A **challenge** binds proof to an attempt or account, purpose, method, exact
  destination or credential, expiry, and verification budget.
* A **verified contact** is an email address or mobile number whose own
  challenge succeeded. An **enrolled authenticator** has a confirmed secret.

An attempt progresses from pending to verified to completed, or becomes
expired or cancelled. Verified means the selected proof succeeded; it does
not imply that all configured activation requirements have been met.
Completed means the account association is committed. Session delivery may
still require retry. Expired or cancelled attempts MUST NOT activate accounts.
Abandoned inputs, challenges, and unenrolled secrets MUST expire and be
removed according to a declared retention policy.

## Minimal entry and continuation

1. Offer a shared registration/sign-in entry point. Ask for only the selected
   method's necessary identifier and any unavoidable activation prerequisites.
2. For email or mobile, use the supplied contact as the destination. Do not
   require both contacts, a password, a chosen username, a device name, or
   authenticator enrollment on this default path. Generate internal identifiers
   automatically; defer optional profile fields until after activation.
3. For authenticator sign-in, obtain an account identifier before checking its
   enrolled credential. For a new account, start enrollment rather than asking
   for a code from a secret the person does not yet have.
4. Preserve entered non-secret information and the intended activity through
   ordinary retries, reloads, and method changes. Store continuation authority
   securely; a public attempt identifier alone MUST NOT authorize resumption.
5. Accept pasted codes, preserve leading zeroes, support keyboard and assistive
   input, and permit platform autofill where available. Explain the next action,
   expiry, and resend availability without exposing internal service errors.
6. After proof and activation prerequisites succeed, create or resolve the
   account and establish a session without asking the person to sign in again.
   Validate any return destination against consumer policy before navigation.

Optional passwords MAY be an additional capability but MUST NOT become a
prerequisite for these OTP flows. Product-specific required fields and consent
MUST be declared in the consumer profile, with their reason for blocking
activation. A changed network address alone MUST NOT discard valid progress.

## Account resolution and contact ownership

The consumer MUST define consistent contact normalization and uniqueness rules
for lookup, challenge creation, verification, and account commitment. Preserve
the entered address for display when useful. Do not infer equivalent email
addresses through provider-specific alias rules. Resolve mobile numbers with
explicit country context rather than silently guessing it.

Account existence MUST NOT be disclosed before proof through response content,
status, available-method lists, masked stored contacts, or materially different
timing. Generic authentication responses reduce account enumeration risks.
Show methods configured for the product before proof; show
account-specific destinations only after sufficient authentication.

When a verified contact already identifies an account, continue that account's
authentication policy instead of creating a duplicate. If it requires additional
proof, restrict the continuation to that proof; do not issue a full session.
Never attach submitted profile data or a new authenticator to an existing
account solely because the attempt contains its contact or username.

Only the challenged contact becomes verified. Supplying two contacts while
proving one MUST NOT verify the other. Adding or changing a contact requires
proof of the new contact and authorization from the existing account. Do not
automatically merge accounts because their submitted fields overlap.

## Delivered OTPs

Email and mobile delivery MUST use the same lifecycle guarantees. The mobile
transport is a consumer choice; text messages are one supported adaptation.

* Generate unpredictable codes and bind them to the challenge. A code from
  registration MUST NOT authorize recovery, contact replacement, or another
  attempt. Verification MUST use trusted time and reject expired, cancelled,
  exhausted, or already-consumed challenges.
* Bound lifetime, guesses, sends, and resends. Enforce limits on the service,
  including simultaneous requests. Replacing a code or changing methods MUST
  NOT reset the attempt's accumulated abuse budget.
* Declare whether resend repeats the active code or replaces it. Repeating
  MUST NOT extend expiry; replacing MUST invalidate the old code. Explain
  which code the person should use when messages arrive out of order.
* A delivery acknowledgment means accepted for delivery, not received or
  verified. On delivery failure or an unknown result, retain the attempt and
  offer a bounded retry or eligible alternative. Never activate on delivery.
* Protect stored verification material against offline guessing if challenge
  storage leaks. Keep any key needed for that protection separately controlled.
  Repeated-code delivery requires protected recoverable code material; expire
  it with the challenge. Do not log codes or continuation credentials.
* Changing a destination MUST invalidate its outstanding challenge, preserve
  permitted non-secret progress, and require proof of the replacement.

## Authenticator enrollment and verification

Use interoperable time-based OTP parameters. Each credential needs its own
random secret, matching client/server parameters, a bounded clock window, and
replay rejection for a successfully accepted time step.

For a new account, a consumer MAY permit authenticator-only registration. It
MUST then provide a usable account identifier and a recovery method before
completion, without marking any contact verified. Otherwise, enroll the
authenticator after a contact-based registration or require it as an explicitly
declared activation prerequisite.

Provisioning MUST occur over a protected channel bound to the pending attempt
or an appropriately reauthenticated account. Provide a scannable setup and a
manual alternative containing equivalent parameters. Do not require an account
with a named authenticator vendor. A displayed secret is pending, not enrolled:
require a valid generated code before enabling it. Expire abandoned setup and
invalidate superseded setup secrets.

Protect retained secrets with access controls and encryption; a verifier needs
access to the secret or a protected verification service. Exclude provisioning
data, codes, and recovery credentials from logs and analytics. After enrollment,
do not redisplay the existing secret as a recovery mechanism.

Enforce guessing limits and atomically reject reuse of a consumed credential
time step across concurrent attempts, including reuse of the enrollment proof
for sign-in. A retry tied to the same authorized completed operation MAY return
its prior result without treating the code as fresh proof. Give bounded clock
correction guidance; never widen the window indefinitely. Authenticators generate
codes locally, so the interface MUST NOT offer a delivery resend operation.

## Commitment, session handoff, and failures

The observable result of concurrent completion requests MUST be one account
association and one proof consumption. Enforce uniqueness at commitment,
including normalized contacts and any chosen public identifier. An implementation
may use atomic storage or a recoverable staged operation, provided no caller can
observe a second successful activation from the same proof.

Commit a recoverable completion result before reporting success. A lost response,
session-service outage, or retry MUST NOT create a duplicate account, consume
another proof unnecessarily, or strand the person behind an unusable code.
Allow bounded resumption of session handoff using the attempt's protected
continuation authority. A consumed code or public attempt identifier alone MUST
NOT retrieve a session. Rotate or invalidate continuation authority when handoff
finishes and replace any pre-authentication session authority.

Distinguish incorrect proof, expiry, cooldown, unavailable delivery, and temporary
service failure where doing so does not disclose account state. Return a useful
next action and a server-derived retry time for cooldowns. Permanent failure
MUST release temporary reservations after the declared retention period.

## Recovery, method changes, and abuse

Before relying on an authenticator as the sole method, establish recovery, such
as single-use recovery credentials or an explicitly verified alternative.
Replacing a factor is sensitive, and recovery must not create an easier account
takeover path. Require fresh appropriate proof for removal or
replacement, verify the replacement before removing the working method, notify
existing verified contacts when available, and revoke affected credentials and
sessions according to the declared policy. Block removal of the last usable
method unless replacement or deliberate account closure completes.

An alternative method MUST satisfy the account's existing authentication policy;
an outage MUST NOT silently bypass an additional-factor requirement. Do not
claim that the three methods provide equal assurance or phishing resistance.
Two delivery options alone do not establish independent authentication factors.

Bound automated sends and guesses across attempts, destinations, accounts where
known, and abuse sources. Also enforce provider spending limits. Do not impose
permanent account disablement solely because unauthenticated traffic exhausts
a budget. Temporary controls MUST have a recovery path. Record minimal events
for issuance, delivery outcome, verification, activation, recovery, and failure,
using non-secret correlation identifiers and bounded retention.

## Consumer decisions and validation

Record enabled methods, activation prerequisites, normalization and uniqueness,
code lengths and lifetimes, verification and delivery limits, resend semantics,
authenticator parameters and clock tolerance, continuation lifetime, recovery,
session policy, providers, and retention. Specify concrete values and ownership
before implementation; this bundle supplies no universal numeric risk policy.

Use [progressive registration](strategies/progressive-registration.md) to make
these choices and [acceptance scenarios](validation.md) to validate them.
