# A-REMOTE-013 D-009 first-slice implementation task

- State: **READY FOR IMPLEMENTATION REVIEW / NOT STARTED**
- Authority: documentation-only preparation; firmware implementation is not authorized by this task publication
- Dependency: satisfied for planning by the exact [D-009 owner approval](../references/D009_OWNER_APPROVAL_2026-10-19.md); execution still requires a separate owner authorization
- Baseline: coordination `aa45826492d78714ce58221ea2a832adb52ac73f`; TUNER v1.1.12 source `d112dd0bbef7d86bd22090ec75d76cad3be77677`; installed REMOTE application 2,526,848 bytes / SHA-256 `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da`

## Outcome

Implement the approved additive radio playback and now-playing profile without changing CCM 1.1.0, volume behavior, pairing, persistence, partitions, UI geometry or Bluetooth semantics.

## Source ownership and dependencies

- TUNER owns playback execution, fixed-list traversal, source/station generation, station text, StreamTitle truth, capability advertisement and final command results. Use the official TUNER repository from v1.1.12 executable source `d112dd0bbef7d86bd22090ec75d76cad3be77677` and the `esp32-lwip-psram` production environment.
- REMOTE owns RTCP decoding/dispatch, CCM admission and correlation, session fencing, HOME input bindings and existing label updates. Start from the public REMOTE repository synchronized with the accepted 2,526,848-byte A-REMOTE-012 baseline.
- The only effective shared requirements are CCM 1.1.0 and the frozen D-009 specification identified by SHA-256 `ad6fa343c7ea6363febfffa143c6ffb62e401c19d994abcdaa7287bd0ded6c92`.
- Install and validate TUNER first. REMOTE implementation starts only after old-REMOTE/new-TUNER compatibility is demonstrated.

## TUNER phase

1. Add exact IDs 9–11 codecs and capability bits/revision.
2. Add one fixed-size main-loop command mailbox and fixed-size authoritative projection.
3. Implement explicit play, pause and fixed-list guarded previous/next. Never route D-009 through discovered-mode Favorite mutation or Bluetooth AVRCP.
4. Invalidate metadata and increment generation on source/station transitions; serialize only valid bounded UTF-8.
5. Add focused codec, invalid-frame, generation/state fence, traversal, combined-metadata, truncation and reconnect tests.
6. Run one production `esp32-lwip-psram` build and record size/hash/headroom/static RAM.
7. Confirm current REMOTE remains authenticated and volume-only compatible.

Stop for separate owner authorization before TUNER application-only installation. Hardware validation must confirm old-REMOTE volume compatibility, radio command behavior, metadata truth and MP3/A2DP/web/RTCP resource health.

## REMOTE phase

Start only after TUNER hardware validation.

1. Add exact codecs and capability parsing without changing IDs 1–8.
2. Register/withdraw D-009 Core capabilities and map correlated result codes.
3. Admit only fresh, same-generation playback/station/metadata observations.
4. Bind the existing HOME previous/toggle/next controls and existing station/now-playing labels. Keep physical buttons unassigned.
5. Preserve single-in-flight, no retry, disconnect/sleep/session invalidation and command-priority behavior.
6. Add focused wire, malformed UTF-8/length, freshness/generation, command-correlation, UI-binding and compatibility tests.
7. Run one `remote01` production build and record size/hash/headroom/static RAM.

Stop for separate owner authorization before REMOTE application-only installation.

## Acceptance

- Exact TUNER-first backward compatibility passes.
- Play/pause/previous/next each produce one correlated result and fresh authoritative state.
- Discovered and unsupported sources refuse safely; old-session results never apply.
- Station and StreamTitle are correct across station changes, absent/malformed/long metadata, reconnect and sleep/wake.
- Existing volume, UI/navigation, configuration, pairing, MP3, A2DP, HTTP/RTCP and power behavior remain functional.
- Exact firmware identities and independent flash readbacks are recorded under separate hardware authorization.

## Resource and compatibility budgets

- Preserve the 512-byte plaintext ceiling and existing 556-byte authenticated-record arrays; the largest D-009 plaintext is 446 bytes and authenticated record is 490 bytes. No transport buffer growth or dynamic allocation in hot paths.
- Use one fixed-size TUNER command mailbox, one fixed-size authoritative projection and one application request in flight. Record static RAM/flash deltas, free/minimum internal heap and largest internal block during later hardware validation.
- Each production application must fit its unchanged slot with material headroom; compare against its accepted baseline and stop on an unexplained regression.
- Mixed versions must retain IDs 1–8 and authenticated volume behavior. New REMOTE sends no D-009 request unless revision 2 and the required capability bit are advertised.

## Verification sequence

1. TUNER focused host tests: exact codecs, malformed framing/UTF-8/lengths, generation and state fences, result errors, fixed-list traversal, combined metadata/truncation, disconnect and old-REMOTE compatibility.
2. One TUNER `esp32-lwip-psram` production build; record commit, size, SHA-256, flash/RAM use and headroom.
3. After separate authorization, application-only TUNER commissioning and the published TUNER-first compatibility protocol.
4. REMOTE focused host tests: codecs, capability gating, freshness/generation, result correlation, session replacement, no retry/replay, UI owner-task updates and old-TUNER compatibility.
5. One REMOTE `remote01` production build; record commit, size, SHA-256, flash/RAM use and OTA headroom.
6. After separate authorization, application-only REMOTE commissioning and joint functional cases. Preserve exact-span readback evidence and reversible application-only rollback for both devices.

## Exclusions

Stop, mute, source selection, Bluetooth AVRCP/metadata, station catalogs/selection, Favorites mutation, Recent, browse/search, logos/artwork, AAC/AAC+ repair, MQTT, SmartThings, motion-wake repair and Native API v1.
