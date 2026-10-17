# A-REMOTE-012 low-latency volume control - software validation and commissioning plan

## Verdict

**SOFTWARE PASS / HARDWARE PENDING.** Both production builds pass, the bounded REMOTE model meets the new targets under a controlled 30 ms simulated command/observation delay, and the owner-reported TUNER-local lag has a source-demonstrated scheduling cause with a bounded correction. No device was accessed or flashed. Audible and UI latency must be measured on the paired hardware before acceptance.

## Verified cause

The approximately ten-second 15-detent observation is consistent with a source-proven serialization chain:

1. REMOTE generated one absolute one-percent command from the last authoritative value.
2. The Channel retained one outstanding command and could not advance until the submitted target was observed.
3. Post-result acquisition could remain behind the periodic snapshot schedule.
4. TUNER's main loop serviced RTCP once per loop after the web manager and ended with a 10 ms delay.

TUNER's protocol decoder already accepts any exact canonical percentage from 0 through 100, and its command handler calls the existing audio setter directly. The wire protocol was not the limitation.

The TUNER-local encoder exposed a separate confirmed serialization path. Its ISR safely queued detents, but the main loop drained only one detent per turn and synchronously refreshed the e-paper volume overlay after every audio update. The next queued detent therefore waited behind panel I/O. This local display path is not called by RTCP commands, so it does not replace the REMOTE/RTCP finding; both paths required scheduling changes.

## Implemented architecture

### REMOTE private source

Changed private files:

- `components/control_home/include/control_home/api.hpp`
- `components/control_home/facade.cpp`
- `components/control_home/runtime.cpp`
- `components/rtcp_client/client.cpp`
- `components/user_app/user_app.cpp`
- `tests/control/volume_admission_tests.cpp`
- `tests/control/hardening_tests.cpp`
- `tests/control/ui_volume_binding_tests.py`

The Channel keeps a byte-sized desired target and coalesces undispatched detents into one absolute command. While one command is dispatched, further detents alter only the bounded successor. After authoritative confirmation of the first target, at most one successor is dispatched to the newest desired target. This preserves every admitted detent without a per-detent round trip or unbounded queue.

CCM capture and the volume observation precondition remain mandatory. Targets remain 0-100 and directionally valid from the fresh authoritative observation. Session and capability revisions remain fenced. Definite refusal cancels. Uncertain execution is retained without retry. Disconnect, sleep or scope change invalidates pending state. After a confirmed result, a fresh different volume is accepted as external authority and cancels the obsolete local successor rather than overwriting it.

TCP no-delay is enabled, command completion schedules an immediate snapshot request, and the control owner cadence is 5 ms. HOME displays a provisional `authoritative>desired` value at a 20 ms UI cadence while the indicator bar remains authoritative.

### TUNER public source

Candidate commit: [`5391beef5e7ba264362ea19f2fdd93202308fa55`](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/commit/5391beef5e7ba264362ea19f2fdd93202308fa55), branch `a-remote-012-low-latency`.

Changed files:

- `src/main.cpp`
- `src/audio.cpp`
- `src/audio.h`
- `src/input.cpp`
- `src/input.h`
- `src/rtcp_server.cpp`
- `src/rtcp_server.h`
- `src/volume_target.h`
- `src/web_portal.cpp`
- `tests/test_ccm_wire.cpp`
- `tests/test_local_volume_latency_policy.py`
- `tests/test_local_volume_target.cpp`
- `tests/test_rtcp_latency_policy.py`
- `CHANGELOG.md`

Physical input is now handled before network/web work. In radio and Bluetooth volume contexts, the first event atomically drains the remaining signed detent total, clamps one absolute 5% target to 0-100, and invokes the existing audio setter once. Menu contexts retain one-event navigation. The synchronous e-paper overlay is deferred until 250 ms of encoder quiet, then renders the authoritative value once. Fixed diagnostics record local command/detent counts and last/maximum setter duration separately from deferred display state.

RTCP is serviced before and after the web-manager turn; the loop delay is 2 ms. Fixed counters record command count, last/maximum audio-apply time and last/maximum complete response time through existing read-only diagnostics. No key, nonce, identity or payload is recorded. The protocol, crypto, pairing store and audio backend semantics are unchanged.

## Verification

- REMOTE coalescing/lifecycle/performance: 8/8 PASS, 164 assertions.
- REMOTE UI distinction/cadence: 1/1 PASS, 11 assertions.
- Full REMOTE relevant regression: Core 69/69; profile 6/6; HOME 41/41; hardening 26/26; ingress 18/18; power 19/19; network 17/17; network-sleep 9/9; external-power 11/11; portal 15/15; diagnostics 9/9; physical input 19/19; both WoM modes 7/7; both stack modes 7/7; OTA preflight 8/8; remaining publication/boundary checks PASS.
- TUNER CCM absolute-volume handler: 16/16 PASS, including 0, 1, 50, 95 and 100 percent plus an inexact-rational rejection.
- TUNER latency policy/source ownership: 1/1 PASS, 9 assertions.
- TUNER local absolute target/bounds: 10/10 PASS.
- TUNER local input/audio/display scheduling policy: 10/10 PASS.

