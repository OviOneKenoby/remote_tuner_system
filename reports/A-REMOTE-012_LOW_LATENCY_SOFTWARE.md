# A-REMOTE-012 low-latency volume control - software validation and commissioning plan

## Verdict

**CONNECTION-STABILITY CORRECTION BUILT / HARDWARE VALIDATION REQUIRED.** Later installed diagnostics prove repeated successful authentication and snapshots together with deadline-driven disconnects during long TUNER application-loop turns. The smallest source correction services RTCP cooperatively during synchronous e-paper BUSY waits and preserves every protocol, security and ownership invariant. Build and focused regression evidence pass; the correction is not installed and physical stability remains unverified.

## RTCP connection-instability root cause and correction

Two later read-only TUNER captures changed the diagnosis from a permanent post-identity failure to persistent-connection instability. Counters rose from 20 to 104 accepted connections, 18 to 66 accepted client finishes, and 86 to 259 snapshot requests and completions. The later capture records 24 server idle timeouts and 79 peer EOFs, which together account for 103 of 104 accepted connections; one connection was current or otherwise not closed at capture time. No partial/failed response write, allocation failure, lwIP `nomem`, or TUNER Wi-Fi disconnect was observed. Free internal heap was 91,548 bytes with a 77,812-byte largest block. Authentication, identity, capability exchange, snapshots, and two volume commands all succeeded at least intermittently. Memory exhaustion and a permanently broken handshake are therefore rejected as causes by the available evidence.

The confirmed scheduling defect is that TUNER's single Arduino application loop owns RTCP polling and also performs synchronous e-paper refreshes. Its measured maximum turn was 5,983 ms. REMOTE closes an awaited response after the unchanged 3,000 ms deadline, while TUNER closes an idle record session after the unchanged 5,000 ms deadline. Thus a long loop turn can cause REMOTE to close first and TUNER subsequently to observe EOF, or cause TUNER to classify idle timeout before consuming an already buffered request. GxEPD2's selected panel driver performs a synchronous BUSY wait and exposes a cooperative callback specifically during that wait. The exact historical 5,983 ms sample was not phase-tagged, so it cannot be assigned to one named refresh call; the e-paper starvation path itself is source-proven and covers every panel BUSY wait. Browser/network operations may still cause deliberate reconnects during exceptional long operations.

TUNER commit [`073b65963e3ed8e3438bc34134f5a903fce995de`](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/commit/073b65963e3ed8e3438bc34134f5a903fce995de) applies the bounded correction:

- `src/display.h` and `src/display.cpp` expose the existing GxEPD2 BUSY callback without new storage.
- `src/main.cpp` registers one callback after Wi-Fi setup; while the panel is busy it calls the existing nonblocking RTCP poll on the same application owner and yields for 1 ms.
- `src/rtcp_server.cpp` reads available bytes before record-idle expiry and processes a complete buffered record at the boundary; incomplete input retains the original timeout.
- `tests/test_rtcp_display_service_policy.py` verifies owner-preserving callback registration, yielding, read-before-timeout ordering and unchanged handshake deadline.

No new task, queue, dynamic allocation, buffer, retry, timeout extension, framing, cryptography, pairing, CCM, audio or REMOTE behavior was added. Normal REMOTE SYSTEM_SLEEP still intentionally invalidates its session, so some reconnects around actual sleep/wake are expected. Existing counters do not tag each peer EOF with REMOTE sleep state; hardware validation must distinguish the expected lifecycle from residual awake-state churn. The occasional partial REMOTE HTTP status response occurs on separate REMOTE tasks and is not proven to share the TUNER main-loop cause.

