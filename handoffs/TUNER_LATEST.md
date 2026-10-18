# TUNER//01 handoff

## Metadata
- Handoff ID: TUNER-A-REMOTE-012-ACCEPTED-2026-10-18T165659Z
- Updated (UTC): 2026-10-18T16:56:59Z
- Task ID: A-REMOTE-012
- Status: ACCEPTED
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `2aef37bcce307db450d164c456fefa6b9d219ba4`

## Milestone
Correct the reproduced A2DP/network coexistence failure and complete final paired validation. Achieved for the recorded hobby/public-beta acceptance scope.

## Baseline
- Device repository: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio
- Branch: `a-remote-012-low-latency`
- Firmware baseline commit: `24395bad10bbca23da5de75062faaf423c453ada`
- Firmware version: embedded build `24395bad10bb`; 2,037,648 bytes; SHA-256 `6310a960f96c382d653a5b44f1b8e828f15985b59a40111308c475cf084c72a1`
- Working tree at start: clean; correction committed and published
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 accepted binding

## Changes
`src/audio.cpp` releases unused BLE controller memory before first initialization and starts the controller explicitly in Classic-only mode. `tests/test_bluetooth_classic_memory_policy.py` provides focused source-policy coverage. Restartable A2DP lifecycle and unrelated audio/network behavior remain unchanged.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Focused policy test | Existing committed test | Host | PASS; 10/10 | TUNER commit `24395bad10bbca23da5de75062faaf423c453ada` |
| Production build | `pio run -e esp32-lwip-psram` | Production PlatformIO environment | PASS; 2,037,648 bytes; 1,108,080-byte headroom; 87,512-byte static DRAM | `references/device_evidence/remote/A-REMOTE-012/FINAL_ACCEPTANCE_POST_FIX_2026-10-18.json` |
| Installation/readback | Application-only write at `0x10000`, exact-span readback | Physical TUNER | PASS; SHA-256 exact | same evidence |
| MP3 coexistence | HTTP/web/RTCP observation with audible playback | Physical pair | PASS | same evidence |
| A2DP coexistence | 24-sample diagnostic/web observation and post-wake RTCP check | Physical pair | PASS for recorded windows | same evidence |

## Remaining unknowns
No merge blocker. Quantitative latency is owner-waived and not measured. Long-duration A2DP behavior beyond the recorded windows is not claimed. E-paper feedback remains slower than audio response.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE; CCM 1.1.0 remains current OWNER APPROVED / FROZEN
- TUNER Native API v1: NO CHANGE
- Other device impact: REMOTE firmware and pairing unchanged; authenticated RTCP recovery verified
- Approval evidence: owner final acceptance and A-REMOTE-012-only latency waiver recorded in `references/device_evidence/remote/A-REMOTE-012/FINAL_ACCEPTANCE_POST_FIX_2026-10-18.json`

## Blockers
NONE for PR #18 merge review.

## PM decision required
Owner authorization is required to merge PR #18.

## Recommended next task
NONE assigned. Preserve rollback artifacts; schedule later work independently.

## Commit
- Firmware result commit(s): `24395bad10bbca23da5de75062faaf423c453ada`
- Device changelog: TUNER source commit and coordination `CHANGELOG.md`
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18
- Previous handoff archive: `archive/tuner/2026-10-18T165659Z_A-REMOTE-012_TUNER-A-REMOTE-012-FINAL-VALIDATION-2026-10-18T112320Z.md`

## Hardware status
- Physical device tested: YES
- Board / hardware configuration: existing classic ESP32 TUNER; 4 MiB flash; unchanged 3 MiB application slot
- Procedure and result: exact readback, boot, MP3 and post-fix A2DP HTTP/RTCP coexistence PASS for recorded scope
- Firmware actually flashed: 2,037,648-byte application at `0x10000`, SHA-256 above
- Build-only or simulated checks: focused policy test 10/10 and production build PASS
