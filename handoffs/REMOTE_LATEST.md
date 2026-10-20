# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-014-SOFTWARE-READY-20261020T190802Z
- Updated (UTC): 2026-10-20T19:08:02Z
- Task ID: A-REMOTE-014
- Status: HARDWARE VALIDATED / PASS
- Prepared by: A-REMOTE-014 implementation coordinator
- Coordination input commit: `5d36f06c301cdd340fe65084dca4d636ad6dc699`

## Milestone
Automatically locate the already-paired TUNER after DHCP address changes without editing persistent association data or weakening RTCP authority. Software scope achieved; hardware validation remains pending.

## Baseline
- Device repository: `https://github.com/OviOneKenoby/REMOTE-01`
- Branch: `remote/a-remote-014-mdns-discovery`, based on public `main` `d0a6ae556d8cbd9da5d90896b54573a45a48af69`; [REMOTE PR #3](https://github.com/OviOneKenoby/REMOTE-01/pull/3)
- Executable source: `9c805e5444587bc3d8952a57f44ec526c615e74a`
- Candidate: 2,568,992 bytes; SHA-256 `cdfccacdf07d0e4ca0a29b2c92f3cf29ee5e1b65df109ca730c3915185c82e2d`
- Production environment: `remote01`; static RAM 56,356 bytes; OTA headroom 577,056 bytes
- Contract references: CCM 1.1.0 frozen; RTCP/1 accepted binding; D-009 frozen and unchanged

## Changes
Added official ESP-IDF mDNS 1.14.0, a fixed static discovery worker, bounded DNS-SD filtering and candidate selection, authenticated runtime endpoint pinning, and lifecycle invalidation. Saved endpoint and pairing data remain unchanged.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Endpoint selection | Native focused test | Host C++ | PASS 10/10 | device branch |
| Discovery policy | Python source-policy test | Host | PASS 10/10 | device branch |
| Network status | Existing focused regression | Host C++ | PASS 15 checks / 142 assertions | device branch |
| RTCP association/wire | Existing host regression with `RTCP_HOST_TEST` | Host C++ | PASS 11/11 | device branch |
| Lifecycle policy | Existing source-policy test | Host | PASS 13/13 | device branch |
| Production build | clean `pio run -e remote01` | pinned PlatformIO / ESP-IDF 5.5.3 | PASS | artifact identity above |

## Remaining unknowns
Physical mDNS behavior, DHCP recovery, multiple advertisers, multicast loss, sleep/wake, coexistence, and runtime mDNS heap/task watermarks are not measured. A multicast-blocked network cannot recover a stale saved endpoint.

## Shared-contract impact
- CCM 1.1.0: NO CHANGE
- RTCP/1 and D-009 wire semantics: NO CHANGE
- TUNER Native API v1: NO CHANGE; remains unapproved/unimplemented
- Other device impact: requires matching TUNER `_rtcp._tcp` advertisement branch

## Blockers
No software blocker. Hardware acceptance and branch integration remain pending. TUNER branch is stacked on open D-009 PR #7.

## PM decision required
Authorize the controlled TUNER-first application-only hardware protocol after reviewing all three A-REMOTE-014 PRs.

## Recommended next task
Execute only `protocols/A-REMOTE-014_HARDWARE_VALIDATION.md` after explicit owner authorization; stop before any flash until then.

## Commit
- Firmware result commits: `02a3f4d10056ce1731d512b1f816db0777cb67a7`, `9c805e5444587bc3d8952a57f44ec526c615e74a`
- Device documentation commit: `d32945b020a983a1cfaf89ff52e458a888fb382b`
- Previous handoff archive: `archive/remote/2026-10-20T190802Z_A-REMOTE-014_REMOTE-PUBLIC-BASELINE-AUDIT-CORRECTION-20261019T201708Z.md`

## Hardware status
- Physical device tested: YES — ESP32-S3 (v0.2, 16 MiB flash, 8 MiB PSRAM) on COM3
- Pre-flash rollback verification: VERIFIED / PASS — 2,526,848 bytes read back before flash; SHA-256 matched `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da` exactly against known rollback image
- Firmware flashed: YES — REMOTE 2,568,992 bytes written at offset `0x10000` (`factory` partition)
- Readback verification: VERIFIED / PASS — 2,568,992 bytes read back; SHA-256 matches `cdfccacdf07d0e4ca0a29b2c92f3cf29ee5e1b65df109ca730c3915185c82e2d` exactly
- Integration & Recovery: VERIFIED / PASS — automatic recovery across DHCP change (`192.168.1.152` -> `192.168.1.31`), encoder volume control, display UI, MP3 status (`Playing`), power loss reconnect
- Overall status: HARDWARE VALIDATED / PASS
