# A-TUNER-001 — verified TUNER baseline and correctness/state foundation scope

Date (UTC): 2026-10-08T14:17:01Z  
Coordination execution input: `769c4dc1f50acebbf855b06d4bcf9cfc5eba7e16`  
Role: TUNER//01  
Result: READY FOR REVIEW; inspection complete, corrective implementation not authorized.

## Executive result

The live TUNER checkout was clean, on `main`, and exactly matched the assigned
baseline `371cdebce7ba2648ea71636d5bdb5d738b42e680`; firmware version is `1.1.0`.
All B01–B11 were rechecked against this source. B01–B07 and B09–B11 remain
source-confirmed open; B08 is partially corrected because metadata snapshots
and decoder lifetime are protected, but not all audio state readers/writers
share that protection. No previously fixed decoder/source lifetime, Recent
alias, Bluetooth codec, now-playing snapshot, Wi-Fi string termination or
finite HTTPS EOF-clamp defect is reopened.

No executable file, dependency, partition, contract or device state was
changed. No fresh build/upload/hardware test was run. A documentation-only
firmware changelog commit was published separately. Recommendations below are
candidate tasks, not implementation authorization or Native API approval.

## Baseline and evidence boundary

| Fact | Verified result | Evidence |
| --- | --- | --- |
| Checkout | clean `main`, matched `origin/main` at inspection start | `git status --short --branch`, [baseline evidence](../references/device_evidence/tuner/A-TUNER-001_BASELINE.md) |
| Source/version | `371cdebce7ba2648ea71636d5bdb5d738b42e680`, `1.1.0` | `git rev-parse HEAD`; `src/config.h:4` |
| Active build config | `esp32dev`, Arduino, `espressif32@7.0.1`, `huge_app.csv`, pinned libraries/commits and AAC patch | `platformio.ini` |
| Local installed tools | PlatformIO Core 6.2.0; resolved platform 7.0.1; Arduino package 3.20017.241212; Xtensa 8.4.0+2021r2-patch5 | package metadata and resolver output in baseline evidence |
| Existing artifacts | four 2026-09-27 artifacts hashed; not rebuilt and not linked to flashed hardware by this task | baseline evidence |
| Current hardware | not tested; flashed commit and live margins unknown | no upload/serial/device action authorized |

The task input named planning hash `dd63c07...`; work started from the later
published coordination head `769c4dc...`, which contains that assignment and
PM publication verification. Source citations below refer to the verified
firmware baseline.

## B01–B11 recheck