The controlled host model uses 15 detents over 56 ms and a 30 ms command/observation delay. It reports first command at 0 ms, first simulated audible application at 30 ms, final authority 34 ms after the last detent, provisional UI refresh at 20 ms and three RTCP submissions. These are model results, not hardware claims.

## Production artifacts

| Device | Environment | Binary bytes | SHA-256 | Slot headroom | Static RAM | Linked flash |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| REMOTE | `remote01` | 2,525,168 | `afd8b426b37cdac5bfd32abf4ee9fbf70c91e3a28ebdf74ae482871572dcdef4` | 620,560 | 47,388 / 327,680 | 2,524,673 / 8,388,608 |
| TUNER | `esp32-lwip-psram` | 2,036,000 | `0680e8f2c6bfb8b1149ab1a8baec56fa80a7995d0401bf74463ff1f0d1143c1a` | 1,109,728 | 87,448 / 327,680 | 2,029,421 / 3,145,728 |

Against the accepted A-011 production baselines, REMOTE adds 1,232 binary bytes and 160 static-RAM bytes; TUNER adds 1,200 binary bytes and 40 static-RAM bytes. Candidate binaries and rollback images remain private.

## Rejected intermediate artifacts

The first TUNER candidate build preceded its source commit and therefore embedded the prior Git identifier. Its 2,035,536-byte binary, SHA-256 `71c40924a935fb098ba3718aeafc48c6531f5c2048b479e410076bf302b35d52`, is rejected. The RTCP-only candidate was rebuilt from committed source before the later local-encoder finding produced the final candidate.

The 2,035,536-byte RTCP-only candidate at commit `6bf53a22191f0ff387899fa9a57c805a55461a11`, SHA-256 `615e6fdbc7fd7b883bcee0e9cfa9ab0156e714d4a37757f84f4983407d8e954e`, remains valid historical build evidence but is superseded by the final candidate, which also addresses the TUNER-local encoder path.

A clean reproduction from the accepted A-011 TUNER source produced the expected 2,034,800-byte length and resource metrics but SHA-256 `7b36921cf0b313f63b9b53b4083685dfd7e78c72cd41f4f554bb302e04d6b6fb`; it is not treated as byte-identical rollback evidence. The original accepted rollback binary was then located in three existing private captures, each matching the recorded `49f249...9bbd4` hash, and an additional verified private copy was retained. This preserves exact rollback without making a reproducible-build claim.

## Security and compatibility

CCM strict validation, exact freshness, authenticated provenance, RTCP encryption/counters, request correlation, command preconditions and one-in-flight delivery are unchanged. No automatic retry was added. Memory remains fixed; a desired target replaces queued per-detent work.

- New REMOTE with new TUNER: supported and performance candidate.
- New REMOTE with old A-011 TUNER: protocol-compatible because the old handler already accepts absolute targets; it lacks the faster service cadence and timing counters.
- Old A-011 REMOTE with new TUNER: protocol-compatible; legacy one-step commands remain accepted and receive the faster TUNER service cadence.

Either update order fails safely and remains functional. Install TUNER first, verify ordinary audio/UI/web behavior, then install REMOTE to minimize time in the slower mixed pair.

## Reversible commissioning checklist

1. Reverify private candidate and rollback sizes/hashes and the existing full-flash backups. Identify one device at a time through ROM identity.
2. Install TUNER candidate only at `0x10000`, length `0x1F1120`; exact readback must match the candidate hash. Do not touch bootloader, partition table, OTA data, NVS or pairing.
3. Verify TUNER UI/settings, MP3, Bluetooth A2DP, Wi-Fi and web manager including Bluetooth coexistence. Confirm RTCP listener and record idle timing counters.
4. Install REMOTE candidate only at `0x10000`, length `0x2687F0`; exact readback must match the candidate hash. Preserve `remote_ctl`, default NVS, pairing and partitions.
5. Verify REMOTE UI/settings, voltage telemetry, sleep/wake and authenticated identity/capability/state synchronization.
6. Measure separately: detent-to-audible change, detent-to-provisional UI, command-to-authoritative UI and final authority after the last of 15 rapid detents. Record TUNER apply/response counters and REMOTE submission count.
7. Require under 100 ms first and continued audible response, under 50 ms provisional UI, no optimistic authority, and final target within 250 ms after the last detent. Confirm materially fewer than 15 submissions for a rapid 15-detent burst, one in flight and no residual pending state.
8. Exercise rapid reversal, minimum/maximum clamping, a local TUNER volume change, one disconnect/reconnect and one sleep/wake. Require correct final authority and no replay.
9. On boot/audio/UI/pairing/memory or timing failure, stop. Restore only the affected application at `0x10000`: REMOTE rollback length `0x268320`, or TUNER rollback length `0x1F0C70`; verify exact readback. Full-flash restoration remains a separately authorized recovery action.

No step above has been executed on hardware for A-REMOTE-012.
