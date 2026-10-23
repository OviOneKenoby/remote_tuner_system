# RTCP/1 Bluetooth Extension v1 implementation plan

Status: **SOFTWARE IMPLEMENTATION COMPLETE / HARDWARE ACCEPTANCE PENDING**

Dependency satisfied: D-011 and the exact BTX/1.0 proposal are owner approved and frozen. Sections 1 and 2 are completed software history; sections 3–6 remain the active hardware/compatibility gate. Current identities are recorded in the integration reconciliation report.

## 1. TUNER firmware task

- Preserve the first ID 3/4 response and legacy D-009 bytes.
- Implement the session-scoped probe window and IDs 12–15 codecs.
- Register bounded A2DP connection/audio callbacks.
- Reuse existing artist/title storage; add UTF-8-safe projection and clearing.
- Add a fixed Bluetooth projection with sequence, generation and revision.
- Add explicit Play/Pause owner methods and reuse Previous/Next through the main-loop mailbox.
- Revalidate source, connection, state, generation and operation availability at execution.
- Add focused codec, lifecycle, callback, command-refusal and legacy-compatibility tests.
- Run one production TUNER build and report flash/static RAM delta. No hardware write.

Stop for review before TUNER hardware installation.

## 2. REMOTE firmware task

- Add the immediate second-ID-3 probe and ID 4 fallback.
- Add strict IDs 12–15 codecs and the negotiated-session state.
- Map active source, connection, playback, media and operation availability into CCM without changing frozen meanings.
- Reuse existing RTCP metadata buffers.
- Increase only the HOME combined-title presentation bound from 32 to 227 bytes.
- Render source label `Bluetooth` and deterministic artist/title formatting through existing labels and scrolling.
- Preserve existing volume, command correlation, session/source fencing and no-retry behavior.
- Add focused codec, HOME, stale-state, rollback and mixed-version tests.
- Run one production REMOTE build and report flash/static RAM/stack delta. No hardware write.

Stop for review before REMOTE hardware installation.

## 3. Compatibility task

- Execute the four-version matrix from the compatibility report.
- Prove exact first ID 4 bytes with old REMOTE/new TUNER.
- Prove new REMOTE/old TUNER fallback keeps the session and volume.
- Exercise malformed frames, source changes, reconnect, sleep and rollback.

## 4. TUNER-first hardware rollout

- Reverify candidate and rollback artifacts.
- Application-only install with exact-span readback.
- Test old REMOTE radio D-009 and volume before installing new REMOTE.
- Measure A2DP audio, HTTP, RTCP, internal heap, minimum heap, largest block and allocation failures.

Separate owner authorization is required for the write.

## 5. REMOTE hardware rollout

- Reverify candidate and rollback artifacts.
- Application-only install with exact-span readback.
- Verify session negotiation, source presentation and legacy fallback.

Separate owner authorization is required for the write.

## 6. Final Bluetooth acceptance

- Radio ↔ Bluetooth transition and stale clearing.
- Phone connect/disconnect/reconnect.
- Artist/title variants, long UTF-8 and live metadata changes.
- Explicit Play/Pause/Previous/Next plus refusal cases.
- Existing Bluetooth volume, rapid encoder behavior and authoritative reconciliation.
- RTCP reconnect, REMOTE sleep/wake and no stale replay.
- MP3, A2DP, HTTP/web-manager and RTCP coexistence.
- Independent rollback of each device.

No task above starts automatically when the proposal is approved; each firmware and hardware stage retains its own authorization gate.