| ID | Disposition | Exact source / trigger | Consequence and future exposure | Smallest correction and required evidence |
| --- | --- | --- | --- | --- |
| B01 | OPEN | `src/web_portal.cpp:125-126` parses the complete DELETE suffix with `String::toInt()`, checks only `<0`, then narrows to `uint8_t`. Trigger `/api/station/not-a-number`, `/api/station/256`, equivalents for Favorite. | Nonnumeric text becomes 0 and 256 narrows to 0, so a malformed destructive request can delete item 0. Any Native/catalog mutation would inherit an unsafe boundary if copied. | Require a nonempty all-decimal suffix, reject overflow before conversion/narrowing, require index `< current count`, and later add a stale/revision guard. Deterministic tests: empty, signs, whitespace, suffix junk, 255/256/large, boundary valid index; assert no mutation on every rejection. |
| B02 | OPEN | `src/audio.cpp:232-250` says pause is mute while decoder runs; `audioTaskFunc()` at `399-404` calls `loop()` only when state is PLAYING. Trigger Pause on live radio, wait, Resume. | PAUSED halts decode while retaining the stream/chain, so the comment and exposed state are false; buffer/socket continuity and resume behavior are unverified. A remote `pause` cannot truthfully promise continuity. | First hardware-characterize MP3/AAC+/HTTP/HTTPS pauses of several durations. Then choose a reviewed semantic: continue decode muted, reconnect-on-resume, or explicitly unsupported pause. Report BUFFERING/failure truth. Test audio continuity, network loss during pause, stop during pause and repeated pause/resume. O13. |
| B03 | OPEN | `src/main.cpp:462-469` adds a currently playing discovered station to Favorites with hard-coded `STATION_CODEC_MP3`. Direct browse add uses the real codec at `582-600`. Trigger play discovered AAC whose URL lacks `.aac`, then Next/+Favorite. | `stationCodecForURL()` cannot recover AAC from an opaque URL; persisted Favorite may later select MP3 decoder and fail/crash. Future catalog activation must preserve codec as part of the item, not infer identity from URL. | Carry the copied current station codec/context into add-to-Favorite. Regression with opaque AAC URL, `.aac` AAC URL and MP3 URL through every add path, reboot/reload, then hardware playback. |
| B04 | OPEN | `src/stations.cpp:55-74` shifts array entries on delete and adjusts `currentStation` only when out of range; `main.cpp:475` uses modulo station count and `484` subtracts from count. Trigger delete an item before the selected/playing numeric position, or delete all saved stations while saved-radio navigation remains possible. | Numeric identity silently changes after shifts; UI `selectedStation`, manager `currentStation` and actual audio can diverge. Next can divide by zero; Prev underflows. URL/name duplicates make either field alone an inadequate durable identity. | Guard zero before traversal; define deletion effects on active context; introduce durable saved-item identity plus catalog revision in a separately approved design/migration. Tests: first/middle/current/last delete, all-delete then all controls, duplicates, reorder/reboot, concurrent stale activation. O07/O14. |
| B05 | OPEN | `src/net_manager.h:28-32` exposes cached state/IP; `connect()` updates it only at synchronous success. `wifiEventHandler()` at `src/net_manager.cpp:227-243` is not registered and does not mutate state; `updateStatus()` at `221-225` only updates RSSI and has no call site. Trigger link loss/DHCP change after initial connect. | `isConnected()`/IP and web status can remain CONNECTED/old IP while the ESP Wi-Fi stack is disconnected or reacquiring. Discovery/availability/reconnect state would be untruthful. | One network owner consumes registered events/current stack status, updates link/IP/incarnation atomically and publishes copied snapshots. Test AP loss, DHCP change, router reboot, reconnect failure/recovery and stale-address refusal. O02/O12. |
| B06 | OPEN | `src/audio.cpp:291-294` subtracts 5 from `uint8_t currentVolume` whenever value >0. Trigger set absolute volume 1–4 then Volume Down. | Unsigned underflow is passed to `setVolume`, whose upper clamp turns it into 100%. A remote absolute-volume prerequisite is unsafe. | Saturating arithmetic before narrowing; validate absolute inputs in their original type. Exhaustive 0–100 boundary/property tests and physical radio/BT volume regression, especially 0–6 and 95–100. |
| B07 | OPEN | `play()` at `src/audio.cpp:91-188` tears down the old chain, writes URL/codec, but sets source/state only after successful decoder begin. Several failures teardown/clear only part of state. Decoder end at `399-408` sets STOPPED and stops decoder but leaves source/URL/codec/allocated chain. | Failed replacement can leave stale PLAYING/source/codec or a STOPPED snapshot with a locator/chain that looks current. Historical locator is mixed with active validity; UI mode may disagree. | Centralize state transitions and idempotent teardown under the owner lock; publish explicit attempting/current/failed context and clear active validity on every exit. Inject open, buffer, AAC PSRAM, decoder-begin and midstream failures; assert state/source/URL/lifetime and successful recovery. O12/O13. |
| B08 | PARTIAL / OPEN | Decoder/source replacement and decode loop share `audioMutex`; now-playing and BT metadata use critical sections; `getDiagnostics()` locks. But `pause/resume/setVolume`, BT enable/disable state writes and inline getters in `src/audio.h:61,66-69` do not all share the same lock. | Snapshots can combine values from different transitions and mutable pointer getters can race with teardown. Existing metadata/lifetime fixes are valid and must remain. | Make one audio owner transition state and return value-owned immutable snapshots; callbacks enqueue facts or update narrowly owned fields. Remove Native/web use of mutable pointers. Stress interleaved local/web/callback/failure operations under sanitizable host models plus hardware soak. O12. |
| B09 | OPEN | `enableBluetooth()` at `src/audio.cpp:326-332` marks PLAYING immediately after starting discoverability, before a source connects. `bluetoothPlayPause()` at `509-520` toggles a local optimistic bool after emitting AVRCP; no observed remote playback callback closes the loop. | PLAYING and pause state can be fabricated from intent rather than observation. Connection is queried live, but playback is not. | Separate sink enabled, peer connected, audio streaming and last command emitted; expose observed state only where supported. Test no peer, connect/disconnect, phone rejects/delays, external phone controls and AVRCP next/previous. O08/O13. |
| B10 | OPEN | The finite EOF clamp is correctly `size-pos` at `src/AudioFileSourceICYSStream.cpp:100-109` and stays closed. However metadata loops at `164-173` and `222-231` repeat forever when `read()` returns 0. They run inside decoder `loop()` while `audioMutex` is held. Trigger a truncated/stalled ICY metadata block. | Audio task can hold the mutex indefinitely; stop, diagnostics and source changes can block behind it. | Add a monotonic deadline/no-progress budget and connection check, return a defined status and release ownership. Fake-stream tests for partial/zero/error/disconnect plus bounded stop/diagnostic latency; hardware malformed/stalled server test. |
| B11 | OPEN | `src/audio.cpp:74-82` ignores `xTaskCreatePinnedToCore` result. Station/Recent/Favorite saves (`src/stations.cpp:259-272,351-364,408-421`), Wi-Fi `EEPROM.commit()` (`src/net_manager.cpp:190-215`) and timezone `putString()` (`src/time_service.cpp:24-40`) ignore write/commit results while callers report success. | Initialization or persistent mutations can report success although no task/storage commit exists. Reboot truth and command results are not dependable. | Check begin/write/commit/task results, stage RAM mutation until persistence outcome is known or report explicit degraded/failed result, and define rollback/reload. Fault-injection for task allocation, namespace open, short/failed writes and commit, followed by reboot verification. O10/O16. |

