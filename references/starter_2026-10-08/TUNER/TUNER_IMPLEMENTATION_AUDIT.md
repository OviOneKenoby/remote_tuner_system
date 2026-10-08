# TUNER//01 implementation audit

2026-10-07. Documentation-only source audit; no build, upload, library change or firmware correction.

## Baseline and evidence rules

Repository: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio.
Remote default branch: `main`; audited HEAD/tag `v1.1.0`: **371cdebce7ba2648ea71636d5bdb5d738b42e680**. `src/config.h` declares `FIRMWARE_VERSION "1.1.0"`. Commit date: 2026-09-27. `origin/v1-stabilization` and peeled annotated `v1.0.0` both identify **c0e25a70af5f5e8f642ac1565d6184fd46fef5a4**. This commit is an ancestor of main, merged by `7a5f858`; no evidence makes the older branch authoritative over default main. Changes since stabilization are confined to CHANGELOG, README, config and input: encoder GPIO13, Gray-code decoding/four transitions per detent, version bump and documentation. Audio/network/station code is unchanged between these baselines.

Audit checkout: `C:/Users/RYZEN/Documents/TUNER01-audit`. Existing local checkout at `C:/Users/RYZEN/Documents/esp-internet-radio-git/ESP32-WROVER-Internet-radio` was behind main at `1663a06` with untracked user files; it was not changed. Fresh checkout was clean before documentation additions.

Classifications used here:

- **VERIFIED CURRENT IMPLEMENTATION**: directly present in this exact source. Does not assert a new physical test.
- **DESIGN REQUIREMENT**: requested future product/interface behavior, not current support.
- **UNKNOWN / REQUIRES IMPLEMENTATION**: missing implementation/evidence; no capability inferred.
- **BUG / DEFECT CONFIRMED FROM SOURCE**: a concrete failing branch/data flow, with prerequisites stated; not a newly reproduced hardware failure.

Evidence precedence: executable code/config over comments and old guides for current behavior. Existing hardware acceptance belongs to its recorded release and test scope. `CHANGELOG.md` records v1.0.0 owner regression across radio, AAC+, Bluetooth, metadata, Wi-Fi, display, catalogs and web; v1.1.0 records hardware encoder validation. This audit does not extend that acceptance to Native API or adversarial multi-client use.

## A. Ownership, execution and hardware

**VERIFIED CURRENT IMPLEMENTATION** (`src/main.cpp::setup/loop/handleInput`): Arduino setup initializes display, input, audio, stations/lists, Wi-Fi credentials and timezone, then connects saved/configured Wi-Fi or starts setup AP. `currentMode` owns the UI state machine: boot/setup, station select, radio, Bluetooth, error, browse stages, favorites, recent and idle clock. MODE_MENU is declared but has no active input handler. UI mode is not authoritative playback state: encoder-click returns to selection without stopping a radio stream.

`loop()` serially executes `webPortal.handle()`, time update, physical input, serial input, periodic UI (~1 s), idle clock and `delay(10)`. Web handlers therefore share the main application execution context with catalog/UI mutations today; there is no separate application network/UI task despite unused NETWORK_TASK_STACK/UI_TASK_STACK constants. Future worker/client code cannot assume that implicit serialization still holds.

`AudioPlayer::init()` creates one persistent **AudioTask**, pinned core 1, priority 5, configured stack 8192 bytes. `audioTaskFunc()` drives decoder under `audioMutex`; active branch yields one tick after >=10 ms, idle branch delays ~50 ms. Application source does not configure Arduino loop-task affinity/stack/priority; these are framework configuration, not an invented project value. Wi-Fi/Bluetooth library tasks and callbacks also exist; this audit does not claim their full resource inventory from application constants.

Decoder/source/buffer lifetime: `play`, `stop`, `enableBluetooth` and decode iteration use `audioMutex`. Network open/decoder calls happen synchronously under that mutex. `getDiagnostics()` also waits indefinitely on it. Pause/resume/volume and inline state getters are not protected by this mutex; `disableBluetooth` changes state without it. ICY text uses `nowPlayingMux` and copies into caller storage; Bluetooth title/artist use `bluetoothMetadataMux` but getter returns a shared member snapshot, not caller-owned immutable data. There is no unified command queue, revisioned media snapshot or acknowledged command lifecycle.

