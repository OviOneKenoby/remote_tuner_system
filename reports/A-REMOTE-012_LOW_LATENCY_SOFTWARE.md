# A-REMOTE-012 low-latency volume control - software validation and commissioning plan

## Verdict

**HARDWARE INSTALLED / RTCP POST-IDENTITY SYNCHRONIZATION BLOCKED.** The pre-commissioning software and rollback verification remain valid, both candidate applications passed exact readback, and TUNER local audible response is fast. Paired REMOTE control acceptance cannot proceed because no first state snapshot becomes authoritative after capability acceptance. The exact server/transport boundary requires bounded TUNER diagnostics before a behavioral correction is justified.

## Post-installation diagnostic update

Both candidates were subsequently installed with exact application readback PASS. TUNER boots normally, and owner observation confirms fast local audible volume response while e-paper refresh remains slower. REMOTE and TUNER are reachable. REMOTE diagnostics demonstrate TCP establishment, mutual authentication, accepted identity and an accepted capability response: diagnostic stage `complete` is assigned only after the capability parser succeeds. The initial state snapshot does not become authoritative, leaving `volume.level` unknown and `volume.set` unavailable. Later automatic reconnect attempts have also ended after client hello with EOF. No intentional control command was sent.

The first proven failure boundary is therefore **after accepted capabilities and before successful admission of the first snapshot**. A source comparison against the working A-REMOTE-011 implementation found no A-REMOTE-012 change to RTCP record framing, cryptography, identity, capability or snapshot encoding. A-REMOTE-012 adds fixed timing counters and changes main-loop scheduling; TUNER static RAM increased by 40 bytes.

TUNER was observed with 2,304 bytes of free internal heap and a 948-byte largest block. This is serious resource pressure, but it is not proof of causation: identity and capability responses completed under the same firmware, no allocation-failure evidence is exposed by the current read-only web diagnostics, and no source-level allocation failure was observed. The server uses fixed 556-byte receive/transmit members and bounded 512-byte stack buffers. Current diagnostics do not identify whether the snapshot request reached TUNER, response construction or the single-call socket write failed, the session closed, or REMOTE received and rejected a snapshot.

The minimum safe next action is a separately authorized, bounded TUNER diagnostic correction before changing transport behavior: fixed counters/state for application request kind, snapshot dispatch, response construction, requested/written byte counts, close reason, and allocation-failure count delta with free/largest internal heap sampled only on failure. Expected persistent RAM impact is approximately 48-64 bytes with no dynamic allocation. Focused tests should cover identity/capability/snapshot progression, partial/failed response writes, timeout/EOF closure, counter saturation and secret-free serialization. If that evidence proves a partial socket write, the subsequent correction should use a bounded fixed-buffer transmit offset and existing deadline; if it proves allocation pressure, memory should be recovered from demonstrated owners rather than relaxing RTCP security or CCM admission.

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

The TUNER binary was built from public commit `5391beef5e7ba264362ea19f2fdd93202308fa55`; its embedded build identity contains `5391beef5e7b`. REMOTE is a private Git-less workspace, so it has no source commit identity. Its preserved candidate matches the current production build byte-for-byte, and a private final scoped manifest records the eight changed source files plus `platformio.ini` and `partitions.csv`. This supports scoped source-to-artifact traceability without claiming a nonexistent REMOTE Git commit or publishing private hashes.

## Final rollback review

The following private evidence was rehashed read-only on 2026-10-17:

| Device / role | Bytes | SHA-256 | Recovery status |
| --- | ---: | --- | --- |
| REMOTE A-011 application rollback | 2,523,936 | `38b43de02bf1ef69b85678f0a67451836cb0a24e3bf1876283933b3185ed4d5d` | Exact application rollback at `0x10000` |
| REMOTE Stage 1 full flash | 16,777,216 | `31fd537c4bf534b101e74ed582bf0aa909235686207da29ad61413f21688b43d` | Primary and local copy match; complete recovery remains separately authorized |
| TUNER accepted A-011 production application | 2,034,800 | `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4` | Exact post-pairing application rollback at `0x10000` |
| TUNER Stage 1 pre-A-011 installed capture | 2,034,800 | `4dc7347191a38a18fe76b1635b446a485443ac6d06406bb6f53d303cd105b88a` | Fresh device readback and full-flash slice; not claimed byte-identical to a historical release artifact |
| TUNER temporary A-011 diagnostic application | 2,036,400 | `f193863f6d2966cc0797b9bdd2144971fb7b4bfc5bb9b1b4c07ff4840cf4a21c` | Exact diagnostic-state rollback only; not the preferred production rollback |
| TUNER Stage 1 full flash | 4,194,304 | `4a980e0887fab052389c233429d9cdf398720e119f2b51141a4fcfb8aa5914f6` | Primary and local copy match; complete recovery remains separately authorized |

The coordination baseline identifies TUNER firmware v1.1.11; no evidence supports relabeling the Stage 1 capture as v1.1.0. The reconstructed 2,034,800-byte application with SHA-256 `7b36921cf0b313f63b9b53b4083685dfd7e78c72cd41f4f554bb302e04d6b6fb` remains rejected as an exact rollback image because its bytes differ.

Stage 1 previously copied all eight rollback-critical files to separate physical USB storage with expected sizes. That USB device is not attached during this review, so those external copies were not rehashed. Reconnecting the owner-controlled storage and verifying its retained files is a mandatory pre-write checkpoint; it does not invalidate the independently matching primary and local full-flash captures.

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

## Hardware acceptance procedure

1. Connect one device at a time. Verify ROM identity, physical flash size and installed partition table. Rehash the exact candidate and application rollback, verify the primary full-flash capture, and reconnect/verify the owner-controlled external backup before the first write.
2. Install TUNER first, application only at `0x10000`, length `0x1F1120`. Exact readback must match SHA-256 `0680e8f2c6bfb8b1149ab1a8baec56fa80a7995d0401bf74463ff1f0d1143c1a`. Do not touch bootloader, partition table, OTA data, NVS or pairing.
3. Confirm normal TUNER boot, settings, Wi-Fi, MP3 playback, Bluetooth A2DP and web manager including operation while Bluetooth is active. Confirm RTCP listener and bounded timing counters.
4. Measure the TUNER physical encoder separately: first and continued detent-to-audible latency, 15 rapid detents, direction reversal and 0/100 boundary clamping. Require first and continued audible response under 100 ms and the final 15-step target within 250 ms after the last detent.
5. Only after TUNER passes, install REMOTE application at `0x10000`, length `0x2687F0`. Exact readback must match SHA-256 `afd8b426b37cdac5bfd32abf4ee9fbf70c91e3a28ebdf74ae482871572dcdef4`. Preserve `remote_ctl`, default NVS, pairing and partitions.
6. Confirm normal REMOTE boot, UI/settings, voltage telemetry, sleep/wake and authenticated identity/capability/state synchronization.
7. Measure REMOTE detent-to-audible change, detent-to-provisional UI, command-to-authoritative UI and final authority after 15 rapid detents. Require under 100 ms first and continued audible response, under 50 ms provisional UI, and final target within 250 ms after the last detent. Confirm fewer than 15 RTCP submissions for a rapid burst, one in flight and no residual pending state.
8. Exercise rapid direction reversal and minimum/maximum boundaries. Confirm the provisional target reconciles to authoritative TUNER volume without stale replay, unsafe retry or command flooding.
9. Exercise one disconnect/reconnect and one REMOTE sleep/wake. Require resynchronization without replay. Recheck MP3 and Bluetooth A2DP audio plus the active web manager after paired operation.
10. On boot, audio, UI, pairing, memory or timing failure, stop. Restore only the affected application at `0x10000`: REMOTE length `0x268320` with SHA-256 `38b43de02bf1ef69b85678f0a67451836cb0a24e3bf1876283933b3185ed4d5d`, or TUNER length `0x1F0C70` with SHA-256 `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4`; verify exact readback. Full-flash restoration remains a separately authorized recovery operation.

No step above has been executed on hardware for A-REMOTE-012.