Focused verification passed: new display-service policy 9/9; existing RTCP latency policy 10/10; local-volume scheduling policy 10/10; diagnostic integration/redaction policy 14/14; diagnostic state model 11/11. One `esp32-lwip-psram` production build passed. The private candidate is 2,037,152 bytes, SHA-256 `19c39f4721ff43b939806f18aee599203225afde384c07934d58f1d0cc0398e8`, with 1,108,576 bytes of the 3 MiB slot remaining. Linked flash is 2,030,581 bytes and static RAM remains 87,512 / 327,680 bytes, a measured 0-byte static-RAM increase over the diagnostic build. The private ELF is 29,789,148 bytes, SHA-256 `697c8ef0662842f7daebd0e3c5c98f675e97b2274f9bdd83cc8f606a6d456367`.

No device was accessed or flashed. Required hardware validation is an application-only TUNER installation with exact readback, followed by awake-state READY/snapshot stability across full and partial e-paper updates, one expected REMOTE sleep/wake invalidation and resynchronization, and MP3/A2DP/web-manager regression. The validated application/full-flash rollback evidence and pairing remain compatible and unchanged.

## Post-installation diagnostic update

Both candidates were subsequently installed with exact application readback PASS. TUNER boots normally, and owner observation confirms fast local audible volume response while e-paper refresh remains slower. REMOTE and TUNER are reachable. REMOTE diagnostics demonstrate TCP establishment, mutual authentication, accepted identity and an accepted capability response: diagnostic stage `complete` is assigned only after the capability parser succeeds. The initial state snapshot does not become authoritative, leaving `volume.level` unknown and `volume.set` unavailable. Later automatic reconnect attempts have also ended after client hello with EOF. No intentional control command was sent.

The first proven failure boundary is therefore **after accepted capabilities and before successful admission of the first snapshot**. A source comparison against the working A-REMOTE-011 implementation found no A-REMOTE-012 change to RTCP record framing, cryptography, identity, capability or snapshot encoding. A-REMOTE-012 adds fixed timing counters and changes main-loop scheduling; TUNER static RAM increased by 40 bytes.

TUNER was observed with 2,304 bytes of free internal heap and a 948-byte largest block. This is serious resource pressure, but it is not proof of causation: identity and capability responses completed under the same firmware, no allocation-failure evidence is exposed by the current read-only web diagnostics, and no source-level allocation failure was observed. The server uses fixed 556-byte receive/transmit members and bounded 512-byte stack buffers. Current diagnostics do not identify whether the snapshot request reached TUNER, response construction or the single-call socket write failed, the session closed, or REMOTE received and rejected a snapshot.

The minimum safe next action is a separately authorized, bounded TUNER diagnostic correction before changing transport behavior: fixed counters/state for application request kind, snapshot dispatch, response construction, requested/written byte counts, close reason, and allocation-failure count delta with free/largest internal heap sampled only on failure. Expected persistent RAM impact is approximately 48-64 bytes with no dynamic allocation. Focused tests should cover identity/capability/snapshot progression, partial/failed response writes, timeout/EOF closure, counter saturation and secret-free serialization. If that evidence proves a partial socket write, the subsequent correction should use a bounded fixed-buffer transmit offset and existing deadline; if it proves allocation pressure, memory should be recovered from demonstrated owners rather than relaxing RTCP security or CCM admission.

## Post-identity diagnostic candidate

The authorized TUNER-only diagnostic source change is complete at commit `fda5f1ad1e5ebb9e83238cdbaa3ad79564e40842`. A fixed 60-byte state object records only bounded enums, counters, requested/written response lengths, internal free/largest heap and allocation-failure count deltas. It retains no payload, key, nonce, proof, pairing identifier, address or device identity and performs no dynamic diagnostic allocation. The existing serial `x` snapshot prints one compact `rtcp_diag` line; the web diagnostics document was deliberately not enlarged under the observed heap pressure.

Instrumentation covers accepted connections, accepted client finish, received application request type, snapshot requests/completions, response build and exact socket-write byte count, partial/zero writes, timeout/EOF and validation close categories, heap at accept/request/close, and allocation failures occurring across the application-response write. Protocol framing, cryptography, counters, timeouts, connection policy, audio and volume behavior are unchanged.

