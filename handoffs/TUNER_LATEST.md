# TUNER//01 handoff

## Metadata
- Handoff ID: TUNER-A-REMOTE-012-PRECOMMISSIONING-READY-20261017T071500Z
- Updated (UTC): 2026-10-17T07:15:00Z
- Task ID: A-REMOTE-012
- Status: READY FOR HARDWARE COMMISSIONING / HARDWARE PENDING
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: 437e79cdfd6b7febf001271a32467191d84b20d2

## Milestone
Reduce both local-encoder and RTCP volume latency while preserving audio, Bluetooth, web-manager and RTCP behavior, then complete artifact and rollback preflight. Source/build and pre-commissioning review are complete; physical coexistence and latency are NOT RUN.

## Baseline
- Device repository: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio
- Branch: baseline `a-remote-011-phase3`; candidate `a-remote-012-low-latency`
- Firmware baseline commit: 18ddd3b16e305341f338afebd7dc725500ecbb73
- Firmware version: v1.1.11 with accepted A-011 RTCP integration
- Working tree at start: clean at baseline; accepted 2,034,800-byte production artifact and retained rollback copies verified
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2 profile; coordination input `437e79cdfd6b7febf001271a32467191d84b20d2`

## Changes
The local encoder ISR still performs bounded quadrature queuing, while the application now handles input before network/web work and atomically coalesces queued detents into one bounded absolute 5% audio target. The synchronous e-paper overlay is rendered once after 250 ms of encoder quiet rather than after every detent; menu navigation remains one event per detent. Read-only diagnostics separate local setter duration and deferred display state. RTCP runs before and after the web-manager turn with a 2 ms loop delay and its own apply/response counters. Protocol, crypto, pairing, response framing and audio backend semantics are unchanged.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Absolute-volume handler | native build/run of `test_ccm_wire.cpp` | GCC 16.2.0, C++17, Windows amd64 | PASS 16/16 | `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md` |
| Scheduling/timing ownership | `python tests/test_rtcp_latency_policy.py` | Python 3.13, Windows amd64 | PASS 1/1, 9 assertions | `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md` |
| Local target/bounds | native build/run of `test_local_volume_target.cpp` | GCC 16.2.0, C++17, Windows amd64 | PASS 10/10 | `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md` |
| Local scheduling policy | `python tests/test_local_volume_latency_policy.py` | Python 3.13, Windows amd64 | PASS 10/10 | `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md` |
| Production build | PlatformIO `run -e esp32-lwip-psram` from committed source | Espressif32 7.0.1, Arduino-ESP32 2.0.17, ESP32 | PASS; 2,036,000 bytes, SHA-256 `0680e8f2c6bfb8b1149ab1a8baec56fa80a7995d0401bf74463ff1f0d1143c1a`; RAM 87,448 | `references/device_evidence/remote/A-REMOTE-012/SOFTWARE_RESULT.json` |
| Rollback identity | direct size/SHA-256 of retained private copies | Windows SHA-256 | PASS; 2,034,800 bytes, SHA-256 `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4` | private evidence; hash recorded in report |

## Remaining unknowns
Actual local detent-to-audio and RTCP detent-to-audio timing, e-paper behavior, loop jitter, internal heap/largest block and stack margin during MP3 and Bluetooth A2DP with active web manager are NOT RUN. Hardware must prove the under-100 ms audible target and absence of audio/UI/web regressions.

Rollback identities remain deliberately distinct. The accepted A-011 production application is 2,034,800 bytes with SHA-256 `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4`. The Stage 1 pre-A-011 installed capture has SHA-256 `4dc7347191a38a18fe76b1635b446a485443ac6d06406bb6f53d303cd105b88a`; the temporary diagnostic application has SHA-256 `f193863f6d2966cc0797b9bdd2144971fb7b4bfc5bb9b1b4c07ff4840cf4a21c`. The non-identical reconstruction remains rejected. Primary and local 4,194,304-byte full-flash captures match SHA-256 `4a980e0887fab052389c233429d9cdf398720e119f2b51141a4fcfb8aa5914f6`.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; current implementation remains under frozen CCM 1.1.0.
- TUNER Native API v1: NO CHANGE; no Native endpoint or semantic was added.
- Other device impact: new and old REMOTE firmware remain wire-compatible; only new REMOTE performs target coalescing.
- Approval evidence: owner A-REMOTE-012 mission and performance override dated 2026-10-16 authorize source/build work on both devices, excluding flash.

## Blockers
Physical application installation and latency/coexistence measurements require owner authorization. The previously populated external backup must be reconnected and verified before writing. No software blocker is known.

## PM decision required
Authorize or reject TUNER-first application-only commissioning. No merge or flash is implied.

## Recommended next task
Install the exact TUNER candidate at `0x10000`, verify exact readback and ordinary UI/settings/MP3/A2DP/Wi-Fi/web behavior, then proceed to REMOTE only if TUNER passes. This recommendation is not authorization.

## Commit
- Firmware result commit(s): `5391beef5e7ba264362ea19f2fdd93202308fa55`
- Device changelog: TUNER source `CHANGELOG.md` and coordination `CHANGELOG.md` record the result
- Coordination publication: branch `remote/a-remote-012-low-latency`; PR and final coordination hash reported in publication message
- Previous handoff archive: `archive/tuner/2026-10-17T071500Z_A-REMOTE-012_TUNER-A-REMOTE-012-SOFTWARE-PASS-20261017T060600Z.md`

## Hardware status
- Physical device tested: NO
- Board / hardware configuration: accepted classic ESP32 TUNER with 4 MiB flash and `esp32-lwip-psram` profile; exact device identity not accessed in this task
- Procedure and result: NOT RUN; reversible commissioning checklist prepared
- Firmware actually flashed: current residency NOT VERIFIED in A-REMOTE-012; retained production rollback is 2,034,800 bytes, SHA-256 `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4`
- Build-only or simulated checks: focused handler, local-target and scheduling checks plus the committed-source production build listed above