## Priority and dependency-ordered correction proposals

1. **P0 mutation safety:** B01 strict parsing/range/no-mutation rejects; B04 zero-count traversal guards. These are small, deterministic and prevent destructive/wild arithmetic behavior.
2. **P0 bounded ownership:** B10 bounded metadata reads so stop/diagnostics cannot deadlock; preserve the existing decoder lifetime mutex fix.
3. **P1 truthful audio transition core:** B07 centralized play/failure/end/stop transitions and B08 one owner plus immutable snapshot. This is the prerequisite for any remote state contract.
4. **P1 validated values and persistence:** B06 saturating volume, B03 codec propagation, B11 checked task/storage outcomes. These support safe absolute volume and durable catalogs.
5. **P1 network truth:** B05 event-driven link/IP/reconnect snapshot before discovery/state synchronization.
6. **P2 semantics requiring hardware:** B02 radio pause choice and B09 observed-versus-emitted BT model. Do not advertise unsupported pause/BT state while this is unresolved.
7. **Later contract work:** durable catalog identity/revision and guarded activation for B04/O07/O14 only after owner review; no ID format is selected here.

Each group should be a separately reviewable firmware task with its own build
and targeted regression. Do not combine it with Native transport/server work or
a dependency upgrade.

## Proposed authoritative ownership/publication boundary

The smallest coherent architecture is a single TUNER control/state owner (an
existing main/control task or a dedicated serialized command owner, to be
chosen during implementation). Physical controls, current web handlers and a
future Native adapter submit validated value-owned intents; none directly
mutates station arrays or audio fields. Decoder, Wi-Fi and Bluetooth callbacks
submit bounded observations/failure events and never retain pointers into
mutable catalogs.

