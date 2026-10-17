# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-012-LIFECYCLE-DIAGNOSTIC-2026-10-17T174748Z
- Updated (UTC): 2026-10-17T17:47:48Z
- Task ID: A-REMOTE-012
- Status: READY FOR REVIEW
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `2dd69af384920e3866f53ffaa5c41810945542e8`

## Milestone
Identify the exact REMOTE RTCP close initiator using existing evidence, or prepare only the minimum bounded diagnostics if existing evidence cannot distinguish it. Evidence excludes expected sleep/network lifecycle as the scale explanation, but the exact close branch remains unknown. A diagnostic-only REMOTE candidate is built and awaits separately authorized hardware validation.

## Baseline
- Device repository: private REMOTE workspace; source remains unpublished
- Branch: NONE - active private workspace is Git-less
- Firmware baseline commit: UNKNOWN - Git-less source
- Firmware version: installed A-REMOTE-012 candidate, 2,525,168 bytes, SHA-256 `afd8b426b37cdac5bfd32abf4ee9fbf70c91e3a28ebdf74ae482871572dcdef4`
- Working tree at start: existing A-REMOTE-012 private changes; no Git metadata
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2; coordination input `2dd69af384920e3866f53ffaa5c41810945542e8`

## Changes
Private REMOTE changes add explicit fixed close classification and accurate EOF/socket-error distinction in the existing RTCP client, export the last reason and saturating count through the existing bounded diagnostics, and add focused tests. No transport, timeout, retry, crypto, framing, pairing, CCM or control behavior changed. One stale host-test assertion was updated from the superseded adjacent-only target rule to the approved A-REMOTE-012 absolute target while retaining disconnect/session rejection.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Hardware evidence correlation | Compare retained initial/final REMOTE status and TUNER counters | Installed physical A-REMOTE-012 pair; read-only evidence | PASS; 245 sessions cannot be explained by +2 sleep requests, +1 wake or +4 network generations | `references/device_evidence/remote/A-REMOTE-012/REMOTE_LIFECYCLE_DIAGNOSTIC_BUILD.json` |
| RTCP diagnostic/readiness/wire/lifecycle | Focused native C++ and source-policy tests | GCC 16.2.0 with temporary UCRT64 PATH | PASS; 44 cases/checks including 128 repeated snapshot parses | same evidence |
| CCM volume/session lifecycle | Volume admission and encoder/session invalidation tests | Native host | PASS; 13/13, 190 assertions | same evidence |
| Sleep/wake and network lifecycle | Focused power and network-sleep tests | Native host | PASS; 28/28, 24,298 assertions | same evidence |
| Diagnostic memory/schema | Fixed-layout status test | Native host | PASS; 9/9, 9,089 assertions; `Snapshots` remains 1,024 bytes | same evidence |
| Production build | `platformio run -e remote01` | PlatformIO Espressif32 6.13.0, ESP-IDF 5.5.3 | PASS; 2,525,696 bytes, SHA-256 `a421cb73411a19bf650c78de6bf048faf6e4ac65019f4180ab3de097c40cd798`; 620,032-byte slot headroom; 47,388-byte static RAM | same evidence |

## Remaining unknowns
The last hardware run cannot identify whether response timeout, peer EOF, socket error, invalid/partial record, network loss or suspend initiated the repeated REMOTE teardowns. The diagnostic candidate has not been installed. Physical latency, reconnect/sleep safety and MP3/A2DP/web-manager coexistence remain unaccepted for A-REMOTE-012.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; current project contract remains CCM 1.1.0 OWNER APPROVED / FROZEN.
- TUNER Native API v1: NO CHANGE.
- Other device impact: NONE in source or firmware; TUNER remains on installed scheduling candidate `19c39f...e8`.
- Approval evidence: owner authorized REMOTE lifecycle investigation, justified source changes, affected tests, production build and documentation; hardware flashing remains prohibited.

## Blockers
Exact RTCP close initiator requires one separately authorized installation and bounded passive observation of the new close-reason fields. Intentional volume performance testing remains blocked until stable fresh authority is restored.

## PM decision required
Authorize application-only installation of the exact REMOTE diagnostic candidate and one no-input awake observation, or retain the current installed artifact. Do not authorize a correction until a close reason is captured.

## Recommended next task
Verify rollback and device identity, install only the REMOTE application at `0x10000`, require exact readback, then capture initial/final REMOTE close reason/count and matching TUNER EOF counters during one recurrence. Stop without volume commands or additional fixes.

## Commit
- Firmware result commit(s): NONE - private REMOTE workspace is Git-less; exact candidate bound by size/hash
- Device changelog: private workspace has no Git changelog publication; coordination `CHANGELOG.md` records sanitized result
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18; final coordination hash reported after publication
- Previous handoff archive: `archive/remote/2026-10-17T174748Z_A-REMOTE-012_RTCP-STABILITY-FAIL.md`

## Hardware status
- Physical device tested: NO in this operation
- Board / hardware configuration: Waveshare ESP32-S3-Touch-LCD-3.49B V2, PCB Rev1.1; partition/GPIO state unchanged
- Procedure and result: NOT RUN; hardware access and flashing prohibited
- Firmware actually flashed: unchanged installed A-REMOTE-012 candidate, 2,525,168 bytes, SHA-256 `afd8b426b37cdac5bfd32abf4ee9fbf70c91e3a28ebdf74ae482871572dcdef4`
- Build-only or simulated checks: affected native tests and one `remote01` production build PASS; no physical root-cause claim
