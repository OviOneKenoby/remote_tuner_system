# A-REMOTE-012: Low-Latency Volume Control

- Owner: REMOTE//01 with coordinated TUNER//01 changes
- State: DIAGNOSTIC CANDIDATE READY / HARDWARE DIAGNOSIS PENDING
- Coordination baseline: `437e79cdfd6b7febf001271a32467191d84b20d2`
- TUNER source baseline: `18ddd3b16e305341f338afebd7dc725500ecbb73`
- TUNER candidate source: `5391beef5e7ba264362ea19f2fdd93202308fa55`
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

## Current stop

Both A-REMOTE-012 applications were installed with exact application readback PASS. TUNER boots normally and its local audio-volume response is fast; the e-paper refresh remains visibly slower. REMOTE and TUNER are reachable, and REMOTE completes mutual authentication, accepts identity and accepts the capability response. No first state snapshot becomes authoritative, so `volume.level` remains unknown, `volume.set` remains unavailable and the session never becomes usable for control. Later automatic reconnects have also ended after client hello with EOF.

Source comparison shows no A-REMOTE-012 change to RTCP framing, cryptography, identity, capability or snapshot encoding. The first proven failure boundary is after accepted capabilities and before a first snapshot is admitted. TUNER internal heap was observed at 2,304 bytes free with a 948-byte largest block, but no allocation failure or causal link was observed; low heap is a material risk signal, not the demonstrated root cause. Current diagnostics cannot distinguish request receipt, response construction/write failure, transport closure or REMOTE-side snapshot rejection. Stop before further firmware changes, flashing or control commands. The minimum next step is separately authorized, bounded TUNER server instrumentation for record type/stage, response-write result, close reason and allocation-failure delta.

That bounded instrumentation is now implemented and built at TUNER commit `fda5f1ad1e5ebb9e83238cdbaa3ad79564e40842`. Focused diagnostics and relevant regressions pass; the production candidate is 2,036,992 bytes with SHA-256 `18d59b75cbf481b517b09fd274207e2271cdd42a0a146f56eafeca2e8a1196d3`, 1,108,736 bytes slot headroom and 87,512 bytes static RAM. No hardware was accessed. The next gate is an owner-authorized TUNER application-only installation followed by one passive automatic-handshake observation and one existing read-only serial snapshot. Root cause remains unproven.
