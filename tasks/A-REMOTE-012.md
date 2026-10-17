# A-REMOTE-012: Low-Latency Volume Control

- Owner: REMOTE//01 with coordinated TUNER//01 changes
- State: CONNECTION-STABILITY CORRECTION BUILT / HARDWARE VALIDATION REQUIRED
- Coordination baseline: `437e79cdfd6b7febf001271a32467191d84b20d2`
- TUNER source baseline: `18ddd3b16e305341f338afebd7dc725500ecbb73`
- TUNER candidate source: `073b65963e3ed8e3438bc34134f5a903fce995de`
- Objective: make EC11 volume control feel like a local control while retaining CCM 1.1.0 and RTCP/1 authority, correlation, replay protection, session fencing and fail-closed behavior.
- Engineering targets on a healthy local network: first and continued audible response under 100 ms; final 15-detent target within 250 ms after the last detent; clearly provisional local UI response under 50 ms.
- Scope: private REMOTE target accumulation, RTCP scheduling and provisional UI; public TUNER RTCP cadence, local encoder/audio scheduling, deferred e-paper feedback and bounded timing evidence; focused/integration regression; production builds; reversible commissioning plan.
- Exclusions: physical flashing, pairing/NVS/partition changes, CCM or RTCP wire changes, AAC/AAC+, unassigned physical-button actions, intermittent QMI8658 motion-wake work, UI redesign and unrelated refactoring.
- Acceptance: software verification is complete. Physical audible/UI timing and MP3/A2DP/web-manager coexistence remain required before owner acceptance.
- Rollback baseline: REMOTE 2,523,936-byte application, SHA-256 `38b43de02bf1ef69b85678f0a67451836cb0a24e3bf1876283933b3185ed4d5d`; TUNER 2,034,800-byte application, SHA-256 `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4`. Both remain private and independently retained.

## Result

The source-proven latency chain serialized each one-percent REMOTE command behind an authoritative round trip, while post-command state could wait for the periodic snapshot schedule. TUNER already accepted absolute canonical volume percentages and applied them directly, so no CCM or RTCP wire change was needed.

REMOTE now maintains one bounded desired target, coalesces queued detents, sends an absolute target, and retains at most one in-flight command. Input received while that command is in flight changes only the bounded successor target. A successful result triggers an immediate authoritative snapshot request. A confirmed post-result observation that differs from the submitted target is treated as legitimate external authority and cancels the obsolete local successor. Definite failure cancels; uncertain delivery is never retried; disconnect, sleep, session and capability invalidation clear pending state.

The HOME value uses `authoritative>desired` while pending and retains the authoritative indicator bar. It refreshes at 20 ms and never marks the provisional target authoritative. REMOTE uses TCP no-delay and a 5 ms control-owner cadence. TUNER services local input before network/web work, coalesces queued local detents into one bounded absolute audio update, and defers synchronous e-paper feedback until 250 ms of encoder quiet. RTCP remains serviced before and after the web-manager turn with a 2 ms loop delay and separate bounded timing evidence.

See [software validation and commissioning report](../reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md) and [sanitized evidence](../references/device_evidence/remote/A-REMOTE-012/SOFTWARE_RESULT.json).

## Historical diagnostic stop

Both A-REMOTE-012 applications were installed with exact application readback PASS. TUNER boots normally and its local audio-volume response is fast; the e-paper refresh remains visibly slower. REMOTE and TUNER are reachable, and REMOTE completes mutual authentication, accepts identity and accepts the capability response. No first state snapshot becomes authoritative, so `volume.level` remains unknown, `volume.set` remains unavailable and the session never becomes usable for control. Later automatic reconnects have also ended after client hello with EOF.

Source comparison shows no A-REMOTE-012 change to RTCP framing, cryptography, identity, capability or snapshot encoding. The first proven failure boundary is after accepted capabilities and before a first snapshot is admitted. TUNER internal heap was observed at 2,304 bytes free with a 948-byte largest block, but no allocation failure or causal link was observed; low heap is a material risk signal, not the demonstrated root cause. Current diagnostics cannot distinguish request receipt, response construction/write failure, transport closure or REMOTE-side snapshot rejection. Stop before further firmware changes, flashing or control commands. The minimum next step is separately authorized, bounded TUNER server instrumentation for record type/stage, response-write result, close reason and allocation-failure delta.

That bounded instrumentation is now implemented and built at TUNER commit `fda5f1ad1e5ebb9e83238cdbaa3ad79564e40842`. Focused diagnostics and relevant regressions pass; the production candidate is 2,036,992 bytes with SHA-256 `18d59b75cbf481b517b09fd274207e2271cdd42a0a146f56eafeca2e8a1196d3`, 1,108,736 bytes slot headroom and 87,512 bytes static RAM. No hardware was accessed. The next gate is an owner-authorized TUNER application-only installation followed by one passive automatic-handshake observation and one existing read-only serial snapshot. Root cause remains unproven.

The owner subsequently authorized that installation. All eight local/external rollback-critical files matched their recorded identities, the expected 4 MiB TUNER was identified, and only the application was written at `0x10000`. Independent 2,036,992-byte readback matched the candidate hash exactly. The single authorized `x` snapshot reported connected Wi-Fi and healthy memory but `connections=0`, `client_finishes=0`, `records=0`, `snapshot_requests=0`, and no allocation failure. A single read-only REMOTE diagnostics request timed out. This run therefore stops before TUNER TCP acceptance and cannot classify the post-identity snapshot failure. A future observation requires REMOTE to be demonstrably online; no reconnect loop or control command is authorized by this result.

## Current status

Two later bounded TUNER snapshots demonstrate that authentication, identity, capabilities and authoritative snapshots succeed repeatedly, but the persistent connection is starved by long TUNER application-loop turns. In the later snapshot, 104 accepted connections account for 24 TUNER idle timeouts, 79 peer EOFs and one current/remaining connection. All 259 snapshot requests completed; partial writes, failed writes, allocation failures, network `nomem` and TUNER Wi-Fi disconnects remained zero. The measured 5,983 ms maximum loop turn exceeds both REMOTE's unchanged 3,000 ms awaited-response deadline and TUNER's unchanged 5,000 ms record-idle deadline.

Source inspection confirms that the same main loop owns RTCP and synchronous GxEPD2 BUSY waits. The panel driver already supplies a cooperative busy callback. TUNER commit `073b65963e3ed8e3438bc34134f5a903fce995de` registers that callback to poll RTCP and yield while the panel is busy, retaining the existing owner and fixed buffers. It also reads buffered application input before classifying the unchanged idle deadline, so a complete request present at the boundary is processed while incomplete input still times out. No task, queue, dynamic allocation, buffer increase, timeout relaxation, protocol change or REMOTE change was introduced.

Focused scheduling, deadline, latency and diagnostic verification passed 54 checks/assertions. The production `esp32-lwip-psram` build passed: 2,037,152 bytes, SHA-256 `19c39f4721ff43b939806f18aee599203225afde384c07934d58f1d0cc0398e8`, 1,108,576 bytes application-slot headroom and unchanged 87,512-byte static RAM. No hardware was accessed or flashed. Hardware validation is still required to confirm stable READY state across e-paper updates, normal REMOTE sleep/wake and reconnect, plus MP3/A2DP/web-manager regression.
