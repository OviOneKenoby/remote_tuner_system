# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-010-DIAGNOSTIC-20261013T064309Z
- Updated (UTC): 2026-10-13T06:43:09.576743+00:00
- Task ID: A-REMOTE-010
- Status: DIAGNOSTIC CANDIDATE READY FOR OWNER REVIEW; HARDWARE NOT RUN
- Prepared by: authorized executor / coordination publisher
- Coordination input commit: e7aa84370098e1096bf18d87856de65a440a1c4a

## Milestone
Owner accepted the A-REMOTE-010 host phase and authorized a private, narrowly gated UART diagnostic candidate. Implemented and verified: 28/28 focused tests and one clean serial target build. No device access or persistent operation occurred.

## Baseline
- Device repository: owner-private REMOTE source; unpublished
- Diagnostic build: `remote01_a010_diag`, `A010_REMOTE_PERSISTENCE_DIAGNOSTIC=1`
- Normal build: `remote01`, diagnostic absent/disabled
- Installed physical state: accepted A-009 seven-entry table; existing factory firmware unchanged because hardware was not accessed
- Contract: CCM 1.1.0 frozen, G1a implemented at host level; G1b deliberate coherent-domain restore outside V1

## Changes
Private diagnostic parser/model, ESP-IDF target adapter and fixed command set added. The candidate reuses the existing single USB-serial reader and logs an explicit validation identity. Boot performs no persistence call. All mutations require exact candidate, command, confirmation token and partition identity. Public changes contain only authorization, sanitized evidence, report, protocol and status.

## Verification
| Check | Result | Evidence |
| --- | --- | --- |
| Backend regression tests | PASS 14/14 | `references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_HOST_TESTS_SANITIZED.log` |
| Diagnostic tests | PASS 14/14 | same |
| ESP-IDF adapter review | PASS; explicit labeled init/open/commit/cleanup/error mapping, no hidden erase | `reports/A-REMOTE-010_DIAGNOSTIC_CANDIDATE.md` |
| Clean candidate build | PASS, 492.70 seconds | `references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_BUILD_SANITIZED.log` |
| Firmware / OTA | 2,503,936 bytes / 641,792 bytes headroom | `references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_ARTIFACT_SHA256.json` |
| Partition image | exact A-009 byte match | same |
| ELF/build gate/no-boot-write | PASS source/config/symbol/string checks | `references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_RESULT.json` |
| Hardware | NOT RUN | owner boundary |

## Remaining unknowns
Physical UART behavior, candidate boot, target NVS initialization/commit/recovery/capacity, UI/configuration retention and restoration remain untested. Optional `remote_ctl` erase is separately gated. No power-cut/endurance campaign is planned.

## Shared-contract impact
- CCM 1.1.0: NO CHANGE
- Native/common API: unapproved/unimplemented; NO CHANGE
- TUNER: untouched
- O01–O17/common gate: OPEN / NOT PASSED
- A-REMOTE-011: NOT STARTED

## Owner decision required
Approve or reject hardware validation of the exact candidate. The first proposed operation is the read-only ROM/USB chip identity query on the newly verified COM port. Candidate flashing and each mutation stage require explicit authorization under the protocol.

## Commit
- Private firmware commit: NONE; source and artifacts remain private
- Coordination continuation: branch `remote/a-remote-010-private-backend-20261012`, PR #16; final head reported after publication
- Previous handoff archive: `archive/remote/2026-10-13T064309Z_A-REMOTE-010_REMOTE-A-REMOTE-010-PRIVATE-HOST-20261013T033507Z.md`

## Hardware status
- Physical device accessed: NO
- Firmware flashed: NO
- Flash/NVS writes or erases: ZERO
- Candidate artifact: built privately only