The owner serializes admission, current-context validation, catalog mutation,
persistence outcome and audio transition. It assigns monotonic local revisions
to published facts only after the outcome is known. Readers receive copied,
immutable snapshots containing independently truthful network, audio, media
context, volume and catalog revision/availability. Snapshot publication must
not take a lock that a decoder callback can hold indefinitely. Existing
`audioMutex` lifetime protection and metadata critical sections remain until a
tested replacement subsumes them.

This is an internal ownership proposal, not a Native wire schema. It does not
choose JSON/HTTP/WebSocket, request IDs, epochs, station IDs, auth or mDNS TXT.
A display mode, encoder cursor, requested action or emitted AVRCP command is
never substituted for observed current media state.

## Operation and catalog semantics actually present

- Radio `play()` synchronously tears down the previous chain, opens the URL,
  allocates the ring/decoder, calls decoder begin and then sets PLAYING. Here
  PLAYING means decoder start succeeded, not proven audible output.
- Radio Pause sets I2S gain to zero and PAUSED. Contrary to its comment, the
  audio task then stops calling the decoder. Resume restores gain/state without
  an explicit reconnect. Actual continuity is unknown.
- Stop locks, sets STOPPED, frees the radio chain and clears source/codec. A
  natural stream/decode end does not perform the same complete teardown.
- Saved-station Next/Previous wrap numeric indices and are unsafe at count 0.
  Discovered/Favorite/Recent playback uses the discovered path: Previous is
  unavailable and Next while playing means add Favorite.
- Recent is a five-item, URL-deduplicated MRU of discovered playback attempts;
  it is updated before play succeeds. Saved-station playback is not added.
- Saved stations (15), Favorites (10) and Recent (5) live in positional arrays.
  RadioBrowser returns at most 20 results and its UUID is not retained. URL is
  used as locator/dedup but is not a durable ID. Complete durable identity is
  therefore not currently feasible without data-model/migration work.
- Bluetooth state reports PLAYING when the sink starts and local pause is the
  last emitted toggle, not confirmed phone playback. Connection itself is
  queried live. Next/Previous are emissions only.
- UI mode and selected cursor are separate variables and are not authoritative
  audio/catalog state; returning to selection can leave playback active.

Implications: O07 needs durable ID and migration evidence; O08 must select only
verified BT capabilities; O12 needs coherent snapshots/revisions/freshness;
O13 must settle radio pause/stop and observed feedback; O14 must define source,
selection/traversal and Recent attempt-versus-success semantics.

## Resource and feasibility evidence

Measured here only from configuration/package metadata and pre-existing files:

- active target/config and exact pinned libraries/commits;
- historical `firmware.bin` 1,999,088 bytes and hashes of all existing output;
- historical map section sizes; static `.data + .bss` is 83,048 bytes for that
  artifact, but this is not a fresh linker summary;
- one active 3,145,728-byte application slot in `huge_app.csv`; OTA proposal is
  inactive;
- audio task configuration: stack 8,192 bytes, priority 5, Core 1;
- diagnostics code can report internal free/largest/min heap, PSRAM, Wi-Fi RSSI,
  audio state/URL/codec and audio-task high-water mark.

Unknown: physical flash size, flashed artifact, current clean-build size,
boot/runtime baseline, heap minima/largest allocation across features, PSRAM
high-water/failures, all task stack minima, socket/client limits, request/body
buffers, command/history memory, callback/stop latency, fragmentation plateau
and coexistence of MP3, AAC+/SBR, TLS requests and Bluetooth. No transport,
security or client limit can be selected from binary size alone.

Required future measurement matrix:

1. Clean pinned build: capture complete package lock/resolution, linker RAM/flash,
   hashes and partition table; then identify exact flashed hash/version.
2. Instrument boot/idle, portal, browse TLS, HTTP/HTTPS MP3, HTTPS AAC+, BT
   disconnected/connected/streaming and BT-to-radio transitions. Sample free,
   largest and minimum internal heap, free PSRAM and every task high-water mark.
3. Measure command admission-to-outcome, snapshot copy and worst-case stop/source
   switch during stalled reads; record socket counts and allocation failures.