Physical path (`input.cpp/h`): Bounce2 polling, one last-event slot; multiple simultaneous events can overwrite each other. Encoder ISR observes both CHANGE pins, validates one-bit Gray transitions, accumulates four per detent and saturates pending steps; loop consumes one step per update. Play-button falling edge emits short action immediately; held >1500 ms emits long action later (not mutually exclusive short/long). Actual GPIOs: buttons 34/35/39; encoder 13/32/push14; EPD CS5/SCK18/MOSI23/reset19/DC21/busy4; PCM5102A BCK26/WS25/data33. Do not reuse these as REMOTE wiring.

Display (`display.cpp/h`): GxEPD2 SSD1681 200x200, rotation1, synchronous page-loop rendering; full refresh every 12 complete partial redraws, header/title ticker 1300 ms, volume overlay 2 s. Idle clock after 60 s stopped main-menu inactivity consumes first input to return; this is a UI clock, not MCU sleep. Screen sleep/wake helpers exist but are not called by the current loop. Placeholder updateStatus/updateNowPlaying methods do not implement a state API.

## B. Audio and control semantics

**VERIFIED CURRENT IMPLEMENTATION**, `audio.cpp/h`, `main.cpp::handlePlayingInput/handleBluetoothInput/playStation/playDiscoveredStation`:

| Capability | Actual behavior and limit |
|---|---|
| Play | `play(url, codec)` synchronously tears down old stream, opens HTTP or vendored HTTPS/ICY, allocates buffer/decoder and sets PLAYING on decoder begin. No external command route. PLAYING is local decoder-start state, not proof of audible output. |
| MP3/AAC | Helix MP3a or AAC. AAC reserves 128 KiB PSRAM, fails if unavailable; ring buffer 16 KiB PSRAM with internal fallback. No OGG/FLAC/WMA decoder selected; no HLS/PLS/M3U playlist parser. |
| Pause/resume | Radio pause sets gain0 and PAUSED; resume restores gain. Decode loop only runs in PLAYING, contrary to the comment claiming decoding continues while muted. No timeshift guarantee. |
| Stop | Internal `stop()` frees stream chain, sets NONE/STOPPED/NONE codec. Browse entry calls it. No explicit web stop command. |
| Next/previous | Saved-list playback wraps by current numeric position. Discovered playback: Next adds favorite, Previous logs unavailable. Bluetooth sends AVRCP next/previous. These input gestures are not uniform playback.next/previous operations. |
| Volume | 0..100 nominal absolute setter, default80; steps +/-5; Bluetooth maps to0..127, radio gain0..1. Not persisted; underflow defect below. |
| Source/state/codec/URL | Internal getters; diagnostic snapshot exposes source/state/codec/URL. BUFFERING enum exists but play doesn't assign it; UI temporarily shows Buffering independently. Stream-end sets STOPPED without clearing source/codec/URL or freeing chain. |
| Station | UI `nowPlayingName` and manager index are separate. Discovered play copies name/URL before Recent mutation (old alias bug fixed). No unified current station ID/name snapshot exported. |
| ICY | StreamTitle parsed, protected copied text256; empty titles ignored, Live stream fallback, KIIS machine suffix simplified. No artwork extraction/download. |
| Bluetooth | Classic A2DP sink `ESP32-Radio`; live connection getter and peer name, AVRCP title/artist, local optimistic play/pause toggle. Enabling marks PLAYING before a phone connects. No remote playback-status acknowledgement or local BLE control service. |

Bluetooth library pairing with a phone is not REMOTE/TUNER LAN association.

## C. Catalogs and persistence

**VERIFIED CURRENT IMPLEMENTATION**, `stations.cpp/h`, `browser.cpp/h`, `main.cpp`:

| Domain | Capacity / ordering / duplicates / storage |
|---|---|
| Saved | 15; append, delete shifts array; duplicates allowed. Preferences namespace `stations`, count plus `n{index}`, `u{index}`, `c{index}`. Defaults are #if0, not boot presets. |
| Favorites | 10; append/remove shift; exact case-sensitive URL duplicate rejection. Separate `favorites` namespace, same key pattern. Physical UI adds/removes; web deletes only. |
| Recent | 5; exact URL match moved to front, oldest evicted. Separate `recent` namespace. Added before discovered playback success; saved `playStation()` does not add Recent. Thus this is discovered-attempt MRU, not all successful playback history. |
| Directory results | Up to20, country250, top tags40; lazy arrays discarded on browse exit/playback. Server popularity ordering (`clickcount` descending), client optional name-first-character filter. Only MP3/AAC retained. `stationuuid` not requested/stored. No durable result IDs. |

RadioStation is name64/URL256/codec enum. URL `.aac` substring heuristic overrides saved codec in load/list helpers; it is not content sniffing. Names/URLs are truncated on internal insertion; web enforces length bounds. Search reads `url_resolved`; URL is a locator/dedup key, not a demonstrated durable station identity. All indices can change on deletion/MRU; no generation or selection token exists. CurrentStation only represents saved list, not current discovered media. No revisioned atomic catalog export.

Wi-Fi (`net_manager.cpp`): EEPROM API 512-byte blob, SSID bytes0..31/password32..95/additive checksum96. In installed matching Arduino2.0.17 EEPROM.cpp this is NVS-backed emulation, not separate EEPROM hardware; no encryption configured by project. Connection success calls saveConfig. Timezone uses Preferences `time`/`tz`64. Catalog saves write count and indexed fields immediately, without transaction/schema-version/return-value checking or cleanup of stale keys beyond count. Current source offers no factory-reset/credential-reset operation. Station/favorite NVS persistence is implemented, not a guarantee of crash-atomic writes or stable IDs.

Directory HTTPS: five configured mirrors, sequential fallback for connection/non200 failures; 20 s connect/read settings per request, synchronous main-loop call. StreamString reserves24576 bytes then JSON filtered parsing; reserve is not a hard response-size ceiling. Audio is stopped before browser fetch; TLS released and browse arrays freed before discovered playback. This is station-directory lookup, not device discovery.

## D. Complete current HTTP surface

**VERIFIED CURRENT IMPLEMENTATION**, all in `src/web_portal.cpp::registerRoutes` and fallback handler. Synchronous WebServer on port80, both normal STA and setup AP; **every route has no application authentication or authorization**. Request forms are `server.arg` values (browser sends URL-encoded forms), not an implemented JSON command contract. No body-size/client/resource policy is specified by this application.

| Method/path | Class | Request -> handler | Response / errors |
|---|---|---|---|
| GET `/` | Read-only | none -> handleRoot/send_P | 200 text/html management page |
| GET `/api/status` | Read-only | none -> handleStatus/WiFiManager/TimeService | 200 JSON connected, ssid, ip, portal, timezone; cached Wi-Fi state caveat below |
| GET `/api/diagnostics` | Read-only diagnostic | none -> handleDiagnostics/AudioPlayer::getDiagnostics/SystemInfo/heap APIs | 200 JSON firmware_version, build_git_id, uptime_ms, reset_reason, free_internal_heap, largest_internal_heap_block, minimum_free_internal_heap, total_psram, free_psram, wifi_rssi_dbm (null disconnected), audio_source, playback_state, codec, stream_url, audio_task_stack_high_water_mark; unavailable fallback if audio mutex absent |
| GET `/api/stations` | Read-only | none -> handleStations/StationManager getters | 200 JSON stations/favorites arrays of name,url,codec (MP3/AAC); no Recent, IDs or revision |
| POST `/api/stations` | Persistent mutation | name,url,codec -> handleAddStation/addStation |201 {ok:true};400 invalid name/URL/length;409 full. Only exact lower-case aac selects AAC; all other codec input defaults MP3. |
| DELETE `/api/station/{suffix}` | Persistent mutation | path suffix -> handleDeleteStation/removeStation |200 {ok:true};404 invalid index. Actual parser accepts prefix plus arbitrary suffix, toInt then uint8 narrowing; strict integer validation absent. |
| DELETE `/api/favorite/{suffix}` | Persistent mutation | path suffix -> handleDeleteFavorite/removeFavorite |200 {ok:true};404 invalid index; same permissive parser |
| POST `/api/wifi` | Provisioning + persistent mutation | ssid,password -> handleWiFiSave/connect/saveConfig |200 {ok:true,connected:true};400 length/emptySSID;503 connection failure, credentials not saved. Up to20 s loop blocking; on success stops setupDNS/AP. Persistence return ignored. |
| POST `/api/timezone` | Persistent mutation | timezone -> handleTimezoneSave/setTimezone |200 {ok:true};400 invalid rule/storage begin failure; checks length/control chars/quotes/backslash, not full POSIX grammar |
| Other method/path | Fallback | onNotFound |302 empty text/plain Location http://192.168.4.1/ when setup active; otherwise404 JSON {error:"Not found"}. DELETE prefixes intercepted before redirect. |

