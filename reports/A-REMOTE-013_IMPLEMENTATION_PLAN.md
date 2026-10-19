# A-REMOTE-013 incremental implementation plan

## Gate 0: approve the shared binding

Before firmware edits, owner review must approve the exact [D-009 proposal](../references/RTCP_1_D009_PROPOSED.md) for the first playback slice. Its IDs 9–11, capability bits 3–7, request/result shapes, fixed-list traversal, metadata projection, 446-byte maximum plaintext and mixed-version rules remain proposed, not effective. CCM 1.1.0 remains unchanged.

For station work, D-010 must separately approve durable station identity, catalog revision/paging and station-logo locator/cache boundaries. Do not combine these decisions with the first playback implementation.

## Slice 1: basic playback controls

Scope: radio `playback.play`, `playback.pause`, `playback.previous`, `playback.next`; authoritative playback state and current station/title feedback. Exclude stop, mute, Bluetooth source selection and catalogs.

1. Add TUNER main-loop-owned command adapters and copied authoritative state.
2. Add additive RTCP capabilities/messages and focused wire/dispatch tests.
3. Add REMOTE adapter capabilities/dispatch/observation mapping.
4. Bind existing HOME touch controls and one approved physical input mapping.
5. Preserve single-in-flight, correlation, no retry, session fencing and stale-state clearing.
6. Build TUNER and REMOTE, then install TUNER first and execute the Slice 1 section of the hardware checklist.

The bounded [implementation task](../tasks/A-REMOTE-013-D009-IMPLEMENTATION.md) and [hardware protocol](../protocols/A-REMOTE-013-D009-HARDWARE-VALIDATION.md) are the recommended next steps after separate D-009 approval and task authorization.

## Slice 2: source selection

Define stable `radio` and `bluetooth` source identities, availability and transition results. Map generic playback controls to AVRCP only if D-009/O08/O13 explicitly permits it. Validate MP3/A2DP/web/RTCP coexistence and mode recovery before proceeding.

## Slice 3: station identity and selection

Introduce a TUNER-owned durable opaque station ID and monotonic catalog revision without changing credentials or unrelated NVS. Expose bounded saved-station pages and guarded activation. REMOTE holds only synchronized references and UI state; TUNER remains catalog authority.

## Slice 4: Favorites and Recent

Expose Favorites as an authoritative TUNER catalog with enumerate/activate and explicit add/remove only if approved. Expose Recent only after defining whether entries represent attempts or successful playback. Validate deletion, reorder, duplicates, reboot and reconnect.

## Slice 5: Radio Browser navigation and search

Add bounded country/tag/result queries with cancellation, paging and one active query. Language and free-form search remain optional and require explicit release-scope approval. Network fetches remain outside the RTCP service hot path.

## Slice 6: REMOTE screens and feedback

Convert existing HOME rows/placeholders into screens only for capabilities delivered by earlier slices. Preserve touch navigation, brightness, volume authority, sleep/wake and input contexts. Buttons 1-3 receive actions only through an owner-approved map.

## Slice 7: selected-station logo

After D-010/O15 approval, obtain only the selected radio station logo. Use a bounded locator and one-at-a-time fetch/decode/cache pipeline. Show a deterministic placeholder on absence, error, unsupported format, oversize data, disconnect or source change. Track logo context by durable station ID and revision. Current-track artwork remains outside scope.

## Slice 8: edge cases and closure

Run practical hobby/public-beta regression for reconnect, sleep/wake, uncertain command delivery, stale catalogs, mode changes, MP3/A2DP, HTTP/RTCP, e-paper coexistence, resource minima and UI truth. Preserve private rollback artifacts and publish sanitized evidence.

## Per-slice quality gate

Each slice requires focused host tests, one production build per changed device, artifact identity, flash/RAM delta, backward-compatibility result, reversible application-only commissioning, exact readback and the applicable hardware checklist. A failed slice stops subsequent dependent work. Passing evidence from unchanged layers is reused.

## Explicitly outside A-REMOTE-013

AAC/AAC+, MQTT, SmartThings, industrial qualification, a Native API implementation, arbitrary current-track artwork, partition changes and motion-wake repair are outside this milestone.
