# TUNER//01 handoff

## Metadata
- Handoff ID: TUNER-A-REMOTE-012-V1.1.12-RELEASED-2026-10-19T155925Z
- Updated (UTC): 2026-10-19T15:59:25Z
- Task ID: A-REMOTE-012
- Status: ACCEPTED
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `78e033f19d5c868251c62421fbc7c73303421f5e`

## Milestone
Correct the reproduced A2DP/network coexistence failure and complete final paired validation. Achieved for the recorded hobby/public-beta acceptance scope.

## Baseline
- Device repository: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio
- Branch: `main`; integration PR: [#6](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/pull/6)
- Firmware executable source: `d112dd0bbef7d86bd22090ec75d76cad3be77677`; integration merge: `4977b49756820edc149acbe1abe4d387a96aa992`
- Firmware version: `1.1.12`; embedded build `d112dd0bbef7`; 2,037,632 bytes; SHA-256 `6d7f2ebfa833bd09f287b8a7024071d736dfb2bf02356f889de94d7b980fdf6a`; [release](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/releases/tag/v1.1.12)
- Working tree at start: clean; exact version-only source commit built, hardware validated, merged and released
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 accepted binding

## Changes
`src/audio.cpp` releases unused BLE controller memory before first initialization and starts the controller explicitly in Classic-only mode. `tests/test_bluetooth_classic_memory_policy.py` provides focused source-policy coverage. Restartable A2DP lifecycle and unrelated audio/network behavior remain unchanged.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Focused policy test | Existing committed test | Host | PASS; 10/10 | TUNER commit `24395bad10bbca23da5de75062faaf423c453ada` |
| v1.1.12 production build | `pio run -e esp32-lwip-psram` | Production PlatformIO environment | PASS; 2,037,632 bytes; 1,108,096-byte binary slot headroom; 87,512-byte static DRAM | `references/device_evidence/tuner/A-REMOTE-012/V1_1_12_RELEASE.json` |
| v1.1.12 installation/readback | Application-only write at `0x10000`, independent 460800-baud exact-span readback | Physical TUNER | PASS; SHA-256 exact | same evidence |
| MP3 coexistence | HTTP/RTCP observation with owner-confirmed audible playback | Physical pair | PASS; 15/15 | same evidence |
| A2DP coexistence and recovery | HTTP/RTCP observation with owner-confirmed audio, then return to MP3 | Physical pair | PASS; A2DP 15/15, recovery 10/10 | same evidence |

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
- Firmware result commit(s): executable source `d112dd0bbef7d86bd22090ec75d76cad3be77677`; integration merge `4977b49756820edc149acbe1abe4d387a96aa992`; tag `v1.1.12`
- Device changelog: TUNER source commit and coordination `CHANGELOG.md`
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18
- Previous handoff archive: `archive/tuner/2026-10-19T155925Z_A-REMOTE-012_TUNER-A-REMOTE-012-ACCEPTED-2026-10-18T165659Z.md`

## Hardware status
- Physical device tested: YES
- Board / hardware configuration: existing classic ESP32 TUNER; 4 MiB flash; unchanged 3 MiB application slot
- Procedure and result: exact readback, boot, MP3 and post-fix A2DP HTTP/RTCP coexistence PASS for recorded scope
- Firmware actually flashed: v1.1.12 2,037,632-byte application at `0x10000`, SHA-256 above; exact readback PASS
- Build-only or simulated checks: focused policy test 10/10 and production build PASS
