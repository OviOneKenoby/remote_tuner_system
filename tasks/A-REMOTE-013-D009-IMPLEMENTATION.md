# A-REMOTE-013 D-009 first-slice implementation task

- State: **PROPOSED / NOT ASSIGNED**
- Dependency: explicit owner approval and freeze of [D-009](../references/RTCP_1_D009_PROPOSED.md)
- Baseline: coordination `aa45826492d78714ce58221ea2a832adb52ac73f`; TUNER v1.1.12 source `d112dd0bbef7d86bd22090ec75d76cad3be77677`; installed REMOTE application 2,526,848 bytes / SHA-256 `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da`

## Outcome

Implement the approved additive radio playback and now-playing profile without changing CCM 1.1.0, volume behavior, pairing, persistence, partitions, UI geometry or Bluetooth semantics.

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

## Exclusions

Stop, mute, source selection, Bluetooth AVRCP/metadata, station catalogs/selection, Favorites mutation, Recent, browse/search, logos/artwork, AAC work, MQTT, SmartThings and Native API v1.
