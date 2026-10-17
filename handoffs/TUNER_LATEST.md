# TUNER//01 handoff

## Metadata
- Handoff ID: TUNER-A-REMOTE-012-POST-IDENTITY-DIAGNOSTIC-BUILD-20261017T071246Z
- Updated (UTC): 2026-10-17T07:12:46Z
- Task ID: A-REMOTE-012
- Status: READY FOR HARDWARE DIAGNOSTIC REVIEW
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: c070cd941e2a639988c864f8bc9b53bc27c7e47f

## Milestone
Add the smallest bounded evidence needed to locate the first post-capability snapshot failure. Source, focused tests and production build pass; installation is not authorized or run.

## Baseline
- Device repository: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio
- Branch: `a-remote-012-low-latency`
- Firmware baseline commit: 5391beef5e7ba264362ea19f2fdd93202308fa55
- Firmware version: v1.1.11 plus A-REMOTE-012
- Working tree at start: clean; final source commit `fda5f1ad1e5ebb9e83238cdbaa3ad79564e40842`
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2; coordination input `c070cd941e2a639988c864f8bc9b53bc27c7e47f`

## Changes
Added `src/rtcp_diagnostics.h`, integrated its fixed 60-byte state in `src/rtcp_server.h/.cpp`, and exposed one compact line through the existing serial snapshot in `src/main.cpp`. Added focused model and redaction/integration tests. The state records bounded request type, snapshot progression, response requested/written bytes, partial/failed writes, close reason, heap and allocation-failure delta. It stores no secret or payload and performs no dynamic diagnostic allocation.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Diagnostic model | native compile/run `tests/test_rtcp_diagnostics.cpp` | GCC 16.2.0, C++17 | PASS 11/11 | `references/device_evidence/remote/A-REMOTE-012/POST_IDENTITY_DIAGNOSTICS_BUILD.json` |
| Integration/redaction | `python tests/test_rtcp_diagnostics_policy.py` | Python 3.13 | PASS 14/14 | same evidence |
| RTCP scheduling regression | `python tests/test_rtcp_latency_policy.py` | Python 3.13 | PASS 9/9 | same evidence |
| CCM wire regression | native `test_ccm_wire.cpp` plus `src/ccm_wire.cpp` | GCC 16.2.0, C++17 | PASS 16/16 | same evidence |
| Production build | PlatformIO `run -e esp32-lwip-psram` | Espressif32 7.0.1, board `esp32dev` | PASS; 2,036,992 bytes, SHA-256 `18d59b75cbf481b517b09fd274207e2271cdd42a0a146f56eafeca2e8a1196d3` | same evidence |

## Remaining unknowns
Hardware has not shown which new counter/stage stops. Root cause remains unknown. The observed 2,304-byte free heap and 948-byte largest block remain non-causal evidence until allocation/write diagnostics demonstrate a relationship.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; CCM 1.1.0 remains frozen.
- TUNER Native API v1: NO CHANGE.
- Other device impact: no wire or behavior change; REMOTE needs no firmware change for diagnosis.
- Approval evidence: owner authorized diagnostic source changes, tests and production build only.

## Blockers
Application installation and one passive automatic-handshake observation require separate owner authorization.

## PM decision required
Authorize or reject application-only installation at `0x10000`, exact readback and one serial `x` snapshot with no control commands.

## Recommended next task
Follow the five-step minimal commissioning procedure in `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md`, then stop with the first proven server/transport boundary.

## Commit
- Firmware result commit(s): `fda5f1ad1e5ebb9e83238cdbaa3ad79564e40842`
- Device changelog: TUNER `CHANGELOG.md` and coordination `CHANGELOG.md`
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18; final hash reported after publication
- Previous handoff archive: `archive/tuner/2026-10-17T071246Z_A-REMOTE-012_TUNER-SNAPSHOT-BOUNDARY-UNKNOWN.md`

## Hardware status
- Physical device tested: NO for this candidate
- Board / hardware configuration: accepted classic ESP32 TUNER, 4 MiB flash, `esp32-lwip-psram`
- Procedure and result: source/test/build PASS; commissioning NOT RUN
- Firmware actually flashed: installed A-REMOTE-012 candidate remains unchanged
- Build-only or simulated checks: 11/11 + 14/14 + 9/9 + 16/16 PASS; production build PASS; static RAM 87,512 bytes; headroom 1,108,736 bytes
