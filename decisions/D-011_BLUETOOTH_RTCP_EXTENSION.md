# D-011 — RTCP/1 Bluetooth Extension v1

Status: **PROPOSED / OWNER REVIEW — NOT APPROVED, NOT IMPLEMENTED**

Date: 2026-10-22

Coordination baseline read: `5d36f06c301cdd340fe65084dca4d636ad6dc699`

Device baselines held unchanged: TUNER accepted application SHA-256 `d2c89edd1e5aa25a01c7f88ce787ccdcfa2e708a89d6fb402d0326a519ec896e`; REMOTE Round 5 source `bfce47816a8b2b8a92f41d76c6a4bc4975d25361` and installed application SHA-256 `6eb44ff4137d8c11f44dc5e0fed0a7061f77b172d4a38982e5219bbd7454e278`.

## Problem

TUNER already owns working A2DP audio, AVRCP metadata and local Play/Pause/Previous/Next. REMOTE already owns authenticated RTCP, volume control and HOME presentation. Frozen D-009 intentionally reports Bluetooth only as context 3 for radio-state invalidation and forbids Bluetooth metadata and operation flags. Reinterpreting D-009 would make deployed REMOTE decoders reject the response and would change an owner-approved contract.

## Proposed decision

Adopt [BTX/1.0](../references/RTCP_1_BLUETOOTH_EXTENSION_V1_PROPOSED.md) as a separate authenticated RTCP/1 application profile after owner review.

- Preserve the first ID 3/4 exchange as exact revision-2 D-009 capability behavior.
- Use one immediate, authenticated second ID 3 request as explicit BTX opt-in.
- A legacy TUNER returns ID 4; a BTX TUNER returns new ID 12.
- Add IDs 13/14 for bounded Bluetooth state and ID 15 for explicit AVRCP commands.
- Reuse generic correlated result ID 8.
- Source, phone connection epoch and authoritative callback state fence every operation.
- Keep one request in flight, no automatic retry and all existing RTCP security.

## Why this mechanism

The deployed legacy TUNER already accepts another authenticated ID 3 and returns the legacy ID 4, so a new REMOTE can probe without sending an unknown message or breaking the session. An old REMOTE never sends the second request, so a new TUNER remains byte-for-byte legacy for that client. Authentication and record counters protect the probe and response.

## Alternatives rejected

| Alternative | Reason rejected |
| --- | --- |
| Increment D-009 revision | Deployed REMOTE requires revision exactly 2 and would withdraw D-009. |
| Allocate another capability bit | All eight bits are occupied. |
| Unconditional new discovery request | Legacy TUNER fails closed on unknown IDs. |
| Put Bluetooth data into D-009 ID 11 | Frozen rules and deployed decoder forbid flags/text for context 3. |
| Infer support from firmware version | Release strings are not a capability contract. |
| Use mDNS TXT as authority | Discovery is not authenticated application negotiation. |
| Change handshake/record version | Unnecessary transport and cryptographic scope expansion. |

## Authority and ownership

TUNER obtains connection and audio state from the pinned A2DP library callbacks. Mode entry or the existing local pause toggle is not authoritative. Bluetooth callbacks publish fixed bounded state; the established TUNER main-loop owner revalidates and executes AVRCP operations. RTCP/socket processing never invokes display or A2DP ownership paths directly.

An accepted command result means TUNER revalidated and submitted the operation locally. It does not claim the phone applied it. REMOTE waits for a later authoritative state response before changing confirmed playback presentation.

## Compatibility and rollback

Legacy and extension behavior coexist in one authenticated service. Negotiation is session-only and is cleared on reconnect, sleep teardown, restart or rollback. Application rollback on either device restores D-009 fallback without changing NVS, pairing, credentials or partitions. TUNER-first rollout is proposed, with old-REMOTE compatibility verified before REMOTE installation.

## Resource consequence

Maximum BTX plaintext is 255 bytes and authenticated size is 299 bytes, below the existing D-009 maxima. TUNER adds no dynamic allocation or transport buffer and is budgeted for at most 64 bytes of new persistent scalar state. REMOTE is budgeted for at most 320 bytes of persistent state, including the 195-byte HOME title-buffer increase.

## Approval boundary

This record is a proposal. Firmware work is blocked until the owner explicitly approves the negotiation mechanism, messages, bounds, authority semantics and rollout order. Approval must be recorded separately and must not rewrite frozen D-009.
