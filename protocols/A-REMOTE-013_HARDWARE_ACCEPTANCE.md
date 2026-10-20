# A-REMOTE-013 hardware acceptance checklist

**UNEXECUTED PLANNING DOCUMENT.** Every installation or persistent operation requires separate owner authorization. Execute only the sections belonging to the approved implementation slice.

For the first playback/metadata slice, use the more specific [D-009 hardware validation protocol](A-REMOTE-013-D009-HARDWARE-VALIDATION.md) after the exact profile is approved and both candidates have passed software verification.

## Preflight

- [ ] Identify each physical device through its actual ROM/USB interface; do not infer identity from a COM number.
- [ ] Verify candidate size/SHA-256, source commit, production environment, partition capacity and application offset.
- [ ] Reverify local and separate-storage rollback files against their recorded sizes/hashes.
- [ ] Confirm no partition, bootloader, OTA metadata, default NVS, pairing or `remote_ctl` write is required.
- [ ] Confirm additive capability compatibility and installation order: TUNER first, REMOTE second.

## Installation gate per device

- [ ] Flash only the authorized application span once.
- [ ] Read back the exact span independently and require the candidate SHA-256.
- [ ] Confirm normal boot, retained configuration, network, pairing and prior accepted behavior.
- [ ] Stop on the first identity/hash/readback/boot discrepancy; do not retry or roll back without authorization.

## Basic controls

- [ ] Old REMOTE with new TUNER retains authenticated volume-only operation.
- [ ] New REMOTE with approved TUNER reaches READY and advertises only implemented capabilities.
- [ ] Play, pause, previous and next each issue exactly one correlated request and produce authoritative feedback.
- [ ] Wrong source, empty list, boundary, disconnect and timeout fail without stale replay or automatic retry.
- [ ] Touch, encoder push and any assigned button act only in their approved UI context.

## Station state and catalogs

- [ ] Current station ID/name and media metadata match TUNER after local and REMOTE changes.
- [ ] Saved station selection survives reconnect/reboot without relying on array position.
- [ ] Delete/reorder/duplicate/stale-revision cases reject safely.
- [ ] Favorites and Recent pages are bounded, complete/partial status is truthful, and activation is guarded.
- [ ] Country/tag/result navigation respects approved page limits and cancellation.

## Selected-station logo

- [ ] Only the selected radio station logo is requested; track artwork is absent.
- [ ] Missing, invalid, oversized, slow and unsupported assets show the placeholder without blocking controls.
- [ ] Station/source changes cannot display a stale logo.
- [ ] Cache bounds and eviction match the approved design; no credential or raw private locator is logged.

## Lifecycle and coexistence

- [ ] Disconnect/reconnect and session change clear pending commands, stale observations, catalog pages and asset work.
- [ ] SYSTEM_SLEEP/wake reconnects without replay and restores authoritative screen state.
- [ ] Motion wake is reported separately from physical-button function.
- [ ] MP3 playback remains audible while HTTP and RTCP are responsive.
- [ ] Bluetooth A2DP remains audible while HTTP and RTCP are responsive; radio/A2DP/radio transition recovers.
- [ ] TUNER e-paper refresh does not starve RTCP or web service.
- [ ] Record internal free heap, minimum heap, largest internal block, allocation failures and resets in both audio modes.
- [ ] Confirm no unused BLE initialization and no unexpected long-lived internal allocation.

## Acceptance record

Record exact firmware identities, observed results and owner physical confirmations. Mark unmeasured behavior NOT TESTED. Do not infer end-to-end PASS from builds or from local TUNER behavior alone.