JSON errors use `{error:message}`. No HTTP playback, volume, source selection, search, favorite-add, association, reboot, update or event route. No special captive-probe routes beyond generic fallback. Browser HTML safely inserts names via esc(); this is not CSRF/authentication protection.

## E-F. Discovery, identity and security

**VERIFIED CURRENT IMPLEMENTATION**: repository-wide source/config search finds no mDNS/SSDP/MQTT/WebSocket/HA/openHAB/Matter/BLE-control implementation. README MQTT/OTA checkboxes are TODOs. DNS wildcard port53 belongs to captive setup, not LAN device discovery. Existing external protocols: HTTP management/JSON, outbound HTTP(S) radio and Radio Browser, SNTP, Classic A2DP/AVRCP, serial input. No event/push state transport.

Identity: only explicit project hardware ID use is `ESP.getEfuseMac()` in `WebPortal::beginConfigPortal`: SSID prefix plus16 MAC bits, password `radio-` plus another16 bits. Device BT name is fixed across units; no stored application ID, hostname setter, Native identity/version endpoint or association registry. Firmware/build IDs identify software, not a device. Implicit framework MAC/hostname behavior is not an adopted Native ID. MAC fragments can collide; password derivation has only16 variable bits and is deterministic, not random-secret provisioning.

**VERIFIED CURRENT IMPLEMENTATION** security: no application auth/authz/CSRF/replay/nonce/rate-limit/Origin/Host/subnet validation. Normal HTTP relies on reachable LAN; setup AP has password protection but all APIs remain unauthenticated to joined/reachable clients. No saved Wi-Fi password returned by routes; SSID and station/current-stream URLs are exposed, so user-supplied credential-bearing stream URLs cannot be assumed sanitized. HTTPS clients use setInsecure: encrypted transport without certificate validation, no server-identity guarantee. No OTA receiver/writer/signature/trial/rollback code, no project secure-boot/NVS encryption setup. `WEB_SECURITY.md` proposes HMAC/nonces/signatures; that proposal is not implementation or automatically a frozen control protocol.

## G. Source-confirmed defects and external-control risks

All numbered rows: **BUG / DEFECT CONFIRMED FROM SOURCE**. No fixes applied.

