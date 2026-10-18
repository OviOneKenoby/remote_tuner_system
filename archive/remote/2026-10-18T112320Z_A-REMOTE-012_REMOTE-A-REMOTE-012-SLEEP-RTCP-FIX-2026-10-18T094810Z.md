# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-012-SLEEP-RTCP-FIX-2026-10-18T094810Z
- Updated (UTC): 2026-10-18T09:48:10Z
- Task ID: A-REMOTE-012
- Status: READY FOR REVIEW
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `0ddffb34c1832b5988b9c53fde5852b5b2b4e531`

## Milestone
Identify the remaining RTCP transport instability and correct it only when demonstrated. A synchronized dual-device capture and passive REMOTE log confirmed the initiating REMOTE sleep-order defect; the minimum private correction, targeted tests and production build are complete. Hardware installation and stability validation are not yet authorized or performed.

## Baseline
- Device repository: private REMOTE workspace and public TUNER commit `073b65963e3ed8e3438bc34134f5a903fce995de`
- Branch: REMOTE NONE (Git-less private workspace); TUNER `a-remote-012-low-latency`
- Firmware baseline commit: REMOTE UNKNOWN (Git-less); TUNER `073b65963e3ed8e3438bc34134f5a903fce995de`
- Firmware version: installed REMOTE timing candidate, 2,526,800 bytes, SHA-256 `a466336cd4fc3bc0e7d911ef2f50a6cf07a2e970d1dfbde5099fd1170eaf65b3`; installed TUNER scheduling candidate, 2,037,152 bytes, SHA-256 `19c39f4721ff43b939806f18aee599203225afde384c07934d58f1d0cc0398e8`
- Working tree at start: coordination clean; REMOTE contained the verified diagnostic source; TUNER inspected read-only at the installed commit
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2; coordination input `0ddffb34c1832b5988b9c53fde5852b5b2b4e531`

## Changes
Private REMOTE only: `components/power_management/runtime.cpp` now requests and verifies Core parking before `network_manager::sleep_prepare()`. If Core refuses because an RTCP request is pending, the attempt returns to DISPLAY_IDLE without stopping Wi-Fi or changing network generation. `tests/control/network_sleep_boundary_tests.py` now guards this ordering and refusal behavior. No protocol, timeout, retry, pairing, CCM, volume, TUNER or partition behavior changed.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Synchronized endpoint window | TUNER serial `x`, REMOTE `/api/status`, wait for first close, repeat once | Installed candidates; no commands except read-only diagnostic | PASS capture; REMOTE network generation +2 and one refused sleep attempt; TUNER snapshots 662/662 to 670/670, EOF +3, timeout +3, zero write/allocation failure | `references/device_evidence/remote/A-REMOTE-012/REMOTE_RTCP_TIMING_DIAGNOSTICS.json` |
| Refusal-stage capture | Passive REMOTE UART for one bounded 70-second window | Installed REMOTE timing candidate | PASS; network prepared, Core refused with `pending=1`, network resumed | same evidence |
| Sleep-boundary regression | `python tests/control/network_sleep_boundary_tests.py` | Python host | PASS; 23 assertions | same evidence |
| Network-sleep model | compile/run `tests/control/network_sleep_tests.cpp` with MSYS2 UCRT64 GCC | GCC 16.2.0 host | PASS; 9/9, 5,062 assertions | same evidence |
| Power lifecycle | compile/run `tests/control/power_tests.cpp` with MSYS2 UCRT64 GCC | GCC 16.2.0 host | PASS; 19/19, 19,236 assertions | same evidence |
| Production build | `platformio run -e remote01` | Espressif32 6.13.0; ESP-IDF 5.5.3 | PASS; 2,526,848 bytes; SHA-256 `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da`; static RAM 47,388 bytes; OTA headroom 618,880 bytes | private build artifact; sanitized identity in same evidence |

## Remaining unknowns
The correction has not been installed. Hardware must demonstrate that a pending RTCP request no longer changes network generation during a refused sleep attempt, that RTCP remains stable while REMOTE is awake, and that a later successful sleep/wake still invalidates and restores the session without stale command replay.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; CCM 1.1.0 remains OWNER APPROVED / FROZEN.
- TUNER Native API v1: NO CHANGE.
- Other device impact: TUNER source and firmware unchanged; it should stop seeing REMOTE-induced EOF/timeout bursts after validation.
- Approval evidence: owner authorized source analysis and the minimum source correction/build only after demonstrated cause; physical installation remains separately gated.

## Blockers
Explicit owner authorization is required before application-only installation of the new REMOTE candidate.

## PM decision required
Approve or reject installation of the 2,526,848-byte REMOTE candidate with SHA-256 `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da` for bounded stability and sleep/wake validation.

## Recommended next task
Reverify rollback backups and candidate identity, flash only the REMOTE application at `0x10000`, verify full-span readback, then observe both endpoints while awake and across one normal idle sleep/wake cycle. Confirm no network-generation change on a pending sleep refusal, stable authoritative volume, and no stale command replay. Do not modify TUNER.

## Commit
- Firmware result commit(s): REMOTE NONE (Git-less private workspace); private source changed only in `components/power_management/runtime.cpp` and its boundary test
- Device changelog: coordination `CHANGELOG.md`; private REMOTE source has no repository changelog
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18; final coordination hash reported after publication
- Previous handoff archive: `archive/remote/2026-10-18T093722Z_A-REMOTE-012_TRANSPORT-INVESTIGATION.md`

## Hardware status
- Physical device tested: YES, read-only synchronized REMOTE/TUNER diagnostics; corrected candidate NOT INSTALLED
- Board / hardware configuration: REMOTE Waveshare ESP32-S3-Touch-LCD-3.49B V2, PCB Rev1.1; TUNER unchanged
- Procedure and result: synchronized snapshots and passive REMOTE UART confirmed the sleep-order root cause; no persistent operation occurred
- Firmware actually flashed: REMOTE remains 2,526,800 bytes, SHA-256 `a466336cd4fc3bc0e7d911ef2f50a6cf07a2e970d1dfbde5099fd1170eaf65b3`; TUNER remains 2,037,152 bytes, SHA-256 `19c39f4721ff43b939806f18aee599203225afde384c07934d58f1d0cc0398e8`
- Build-only or simulated checks: corrected REMOTE candidate 2,526,848 bytes, SHA-256 `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da`; three targeted suites PASS; production build PASS