4. Load/soak with candidate bounded clients/messages/history, slow/disconnected
   clients, malformed bodies and repeated reconnects; require memory plateau and
   uninterrupted audio/local controls.
5. Repeat on physical target with exact artifact for MP3/AAC+/TLS/BT combinations;
   test recovery after AP/router/TUNER restart and storage failure injection.

## Open-decision evidence and questions

| Decision | Evidence/feasibility question before closure |
| --- | --- |
| O01 transport/serialization | What framing and full-resync behavior fits measured sockets, heap/largest block and latency under AAC+/TLS? Compare bounded poll and push prototypes; no transport preferred here. |
| O02 synchronization | Which owner revision/incarnation and gap/full-resync rules survive link loss, restart and sleep without stale replay? Requires B05/B07/B08 first. |
| O03 device ID | Where is a random persistent non-name/non-IP identity created, verified, migrated and reset; how are collision/replacement tests run? |
| O04 mDNS | Exact service/TXT lengths, expiry and negotiation fields must be tested with multiple/stale candidates; advertisements cannot establish trust. |
| O05 association/auth | What deliberate approval, secret/grant storage, multi-controller revocation/recovery and execution-time authorization fit measured NVS/RAM? |
| O06 port/path | How does a Native binding coexist with unauthenticated port-80 legacy routes without creating a bypass? No path is selected. |
| O10 result retention | What bounded ledger size/expiry/reboot guarantee is affordable and truthful under failed persistence? B11 and interrupted-write evidence first. |
| O11 bounds | Choose clients, sockets, bodies, rates, queues and timeouts only after the measurement matrix, including slow-client backpressure. |
| O16 reset domains | Define which reset preserves/erases identity, grants, catalogs and result history; prove interrupted writes/migration and report failures. |
| O17 security/coexistence | Threat review must cover authorized reads/mutations, CSRF/replay/abuse, secret redaction, legacy portal bypass and revocation during execution. OTA trust remains separate/deferred. |

O07/O08/O12/O13/O14 are additionally constrained by the concrete semantics
above. O09/O15 can remain deferred. O01–O17 stay OPEN.

## Verification performed and limitations

Read-only inspection included Git identity/dirty state, source/config/version,
dependency/package metadata, partitions, existing artifacts/hashes/map sections,
task/reference/handoff validation and exact B01–B11 source paths. `pio pkg list`
resolved the pinned platform but its presentation failed with a cp1252 Unicode
encoding error; package metadata/directories supplied the remaining inventory.
No fresh build was required or run, so this is not a build failure.

Fresh build: NOT RUN by task boundary. Upload: NOT RUN. Physical hardware:
NOT RUN. Existing 2026-08/09 changelog claims remain historical evidence with
their original scope; they are not promoted to current acceptance.

## Recommended next tasks for PM review

1. **TUNER correctness guards:** B01, B04 zero-list traversal, B06 and B03;
   deterministic software tests plus clean build and targeted hardware regression.
2. **TUNER bounded audio/state owner:** B10 then B07/B08; fault injection,
   concurrency stress and MP3/AAC+/TLS/BT/local/web hardware regression.
3. **TUNER persistence/network truth:** B11 and B05; failure/reboot/AP/DHCP tests.
4. **TUNER semantics characterization:** B02/B09 physical evidence and owner
   decision proposal for O08/O13, without Native implementation.
5. After those reviews, a separate measured resource-profile task and a
   contract-design task for O01–O17. Native server/discovery/pairing remains
   unassigned until explicit owner approval/freeze.

## Contract and gate statement

CCM 1.0.0 remains OWNER APPROVED/FROZEN with no change. The final approved
artifact/original approval provenance remains missing from this coordination
checkout, so final conformance cannot be claimed. TUNER Native API v1 remains
UNAPPROVED/UNFROZEN/NOT IMPLEMENTED. No endpoint, schema, station-ID format,
transport, security profile or cross-device semantic was approved or changed.
The common gate remains OPEN / NOT PASSED.