| ID | Source and reproducible source-level trigger | Consequence |
|---|---|---|
| B01 | web_portal.cpp::handleDeleteStation/handleDeleteFavorite: `toInt()` on arbitrary suffix followed by `(uint8_t)idx`. A nonnumeric suffix yields0; 256 narrows to0. | Malformed DELETE can delete first persisted item. Numeric positions also have no stale-selection guard (architecture limitation). |
| B02 | audio.cpp::pause versus audioTaskFunc: PAUSED excluded from isDecoding. | Comment/documented running-decoder mute semantics are false; connection retained but not consumed by task. Resume may encounter old buffered data/disconnect; audible result requires hardware. |
| B03 | main.cpp::handlePlayingInput EVENT_NEXT discovered branch always passes STATION_CODEC_MP3 to addToFavorites. For AAC URL without `.aac`, URL helper cannot correct it. | New favorite saved with MP3 despite actual AAC; later wrong decoder chosen. Results/Recent direct favorite path correctly carries codec. |
| B04 | stations.cpp::removeStation shifts array, only resets currentStation when >=new count. Play B at index1 of [A,B,C], deleteA: index1 nowC while B can continue streaming. main selectedStation is separate and not repaired. | Wrong manager current identity, traversal changes; deleting all saved entries while still in saved radio mode then Next evaluates modulo0. |
| B05 | net_manager.cpp connect sets cached state/IP; wifiEventHandler is never registered; updateStatus never called and only updates RSSI anyway. | On later link loss cached connected/IP/RSSI can remain stale while raw WiFi.status diagnostics disagree. No application reconnect loop after boot. Driver auto-recovery is not verified by this source. |
| B06 | audio.cpp::volumeDown with absolute currentVolume1..4 computes negative promoted int then narrows to uint8; setVolume clamps wrapped value to100. | Decrease can jump to100. Reachable through public setter, though normal boot80 plus5-step controls do not produce1..4. Must regress before absolute-volume API. |
| B07 | audio.cpp::play tears down chain without first resetting state/source; open/allocation/begin failures return without setting STOPPED/NONE consistently. | Prior PLAYING/PAUSED/source can survive with no decoder; codec/URL may describe failed attempt. In contrast stream-end retains last URL deliberately but offers no history/current validity distinction. |
| B08 | audio.cpp pause/resume/setVolume and inline getState/getSource/getVolume do not use same lock as decode/state writes/getDiagnostics. | Existing task read/write synchronization is incomplete; locking only getDiagnostics cannot make snapshot authoritative when writers bypass it. Observable race occurrence not measured here. |
| B09 | audio.cpp::enableBluetooth sets PLAYING before connected; bluetoothPlayPause changes only optimistic boolean and sends AVRCP, no confirmed playback-state update. | Diagnostics cannot be treated as observed BT playing/paused state; toggle loses synchronization when phone changes state independently. |
| B10 | AudioFileSourceICYSStream.cpp::readInternal metadata while(mdSize) loops continue on read0 with delay1 but no deadline/disconnect check; called inside audioMutex. | A truncated/stalled metadata block can wait indefinitely, blocking diagnostics and stop/play behind same mutex. Source proves missing bound, not that a tested live server triggered it. |
| B11 | audio.cpp::init ignores xTaskCreatePinnedToCore result; stations save and net_manager::saveConfig ignore persistent-write/commit outcomes. | Audio init/config mutations can report success despite task/write failure; no correlated result or truthful persistence outcome. |

Additional **VERIFIED CURRENT IMPLEMENTATION** limitations (not invented hardware failures): getStation/getFavorite/getRecent return mutable array pointers, invalidated by shifts; getCurrentURL returns mutable storage; shared BT snapshot unsuitable for concurrent independent callers. Catalog cursors are not revalidated after web deletion before pointer/name display use. Serialization in one main loop prevents simultaneous web/physical writes today but does not repair stale indices or audio-task races. Recent records attempts from discovery before success, not all successful saved playback. Unsupported codec input silently coerced to MP3. New clients must not call arbitrary AudioPlayer methods from server callbacks or bypass owner state.

No proof of a new decoder-lifetime use-after-free: prior teardown race is covered by the shared mutex in current source. Previous Recent-pointer bug is fixed by local copy. Previous Bluetooth codec bug is fixed with SBC/NONE assignment. Do not present historical fixed bugs as still open.

## H-I. Standalone association readiness

**UNKNOWN / REQUIRES IMPLEMENTATION**: no REMOTE association, authorization record, persistent Native device identity, pairing UI, discovery advertisement, catalog/context generations, request/result correlation, reconnect reconciliation or multi-client command ownership. Required future work: discover candidate devices separately from deliberate association; persist stable identity and authorization independent of IP; rediscover after DHCP/reboot; distinguish multiple TUNERs; explicit unpair/replacement/revocation; immutable state and serialized mutations; bounded client resources and unknown-outcome handling. A BT phone connection or saved Wi-Fi SSID establishes none of these.

## J-K. Model compatibility and transport assessment

**DESIGN REQUIREMENT**: TUNER authoritative media endpoint -> REMOTE direct LAN client, optional HA/openHAB adapters and future clients. Neither automation hub is required for normal operation. REMOTE protocol-neutral Core remains unchanged.