Focused results:

- RTCP diagnostic state model: 11/11 PASS, including normal identity/capability/snapshot progression, partial write, zero write, allocation delta, timeout, EOF and saturation.
- Diagnostic integration/redaction policy: 14/14 PASS.
- Existing RTCP scheduling policy: 9/9 PASS.
- Existing CCM wire regression: 16/16 PASS.

One production build using `esp32-lwip-psram` and board `esp32dev` passed. The exact private firmware artifact is 2,036,992 bytes, SHA-256 `18d59b75cbf481b517b09fd274207e2271cdd42a0a146f56eafeca2e8a1196d3`; its application-slot headroom is 1,108,736 bytes. Static RAM is 87,512 / 327,680 bytes, an increase of 64 bytes over the installed A-REMOTE-012 candidate and 104 bytes over A-REMOTE-011. The private ELF SHA-256 is `c32bc7023b6ea91b1deee96e1a3b568d2813aa703cc9db9f41cc959bb55db2`; map SHA-256 is `ecba389e4b77e4a7ee3f2f1c8556de2aa23c5e33127bd901c1b3bc3814591281`.

### Minimal commissioning procedure

1. Separately authorize TUNER hardware access. Verify the physical TUNER, current installed A-REMOTE-012 application, retained exact rollback and candidate size/hash.
2. Write only the 2,036,992-byte (`0x1F1500`) TUNER application at `0x10000`; do not erase or write bootloader, partition table, OTA metadata, default NVS or pairing. Read back exactly that range and require the candidate SHA-256.
3. Boot normally with REMOTE powered. Send no control command and do not rotate either encoder. Allow only the existing automatic connection attempt.
4. Capture one existing read-only serial `x` snapshot after the attempt. Preserve the private full capture and publish only the compact diagnostic counters.
5. Interpret the first boundary once: no snapshot request means REMOTE did not deliver it; a request without completion plus partial/failed bytes identifies response transmission; a positive allocation delta identifies an observed allocation failure; a completed snapshot with REMOTE still unknown moves the boundary to REMOTE receipt/admission; timeout/EOF records the close category. Stop after the observation without reconnect loops or speculative correction.

No hardware operation was performed for this diagnostic candidate, and no root-cause fix is claimed.

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

At the time this checklist was published, none of its hardware steps had been executed. The later bounded diagnostic installation is recorded below.

## Post-identity diagnostic commissioning result

On 2026-10-17 the owner authorized the bounded TUNER diagnostic installation. The complete eight-file rollback set on separate physical USB storage and the matching local files were reverified against their recorded sizes and SHA-256 identities. ROM preflight identified the expected classic ESP32 TUNER revision with 4 MiB flash. The 2,036,992-byte diagnostic candidate fit the unchanged 3 MiB application slot.

Only the application range beginning at `0x10000` was written. Independent full-span readback matched SHA-256 `18d59b75cbf481b517b09fd274207e2271cdd42a0a146f56eafeca2e8a1196d3`. The normal application then reported build identity `fda5f1ad1e5e`, connected Wi-Fi, 110,412 bytes free internal heap, a 106,484-byte largest block, and zero allocation failures.

Exactly one existing read-only serial `x` snapshot was captured. Its RTCP diagnostic line reported stage/request/close zero, zero connections, zero client finishes, zero records, zero snapshot requests/completions, zero partial or failed writes, and zero timeout/EOF/allocation deltas. A single read-only request to the existing REMOTE diagnostic endpoint timed out. Thus the intended automatic RTCP exchange did not reach TUNER during this bounded observation. The first proven boundary for this run is before TUNER TCP acceptance; it provides no evidence for or against response construction, response writes or allocation failure in the post-identity snapshot path.

The minimum next action is a separately controlled observation with REMOTE first demonstrated online, followed by one natural automatic connection and one TUNER `x` snapshot. Do not loop reconnects, issue control commands or infer that the instrumentation fixed the original defect.
