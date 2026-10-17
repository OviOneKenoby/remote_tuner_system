# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-012-PRECOMMISSIONING-READY-20261017T071500Z
- Updated (UTC): 2026-10-17T07:15:00Z
- Task ID: A-REMOTE-012
- Status: READY FOR HARDWARE COMMISSIONING / HARDWARE PENDING
- Prepared by: REMOTE//01 executor with coordinated TUNER//01 implementation
- Coordination input commit: 437e79cdfd6b7febf001271a32467191d84b20d2

## Milestone
Implement and verify the low-latency EC11 volume path without weakening CCM 1.1.0 or RTCP/1, then complete the rollback and artifact preflight. Software and pre-commissioning review are complete; audible/UI timing and coexistence on physical hardware are NOT RUN and remain the acceptance gate.

## Baseline
- Device repository: private REMOTE workspace; source remains unpublished
- Branch: NONE - active private workspace is git-less
- Firmware baseline commit: UNKNOWN - git-less source; validated binary identity is recorded below
- Firmware version: A-REMOTE-011 validated private production application
- Working tree at start: active private source matched the accepted A-011 state for the eight scoped files; a reversible private source backup was created before editing
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2 profile; A-REMOTE-011 accepted implementation; coordination input `437e79cdfd6b7febf001271a32467191d84b20d2`

## Changes
Private source now coalesces admitted detents into a bounded absolute desired-volume target while retaining one command in flight. It requests an authoritative snapshot immediately after a result, enables TCP no-delay, reduces the control-owner cadence to 5 ms and displays a clearly provisional `authoritative>desired` value on a 20 ms LVGL refresh while retaining the authoritative bar. Confirmed external divergence cancels the obsolete successor; definite failure, uncertain delivery, disconnect, sleep and scope invalidation retain fail-closed/no-replay behavior. Changed private paths are enumerated in the public report without publishing contents.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Coalescing/lifecycle/performance | host compile/run of `volume_admission_tests.cpp` | GCC 16.2.0, C++23, Windows amd64 | PASS 8/8, 164 assertions | `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md` |
| UI provisional/authority boundary | `python tests/control/ui_volume_binding_tests.py` | Python 3.13, Windows amd64 | PASS 1/1, 11 assertions | `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md` |
| Full relevant regression | `python tests/control/run_tests.py` with MSYS2 UCRT64 on process PATH | GCC 16.2.0/Python 3.13, Windows amd64 | PASS; all listed suites | `reports/A-REMOTE-012_LOW_LATENCY_SOFTWARE.md` |
| Production build | PlatformIO `run -e remote01` | Espressif32 6.13.0, ESP-IDF 5.5.3, ESP32-S3 | PASS; 2,525,168 bytes, SHA-256 `afd8b426b37cdac5bfd32abf4ee9fbf70c91e3a28ebdf74ae482871572dcdef4`; RAM 47,388 | `references/device_evidence/remote/A-REMOTE-012/SOFTWARE_RESULT.json` |
| Controlled latency model | 15 detents over 56 ms, 30 ms simulated command/observation delay | bounded host model, not hardware | PASS; first audio 30 ms, final 34 ms after last, UI 20 ms, 3 submissions | `references/device_evidence/remote/A-REMOTE-012/SOFTWARE_RESULT.json` |

## Remaining unknowns
Physical detent-to-audio, continued-rotation and authoritative-UI latency are NOT RUN. The under-100 ms audible, under-50 ms provisional-UI and 250 ms final-target requirements require the published hardware procedure. Runtime heap/stack under paired MP3 and A2DP with the web manager active must also be observed. Unassigned physical-button functions and intermittent QMI8658 motion-wake initialization remain outside this task.

The retained REMOTE full-flash primary and local copy are each 16,777,216 bytes and match SHA-256 `31fd537c4bf534b101e74ed582bf0aa909235686207da29ad61413f21688b43d`. The owner-controlled external backup was populated previously but is not currently attached; reconnecting and verifying it is required before the first write.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; historical revision remains preserved and CCM 1.1.0 remains the current frozen contract.
- TUNER Native API v1: NO CHANGE; A-REMOTE-012 uses the accepted RTCP/1 binding.
- Other device impact: coordinated TUNER RTCP and local-encoder scheduling/timing implementation at `5391beef5e7ba264362ea19f2fdd93202308fa55`; wire format remains compatible.
- Approval evidence: owner A-REMOTE-012 mission and performance override dated 2026-10-16 authorize both source trees and builds, but no physical flashing.

## Blockers
Physical installation and measured latency require explicit owner authorization. The external backup must be reconnected and verified during the pre-write check. No software blocker is known.

## PM decision required
Authorize or reject the published TUNER-first application-only commissioning checklist. No merge or hardware authority is implied.

## Recommended next task
Commission TUNER first and REMOTE second using exact private hashes; measure audible and UI latency, submission count, final authority, MP3/A2DP/web coexistence and rollback readiness. This recommendation is not authorization.

## Commit
- Firmware result commit(s): REMOTE private source is uncommitted/git-less; TUNER public source `5391beef5e7ba264362ea19f2fdd93202308fa55`
- Device changelog: private REMOTE and public TUNER changelogs updated; sanitized coordination `CHANGELOG.md` updated
- Coordination publication: branch `remote/a-remote-012-low-latency`; PR and final coordination hash reported in publication message
- Previous handoff archive: `archive/remote/2026-10-17T071500Z_A-REMOTE-012_REMOTE-A-REMOTE-012-SOFTWARE-PASS-20261017T060600Z.md`

## Hardware status
- Physical device tested: NO
- Board / hardware configuration: Waveshare ESP32-S3-Touch-LCD-3.49B V2 PCB Rev1.1; accepted EC11 GPIO2/GPIO5 wiring retained
- Procedure and result: NOT RUN; only the reversible checklist was prepared
- Firmware actually flashed: A-011 rollback baseline remains the last validated REMOTE application: 2,523,936 bytes, SHA-256 `38b43de02bf1ef69b85678f0a67451836cb0a24e3bf1876283933b3185ed4d5d`
- Build-only or simulated checks: host regressions, bounded 30 ms latency model and `remote01` production build listed above
