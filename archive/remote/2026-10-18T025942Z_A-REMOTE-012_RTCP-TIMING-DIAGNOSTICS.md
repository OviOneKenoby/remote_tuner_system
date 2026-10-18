# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-012-RTCP-TIMING-DIAGNOSTICS-2026-10-18T025942Z
- Updated (UTC): 2026-10-18T02:59:42Z
- Task ID: A-REMOTE-012
- Status: READY FOR REVIEW
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `81e875f64d6fc5ec85fda11b758fbb2082ee7b61`

## Milestone
Add only the bounded evidence needed to distinguish REMOTE RTCP scheduling starvation from a response that was absent at the unchanged three-second deadline. Source, focused verification and one production build passed. Hardware installation remains separately gated.

## Baseline
- Device repository: private REMOTE workspace; source remains unpublished
- Branch: NONE - active private workspace is Git-less
- Firmware baseline commit: UNKNOWN - Git-less source
- Firmware version: installed volume-reconciliation correction, 2,525,824 bytes, SHA-256 `3f46c3ccfd45b29985bbda37f1357a8f36831c17066bd0a33952f238936290bf`; exact readback and rapid-volume hardware validation PASS
- Working tree at start: existing private A-REMOTE-012 corrections plus four interrupted, uncommitted diagnostic edits; preserved and completed without reset or overwrite
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2; coordination input `81e875f64d6fc5ec85fda11b758fbb2082ee7b61`

## Changes
The private REMOTE source records the last and maximum interval between `Client::poll()` calls. Immediately before an actual `response_timeout`, it retains the client state, elapsed request deadline, a safe nonblocking `FIONREAD` queued-byte result and a saturating count of timeouts where unread bytes were present. Successful reconnects do not erase this timeout snapshot. The existing `/api/status` exposes fixed, secret-free values; timing uses 32 ms ceiling units to keep the existing diagnostic limits. Network RSSI and `http_dns_off` retain their prior meaning in natural bounded fields. No timeout, retry, socket lifecycle, protocol, CCM, pairing, session or volume behavior changed.

Private files changed: `components/rtcp_client/include/rtcp_client/diagnostic.hpp`, `components/rtcp_client/client.cpp`, `components/control_home/runtime.cpp`, `components/diagnostics/include/diagnostics/model.hpp`, `components/diagnostics/model.cpp`, `components/network_manager/runtime.cpp`, `tests/rtcp_client/diagnostic_tests.cpp`, and `tests/control/diagnostics_tests.cpp`.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| RTCP timing retention | Compile/run `tests/rtcp_client/diagnostic_tests.cpp` | GCC 16.2.0, temporary UCRT64 PATH | PASS; 13/13 | `references/device_evidence/remote/A-REMOTE-012/REMOTE_RTCP_TIMING_DIAGNOSTICS.json` |
| Status schema and memory guards | Compile `components/diagnostics/model.cpp` with `tests/control/diagnostics_tests.cpp`; run once | GCC 16.2.0, temporary UCRT64 PATH | PASS; 9/9, 9,096 assertions; `Snapshots` 1,024 bytes; total storage 8,192 bytes | same evidence |
| Production build | PlatformIO `run -e remote01` | Espressif32 6.13.0; ESP-IDF 5.5.3; ESP32-S3 | PASS; 2,526,800 bytes; SHA-256 `a466336cd4fc3bc0e7d911ef2f50a6cf07a2e970d1dfbde5099fd1170eaf65b3` | same evidence |
| Memory/slot | PlatformIO size plus exact binary length | `remote01`; 3 MiB application slot | PASS; 47,388-byte static RAM; 618,928-byte headroom | same evidence |
| Physical timing observation | Install candidate and observe retained fields | REMOTE//01 | NOT RUN; hardware access prohibited in this task | NONE |

## Remaining unknowns
The evidence has not yet determined whether response timeouts coincide with a REMOTE poll gap, unread queued socket data, or no TUNER response. `FIONREAD` may return unavailable (`-1`) if the platform rejects the query; no blocking fallback was added. Public millisecond fields are ceiling-quantized to 32 ms and saturate at 8,160 ms; the private retained model remains full-width.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; CCM 1.1.0 remains OWNER APPROVED / FROZEN.
- TUNER Native API v1: NO CHANGE.
- Other device impact: NONE; TUNER source and firmware were not modified.
- Approval evidence: owner authorized bounded REMOTE timing diagnostics, directly affected tests, one production build and essential PR #18 documentation; flashing remains unauthorized.

## Blockers
Root-cause classification requires one separately authorized REMOTE application-only installation and passive read-only observation. No software/build blocker remains.

## PM decision required
Authorize or decline installation of the exact 2,526,800-byte REMOTE candidate at `0x10000`, exact readback, and one passive observation with no control input.

## Recommended next task
After normal identity and rollback preflight, install only the candidate application and require exact readback SHA-256. Keep REMOTE awake with TUNER online and issue no control command. Capture `/api/status` before observation and at the first `response_timeout` (or after five minutes): `rtcp_close_reason`, `rtcp_close_count`, `rtcp_failure`, `rtcp_error`, `rtcp_poll_last_ms`, `rtcp_poll_max_ms`, `rtcp_timeout_state`, `rtcp_timeout_elapsed_ms`, `rtcp_timeout_queued_bytes`, `rtcp_timeouts_with_unread`, session and connection counters. Stop after that single bounded observation.

## Commit
- Firmware result commit(s): NONE - private REMOTE workspace is Git-less; artifact is bound by exact size/hash
- Device changelog: NONE - private source workspace has no public changelog commit
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18; final coordination hash reported after publication
- Previous handoff archive: `archive/remote/2026-10-17T184055Z_A-REMOTE-012_VOLUME-RECONCILIATION-FIX.md`

## Hardware status
- Physical device tested: NO for this diagnostic candidate; prior volume-reconciliation firmware and rapid-volume behavior were tested and passed
- Board / hardware configuration: Waveshare ESP32-S3-Touch-LCD-3.49B V2, PCB Rev1.1; layout and GPIO state unchanged
- Procedure and result: NOT RUN for this candidate; no hardware access authorized
- Firmware actually flashed: prior 2,525,824-byte application, SHA-256 `3f46c3ccfd45b29985bbda37f1357a8f36831c17066bd0a33952f238936290bf`
- Build-only or simulated checks: RTCP timing retention 13/13; diagnostics/schema 9/9 with 9,096 assertions; one `remote01` production build PASS
