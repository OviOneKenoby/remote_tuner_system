# TUNER//01 handoff

## Metadata
- Handoff ID: TUNER-A-REMOTE-014-SOFTWARE-READY-20261020T190802Z
- Updated (UTC): 2026-10-20T19:08:02Z
- Task ID: A-REMOTE-014
- Status: HARDWARE VALIDATED / PASS
- Prepared by: A-REMOTE-014 implementation coordinator
- Coordination input commit: `5d36f06c301cdd340fe65084dca4d636ad6dc699`

## Milestone
Advertise the existing authenticated RTCP listener through standard DNS-SD so paired REMOTE devices can recover after DHCP address changes. Software scope and hardware validation achieved.

## Baseline
- Device repository: `https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio`
- Branch: `tuner/a-remote-014-mdns-discovery`, stacked on D-009 head `79d247893095b9464583c3cfe0e612d7683871c9`; [TUNER PR #8](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/pull/8)
- Executable source: `63ff6770fe4f0d7a46cb547ddc8f14abaec7f0fc`; project build identity `63ff6770fe4f`
- Candidate: 2,069,152 bytes; SHA-256 `d2c89edd1e5aa25a01c7f88ce787ccdcfa2e708a89d6fb402d0326a519ec896e`
- Production environment: `esp32-lwip-psram`; static RAM 89,832 bytes; slot headroom 1,076,576 bytes
- Rollback: installed D-009 candidate and released v1.1.12 remain preserved

## Changes
Added bounded `ESPmDNS` `_rtcp._tcp` advertisement on port 46411, following Wi-Fi/listener availability with a five-second retry. No TXT data, pairing identifier, credential, key, or station metadata is advertised. PR #7 is unchanged.

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| Advertisement lifecycle | Native focused test | Host C++ | PASS 9/9 | device branch |
| Discovery policy | Python source-policy test | Host | PASS 6/6 | device branch |
| D-009 focused behavior | Existing tests | Host | PASS 23/23 | device branch |
| D-009 integration policy | Existing tests | Host | PASS 12/12 | device branch |
| Production build | `pio run -e esp32-lwip-psram` | pinned PlatformIO | PASS | artifact identity above |

## Remaining unknowns
Physical mDNS packet trace, forced second DHCP change, long-duration soak testing, A2DP regression, and exact runtime mDNS allocation/task watermarks are not measured.

## Shared-contract impact
- CCM 1.1.0: NO CHANGE
- RTCP/1 and D-009 wire semantics: NO CHANGE
- TUNER Native API v1: NO CHANGE; remains unapproved/unimplemented
- Other device impact: requires matching REMOTE discovery branch for automatic recovery

## Blockers
No software blocker. Hardware acceptance complete. This branch depends on open D-009 PR #7.

## PM decision required
Review pull request integration sequence.

## Recommended next task
Merge TUNER PR #7, TUNER PR #8, REMOTE PR #3, and coordination PR #23 / PR #24.

## Commit
- Firmware result commit: `63ff6770fe4f0d7a46cb547ddc8f14abaec7f0fc`
- Device documentation commit: `216f5a14d375652543d3f722141acbf526bee8c8`
- Previous handoff archive: `archive/tuner/2026-10-20T190802Z_A-REMOTE-014_TUNER-A-REMOTE-012-V1.1.12-RELEASED-2026-10-19T155925Z.md`

## Hardware status
- Physical device tested: YES — ESP32-WROVER (ESP32-D0WDQ6-V3 / 4 MiB flash) on COM5
- Firmware flashed: YES — TUNER 2,069,152 bytes written at offset `0x10000`; esptool write verified
- Readback verification: VERIFIED / PASS — 2,069,152 bytes read back at 115200 baud on COM5; SHA-256 matches `d2c89edd1e5aa25a01c7f88ce787ccdcfa2e708a89d6fb402d0326a519ec896e` exactly
- DNS-SD mDNS advertisement: VERIFIED / PASS — PTR `_rtcp._tcp.local` -> `tuner-641d44._rtcp._tcp.local`, SRV `tuner-641d44.local:46411`, A `tuner-641d44.local` -> `192.168.1.31`
- Audio & HTTP: PASS — MP3 playback through headphones & HTTP 200 OK
- Overall status: HARDWARE VALIDATED / PASS
