# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-012-NETWORK-STATUS-FIX-2026-10-17T181203Z
- Updated (UTC): 2026-10-17T18:12:03Z
- Task ID: A-REMOTE-012
- Status: READY FOR REVIEW
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `6ed4f4868e974494190e096a39a4d6713f4d4a52`

## Milestone
Correct the confirmed false `network_lost` RTCP teardown without changing protocol or control semantics, add deterministic lifecycle regressions and produce one verified REMOTE production candidate. Software acceptance passed; hardware installation remains separately gated.

## Baseline
- Device repository: private REMOTE workspace; source remains unpublished
- Branch: NONE - active private workspace is Git-less
- Firmware baseline commit: UNKNOWN - Git-less source
- Firmware version: installed lifecycle diagnostic application, 2,525,696 bytes, SHA-256 `a421cb73411a19bf650c78de6bf048faf6e4ac65019f4180ab3de097c40cd798`
- Working tree at start: existing private A-REMOTE-012 lifecycle diagnostic source and validated low-latency implementation
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2; coordination input `6ed4f4868e974494190e096a39a4d6713f4d4a52`

## Changes
Added a fixed `NetworkStatusGate` to the REMOTE RTCP client. A transient unavailable zero-wait network snapshot now preserves the live socket and generation baseline. A confirmed disconnected snapshot still closes immediately with `network_lost`. A connected snapshot with a changed generation closes an active transport; when no transport exists after sleep/wake, the current generation is adopted before reconnecting. Close diagnostics and all existing security, timeout, retry, pairing and volume behavior remain unchanged.

Private files changed: `components/rtcp_client/client.cpp`, `components/rtcp_client/include/rtcp_client/client.hpp`, new `network_status.hpp`, new `tests/rtcp_client/network_status_tests.cpp`, and `tests/rtcp_client/lifecycle_policy_tests.py`.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Network decision model | Compile/run `network_status_tests.cpp` | GCC 16.2.0 with UCRT64 PATH | PASS; 15 checks, 142 assertions | `references/device_evidence/remote/A-REMOTE-012/REMOTE_NETWORK_STATUS_FIX_BUILD.json` |
| RTCP lifecycle and support suites | Lifecycle policy, diagnostic, I/O, readiness and association/wire tests | Native host | PASS; 13 + 9 + 5 + 9 + 11 checks | same evidence |
| Sleep/wake and network lifecycle | Power, network-sleep and boundary tests | Native host | PASS; 19/19 + 9/9 + 1/1, 24,319 assertions | same evidence |
| Production build | `pio run -e remote01` | Espressif32 6.13.0, ESP-IDF 5.5.3 | PASS; 2,525,808 bytes, SHA-256 `1ca95a1abe31e990d28d125f0994610f88dc554efa8acb744cef866759033477` | same evidence |
| Memory/slot | PlatformIO size plus exact binary length | `remote01`, 3 MiB application slot | PASS; 47,388-byte static RAM, 619,920-byte slot headroom | same evidence |

## Remaining unknowns
Physical stability after the correction is NOT VERIFIED. Real confirmed Wi-Fi loss, normal sleep/wake, RTCP recovery and the final volume latency/coexistence criteria require a separately authorized installation and bounded hardware test. The existing installed diagnostic firmware remains active.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; current project contract remains CCM 1.1.0 OWNER APPROVED / FROZEN.
- TUNER Native API v1: NO CHANGE.
- Other device impact: NONE in source or firmware; TUNER remains on its installed A-REMOTE-012 scheduling candidate.
- Approval evidence: owner authorized the minimum REMOTE correction, affected tests, one production build and sanitized PR #18 documentation; hardware flashing remains prohibited.

## Blockers
Hardware acceptance is blocked only on explicit owner authorization to install the exact candidate and perform the bounded passive paired stability test.

## PM decision required
Authorize one REMOTE application-only installation of the 2,525,808-byte candidate at `0x10000`, exact readback, normal boot verification and one no-input awake stability window. Do not authorize volume commands until stable authority passes.

## Recommended next task
Revalidate the existing rollback sets and device identity, install only the candidate application, require SHA-256 readback, then compare close/session/network counters over five minutes with TUNER unchanged.

## Commit
- Firmware result commit(s): NONE - private REMOTE workspace is Git-less; candidate bound by exact size/hash
- Device changelog: private workspace has no public source changelog; coordination `CHANGELOG.md` records the result
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18; final coordination hash reported after publication
- Previous handoff archive: `archive/remote/2026-10-17T181203Z_A-REMOTE-012_REMOTE-LIFECYCLE-ROOT-CAUSE.md`

## Hardware status
- Physical device tested: NO
- Board / hardware configuration: Waveshare ESP32-S3-Touch-LCD-3.49B V2, PCB Rev1.1; layout and GPIO state unchanged
- Procedure and result: NOT RUN; hardware access and flashing prohibited
- Firmware actually flashed: unchanged installed lifecycle diagnostic, 2,525,696 bytes, SHA-256 `a421cb73411a19bf650c78de6bf048faf6e4ac65019f4180ab3de097c40cd798`
- Build-only or simulated checks: affected native suites and one `remote01` production build PASS
