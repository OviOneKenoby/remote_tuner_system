# TUNER//01 handoff

## Metadata
- Handoff ID: TUNER-A-REMOTE-012-RTCP-STABILITY-FAIL-2026-10-17T143224Z
- Updated (UTC): 2026-10-17T14:32:24Z
- Task ID: A-REMOTE-012
- Status: BLOCKED
- Prepared by: coordinated A-REMOTE-012 executor
- Coordination input commit: `9b6cce3b0217eea6ad7b0f7cb66dec00049c16e1`

## Milestone
Install the verified cooperative e-paper/RTCP scheduling correction and demonstrate stable authenticated synchronization for approximately five minutes. Exact installation passed and the prior loop stall was reduced; persistent RTCP stability failed.

## Baseline
- Device repository: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio
- Branch: `a-remote-012-low-latency`
- Firmware baseline commit: `fda5f1ad1e5ebb9e83238cdbaa3ad79564e40842`
- Firmware version: v1.1.11 plus A-REMOTE-012 low-latency, bounded diagnostics and scheduling correction
- Working tree at start: clean
- Contract references: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2; coordination input `9b6cce3b0217eea6ad7b0f7cb66dec00049c16e1`

## Changes
No source change in this operation. After exact rollback/candidate preflight, the accepted 2,037,152-byte TUNER application was written once at `0x10000`. No other flash region was written. Independent readback matched SHA-256 `19c39f4721ff43b939806f18aee599203225afde384c07934d58f1d0cc0398e8`.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Rollback preflight | Rehash eight local files and eight copies on separate physical USB storage | Owner-controlled local and USB storage | PASS; all 16 file/hash checks matched recorded identities | `references/device_evidence/remote/A-REMOTE-012/RTCP_SCHEDULING_FIX_HARDWARE_RESULT.json` |
| Device/candidate/slot preflight | esptool ROM identification, flash-size check, candidate size/hash and verified partition evidence | ESP32, 4 MiB flash, 3 MiB app slot | PASS | same evidence |
| Application installation | Application-only write at `0x10000`, 921600 baud; independent exact full-span readback | esptool 4.11.0 | PASS; 2,037,152 bytes and expected SHA-256 | same evidence |
| Boot/service | Passive boot and one existing read-only `x` snapshot | Installed TUNER candidate | PASS for initialization, retained Wi-Fi and audio service; active playback NOT RUN | same evidence |
| Five-minute RTCP stability | Initial/final snapshots around passive paired interval | Physical pair, no intentional command | FAIL; +262 connections and +262 peer EOFs, 523/523 additional snapshots completed, final REMOTE disconnected | same evidence |

## Remaining unknowns
The installed artifact reports embedded build ID `fda5f1ad1e5e` because it was built while the parent commit was HEAD before correction commit `073b65963e3ed8e3438bc34134f5a903fce995de`; exact size/hash identify the accepted artifact. Existing diagnostics do not prove the REMOTE-side reason for closing each otherwise functional session. Active MP3/A2DP/web-manager and physical latency regression remain unrun.

## Shared-contract impact
- CCM 1.0.0: NO CHANGE.
- TUNER Native API v1: NO CHANGE.
- Other device impact: REMOTE stays reachable but does not retain fresh authority through the repeated closures.
- Approval evidence: owner authorized this exact application-only installation and passive observation; no further correction or rollback was authorized.

## Blockers
The stability gate failed despite zero server timeout, partial/failed write, allocation failure or Wi-Fi disconnect. Intentional volume-performance testing remains blocked.

## PM decision required
Authorize a narrow peer-close lifecycle diagnosis or separately authorize application rollback. No automatic rollback is permitted.

## Recommended next task
Identify which REMOTE lifecycle transition closes each connection after successful snapshot exchanges and whether DISPLAY_IDLE/SYSTEM_SLEEP contributes. Use existing counters/source before adding instrumentation.

## Commit
- Firmware result commit(s): `073b65963e3ed8e3438bc34134f5a903fce995de`
- Device changelog: TUNER `CHANGELOG.md` at `073b65963e3ed8e3438bc34134f5a903fce995de`
- Coordination publication: branch `remote/a-remote-012-low-latency`, PR #18; final coordination hash reported after publication
- Previous handoff archive: `archive/tuner/2026-10-17T143224Z_A-REMOTE-012_CONNECTION-STABILITY-BUILD-READY.md`

## Hardware status
- Physical device tested: YES
- Board / hardware configuration: classic ESP32 TUNER, 4 MiB flash, unchanged 3 MiB application slot
- Procedure and result: candidate/readback/boot PASS; passive paired stability **FAIL**
- Firmware actually flashed: 2,037,152 bytes at `0x10000`, SHA-256 `19c39f4721ff43b939806f18aee599203225afde384c07934d58f1d0cc0398e8`
- Build-only or simulated checks: prior focused 54 checks/assertions and production build PASS retained; no rebuild in this operation