Read-only cross-reference to REMOTE `docs/COMMON_CONTROL_MODEL_V1.md` (OWNER APPROVED/FROZEN1.0.0), `docs/TUNER_NATIVE_API_V1.md` (candidate UNAPPROVED/UNFROZEN plus canonical overlay) and `docs/REMOTE01_PRODUCT_DECISIONS.md`. Current decisions include mDNS discovery/manual fallback, TUNER-owned favorites/recent, REMOTE-owned artwork lookup/cache bound to active URL; exact wire transport remains design work. These documents were not changed and candidate endpoints are not evidence of this TUNER server.

Explicit mismatches: mode-dependent Next=add-favorite is not CCM playback.next; Bluetooth toggle cannot substitute explicit playback.play/pause; stopped local enum is not automatically CCM NOT_PLAYING truth; decoder begin/AVRCP request is not correlated physical execution acknowledgement; mutable indexes cannot be SelectionRef without verified identity/catalog/token context; mixed station/source/title snapshots lack media generations and may be stale. DEVICE_NATIVE favorites can map TUNER-owned catalog only after identity/guard evidence; REMOTE_RECIPE remains distinct and does not imply a REMOTE station database. URL artwork retrieval must discard obsolete context results and keep credential-bearing locators private. No frozen-model amendment or conformance claim.

| Transport | Current readiness | Future trade-offs, not frozen choice |
|---|---|---|
| HTTP request/response + JSON | WebServer/ArduinoJson already used | Small migration surface; define strict schemas, ownership, bounds/auth and correlated outcomes. Polling adds traffic/latency; waking REMOTE needs fresh snapshot, not blind replay. Current synchronous browse/audio locks can stall HTTP. |
| Bounded polling/versioned events | None beyond ordinary GET | Simpler socket lifecycle, reconnect-gap/full-refresh rules required; multi-client rate and memory budgets. |
| WebSocket/push | Not implemented | Lower update latency, but persistent clients, queues/backpressure, disconnect/epoch/gap handling and memory need design/testing. |
| MQTT | README TODO only | Optional HA/openHAB adapter friendliness; broker must never be mandatory for direct REMOTE; topics/auth/retained stale state/command correlation need definition. |
| mDNS | Not implemented; recovered product discovery direction | IP-change discovery, not trust/pairing or command transport. Service/TXT/port and ID format not selected here. |

HA/openHAB future mappings: media-player state/source/volume/transport, native favorites/catalog browsing, availability and metadata. Must map observed semantics accurately, advertise only verified actions, preserve device identity and handle concurrent physical/direct clients. No HA entity/discovery/binding/adapter files exist; cannot call this already compatible. Security, retries, causality, event/state revisions and resource bounds must be settled before API freeze.

## L. Resources and existing documentation conflicts

**VERIFIED CURRENT IMPLEMENTATION** platformio.ini: `esp32-dev`, espressif32@7.0.1, boardesp32dev, Arduino,240MHz CPU/80MHz flash/DIO, PSRAM flags, huge_app.csv. Libraries pinned GxEPD2 1.6.9/GFX1.12.6/BusIO1.17.4/Bounce2 2.72/ArduinoJson7.4.3/A2DP3245602afc494f9e62160a0cfb2af864af45a37f/ESP8266Audio058e131b26e459b9aadcb589a50f07877f1a09fd. Patch middleware applies AAC/SBR output buffer, invalid MP3 frame guard and HTTP ICY wait change; build_info embeds commit. No version upgrades performed.

COMPILATION_GUIDE records resolved Arduino package3.20017.241212+sha.dcc1105b (core2.0.17), GCC8.4.0 and PlatformIO6.1.19. Read-only installed platform7.0.1 manifest corroborates Arduino~3.20017.0; matching installed package SDK header identifies **ESP-IDF4.4.7**, not REMOTE IDF5.5.3 or old comments' Arduino3/IDF5. Matching cached pinned AudioOutputI2S uses legacy i2s_driver_install/uninstall, contradicting stale newer-driver comments. This is package inspection, not a new resolution/build.

Historical stabilization metrics only: BIN1,998,768; linkedflash1,992,189/3,145,728; staticRAM83,024/327,680. **Current main BIN/RAM/heap/stack values UNKNOWN: no current artifact or build measured.** Hardware flash capacity still unverified in provided TUNER records; boot logs ESP.getFlashChipSize but `/api/diagnostics` does NOT expose flash size despite OTA_READINESS suggesting it. PSRAM boot detection/logging exists; configured flags are not proof of capacity.

