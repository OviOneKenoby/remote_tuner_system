# A-REMOTE-012: Low-Latency Volume Control

- Owner: REMOTE//01 with coordinated TUNER//01 changes
- State: READY FOR HARDWARE COMMISSIONING / HARDWARE PENDING
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

The final pre-commissioning review reverified both candidates, exact application rollback images, matching local full-flash captures and the source-demonstrated TUNER local-encoder correction. Before the first write, reconnect and verify the previously populated owner-controlled external backup. Do not flash either device without separate owner authorization. Status is READY FOR HARDWARE COMMISSIONING / HARDWARE PENDING.
