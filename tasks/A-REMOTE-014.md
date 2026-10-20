# A-REMOTE-014 — Automatic TUNER discovery and reconnection

## Status

**HARDWARE VALIDATED / PASS** as of 2026-10-20.

## Objective

Allow an already-paired REMOTE to locate TUNER after DHCP address changes
without a reservation, manual endpoint edit, re-pairing, or persistent
association change. DNS-SD supplies transport candidates only; RTCP mutual
cryptographic authentication remains the sole authority.

## Authorized scope

- TUNER advertises `_rtcp._tcp` on the existing port 46411 while Wi-Fi and the
  RTCP listener are available.
- REMOTE performs bounded discovery, rotates eligible candidates, and pins a
  runtime endpoint only after the existing RTCP proof and encrypted identity
  response succeed.
- Preserve CCM 1.1.0, D-009, RTCP cryptography, one session, one command in
  flight, pairing storage, NVS, partitions, playback, HTTP, Bluetooth, UI,
  power management, and rollback artifacts.
- Focused host tests, pinned production builds, public documentation, and
  separate open implementation PRs are authorized.

## Explicit exclusions

No hardware access, flash, erase, reset, pairing or NVS mutation, release,
merge, UI redesign, custom broadcast protocol, or unrelated feature work.
TUNER PR #7 remains unchanged and dedicated to D-009.

## Result

Software design, implementation, focused verification, both production builds,
and physical hardware validation passed. TUNER (2,069,152 bytes) and REMOTE
(2,568,992 bytes) candidates were flashed, read back, and independently
SHA-256 verified. Functional automatic endpoint recovery across a DHCP address
change (from `192.168.1.152` to `192.168.1.31`), encoder volume control, audio
playback status, and TUNER power disconnect/reconnect recovery were verified.
The exact evidence and limitations are in
[`reports/A-REMOTE-014_DISCOVERY.md`](../reports/A-REMOTE-014_DISCOVERY.md).