Installed matching huge_app.csv: NVS0x9000/0x5000; otadata0xe000/0x2000; single app0 subtypeota_0 at0x10000/0x300000; SPIFFS0x310000/0xe0000; coredump0x3f0000/0x10000. No app1; filesystem unused by application. Proposed CSV is inactive, slots2,031,616 each. Against HISTORICAL BIN headroom32,848 bytes (1.62%), not current build headroom. Historical CHANGELOG reports32,928; OTA_READINESS uses32,848 matching later BIN arithmetic. REMOTE accepted16MiB layout is not TUNER infrastructure.

Memory constraints: decoder task8KiB; ring16KiB, AAC block128KiB PSRAM; browse lazy arrays plus24KiB reserved response/String/JsonDocument/TLS allocations; Classic BT memory released with end(true) before return to browse/radio. Historical heap fragmentation/TLS pressure documented; no current quantitative coexistence/large-client benchmark. Allocation and blocking paths must be measured before adding API clients/push/security. Plain reserve is not an input bound. OTA blocked by physical flash evidence, slot headroom and unimplemented writer/trust/recovery; do not enable proposed partition as part of API work.

Other stale evidence to retain/correct separately: READ_THIS_FIRST says no dependency pins; QUICK_START GPIO16/17/36, default BBC presets, playlist links, BT click exits and factory-reset chord disagree with current source; no reset chord implemented. README radio Next guidance omits discovered add-favorite behavior. README performance/power estimates and old no-PSRAM/core3 comments are not measurements of this release. Historical entries remain intact; this audit supersedes their current-behavior interpretation only.

## Exact inspected files and limits

Complete tracked application/config/tools/document tree inventory at baseline follows. Source/header execution paths were traced; large historical CHANGELOG was inspected by sections/search against current source. No vendored dependency tree is tracked. No hardware, current test suite or firmware binary was produced. No automated test directory is tracked.

- `.gitattributes`
- `.gitignore`
- `CHANGELOG.md`
- `COMPILATION_GUIDE.md`
- `OTA_READINESS.md`
- `QUICK_START.md`
- `README.md`
- `READ_THIS_FIRST.md`
- `WEB_SECURITY.md`
- `partitions/ota_4mb_proposed.csv`
- `platformio.ini`
- `src/AudioFileSourceHTTPSStream.cpp`
- `src/AudioFileSourceHTTPSStream.h`
- `src/AudioFileSourceICYSStream.cpp`
- `src/AudioFileSourceICYSStream.h`
- `src/audio.cpp`
- `src/audio.h`
- `src/browser.cpp`
- `src/browser.h`
- `src/compat_fixes.h`
- `src/config.h`
- `src/display.cpp`
- `src/display.h`
- `src/input.cpp`
- `src/input.h`
- `src/main.cpp`
- `src/net_manager.cpp`
- `src/net_manager.h`
- `src/stations.cpp`
- `src/stations.h`
- `src/system_info.cpp`
- `src/system_info.h`
- `src/time_service.cpp`
- `src/time_service.h`
- `src/web_portal.cpp`
- `src/web_portal.h`
- `tools/build_info.py`
- `tools/patch_esp8266audio_aac.py`

Supplementary read-only evidence: matching cached pinned ESP8266Audio AudioOutput.h/AudioOutputI2S.cpp (commit verified); cached A2DP commit verified; installed platformespressif32@7.0.1/platform.json; framework-arduinoespressif32/package.json, SDKesp32/include/esp_common/include/esp_idf_version.h, tools/partitions/huge_app.csv and libraries/EEPROM/src/EEPROM.cpp. Remote HEAD/branches/tags and ancestry/diff inspected with git. REMOTE cross-reference files listed in sectionJ; no REMOTE file changed.

Scope closure: four audit/architecture/matrix/plan documents plus append-only CHANGELOG; documentation validation only. No runtime fix, Native API, pairing, discovery/integration implementation, config change, build, upload, commit or push. Next milestone is described in [implementation plan](TUNER_REMOTE_IMPLEMENTATION_PLAN.md).
