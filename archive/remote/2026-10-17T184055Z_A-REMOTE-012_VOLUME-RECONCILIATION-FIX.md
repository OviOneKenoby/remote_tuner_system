# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-012-VOLUME-RECONCILIATION-FIX-2026-10-17T184055Z
- Updated (UTC): 2026-10-17T18:40:55Z
- Task ID: A-REMOTE-012
- Status: READY FOR REVIEW
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `9e685ab1c49c8e8cbf2ed7d0ccccefc3db884af5`

## Milestone
Correct the demonstrated loss of accepted rapid encoder detents during post-result authoritative reconciliation, retain bounded coalescing and produce one verified REMOTE production candidate. Software acceptance passed; corrected-candidate hardware installation remains separately gated.

## Baseline
- Device repository: private REMOTE workspace; source remains unpublished
- Branch: NONE - active private workspace is Git-less
- Firmware baseline commit: UNKNOWN - Git-less source
- Firmware version: installed network-status correction, 2,525,808 bytes, SHA-256 `1ca95a1abe31e990d28d125f0994610f88dc554efa8acb744cef866759033477`
- Working tree at start: existing private A-REMOTE-012 network-status correction source and validated low-latency implementation
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2; coordination input `9e685ab1c49c8e8cbf2ed7d0ccccefc3db884af5`

## Changes
`Channel::publish()` now classifies confirmed divergent authority only when the incoming authoritative volume changed from the previously published value. This prevents the 5 ms owner loop's unchanged pre-command snapshot from clearing a newer accumulated target before the 1 s RTCP acquisition refresh. A genuinely changed divergent value still cancels obsolete local intent. Private files changed: `components/control_home/include/control_home/api.hpp` and `tests/control/volume_admission_tests.cpp`.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Hardware reproduction | Exactly ten downward detents from 53%, compare bounded counters and authority | Installed prior A-REMOTE-012 candidate | FAIL reproduced: 10 accepted, 5 submissions, final 48%, expected 43%, no operation in flight | `references/device_evidence/remote/A-REMOTE-012/REMOTE_VOLUME_RECONCILIATION_FIX.json` |
| Volume reconciliation regression | Compile/run `volume_admission_tests.cpp` | GCC 16.2.0 with UCRT64 PATH | PASS; 9/9, 238 assertions; equal ten-detent slow/rapid sequences both final 43%; reversal PASS | same evidence |
| Production build | PlatformIO `run -e remote01` | Espressif32 6.13.0, ESP-IDF 5.5.3 | PASS; 2,525,824 bytes, SHA-256 `3f46c3ccfd45b29985bbda37f1357a8f36831c17066bd0a33952f238936290bf` | same evidence |
| Memory/slot | PlatformIO size plus exact binary length | `remote01`, 3 MiB application slot | PASS; 47,388-byte static RAM, 619,904-byte slot headroom | same evidence |

## Remaining unknowns
The corrected candidate is NOT physically installed. Exact ten-detent accumulation, rapid reversal, audible latency, authoritative settling, sleep/wake replay safety and MP3/A2DP/web-manager coexistence require bounded hardware validation.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; current project contract remains CCM 1.1.0 OWNER APPROVED / FROZEN.
- TUNER Native API v1: NO CHANGE.
- Other device impact: NONE; TUNER source and firmware are unchanged.
- Approval evidence: owner authorized the demonstrated REMOTE reconciliation correction, targeted regression, one production build and necessary PR #18 documentation; flashing remains prohibited.

## Blockers
Hardware acceptance requires explicit owner authorization to install the exact corrected REMOTE candidate and run the bounded control test.

## PM decision required
Authorize one REMOTE application-only installation of the 2,525,824-byte candidate at `0x10000`, exact readback, normal boot verification, one isolated ten-detent 53% to 43% test and one rapid reversal test. Keep TUNER unchanged.

## Recommended next task
After normal rollback/device preflight, install only the corrected application, require exact readback, then capture before/after detent, accepted-intent, dispatch, authority and in-flight fields. Stop on any lost accepted detent or stale replay.

## Commit
- Firmware result commit(s): NONE - private REMOTE workspace is Git-less; candidate bound by exact size/hash
- Device changelog: private source workspace has no public source commit; coordination `CHANGELOG.md` records the result
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18; final coordination hash reported after publication
- Previous handoff archive: `archive/remote/2026-10-17T184055Z_A-REMOTE-012_NETWORK-STATUS-FIX.md`

## Hardware status
- Physical device tested: YES for the installed prior network-status candidate and defect reproduction; NO for the corrected candidate
- Board / hardware configuration: Waveshare ESP32-S3-Touch-LCD-3.49B V2, PCB Rev1.1; layout and GPIO state unchanged
- Procedure and result: prior candidate installation/readback/essential boot PASS; ten accepted downward detents reproduced final 48% instead of expected 43%
- Firmware actually flashed: 2,525,808 bytes, SHA-256 `1ca95a1abe31e990d28d125f0994610f88dc554efa8acb744cef866759033477`
- Build-only or simulated checks: focused reconciliation 9/9 PASS, 238 assertions; one `remote01` production build PASS before the test-only slow/rapid comparison
