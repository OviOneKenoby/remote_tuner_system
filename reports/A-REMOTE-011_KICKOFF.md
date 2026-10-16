# A-REMOTE-011 kickoff: minimum common API integration

## Verdict

Kickoff inspection is complete. No common REMOTE-TUNER wire API exists in either firmware. CCM 1.1.0 supplies the required logical semantics, but it deliberately does not define a wire format, endpoint, port, transport, discovery method, pairing mechanism or authorization mechanism. The existing `TUNER_NATIVE_API_V1.md` is a design candidate and explicitly leaves framing/transport and security OPEN. An executable network endpoint must therefore wait for an owner-approved secure binding; inventing one during implementation would change the shared contract boundary.

The smallest useful first end-to-end milestone is a single authorized REMOTE controlling one TUNER target with:

1. version/identity negotiation, session generation and capability revision;
2. a bounded capability snapshot;
3. verified fresh observations for `volume.level` and `playback.state`;
4. one executable operation, `volume.set`, with closed arguments, correlated result, deadline, deduplication and no automatic retry;
5. disconnect/reconnect resynchronization that invalidates the old session; and
6. persistence only for the minimum association/session/dedup state required by CCM 1.1.0, using the validated private `remote_ctl` backend.

Playback commands and station/catalog operations are excluded from the first milestone. Their current TUNER semantics do not yet satisfy the CCM evidence requirements: radio pause is implemented as mute while the live stream continues, Bluetooth exposes a toggle, and station entries do not yet have the stable opaque identities/generations required by CCM catalogs.

## Applicable CCM 1.1.0 capabilities

The following frozen capabilities apply directly to this first slice:

- `CommonDevice`, `Target` and `Binding`, including device/association generations, `capability_revision`, `mapping_revision`, `session_generation`, authorization and reachability.
- Explicit `CapabilityDescriptor` records. Missing descriptors mean UNKNOWN. SUPPORTED/READY requires current identity, authorization, mapping and operation/field evidence.
- `volume.set {level: Normalized}` as a context-independent, context-dependent-idempotence operation. The adapter must reject out-of-range input before dispatch and report the actual representable level; normalized volume does not claim dB or loudness semantics.
- `volume.level` as an independently observed normalized value with declared precision.
- `playback.state` as a read-only field with exact PLAYING/PAUSED/NOT_PLAYING/BUFFERING mapping and matching media-context generation. Command success cannot manufacture it.
- `StateObservation` provenance, association/mapping/session generations, acquisition order or verified source sequence, explicit freshness and reconnect RESYNC.
- Request capture/admission/dispatch, lifecycle and correlated results. Deadlines are checked before send; completion does not imply an observed field change.
- Automatic retry disabled. Deduplication, ordering, old-session rejection and non-reuse of durable request/generation identity apply.
- CCM 1.1.0 section 12.1 G1a: ordinary interruption/corruption must preserve fail-closed, no-replay, barrier and non-reuse behavior. Deliberate coherent full-domain restoration remains outside the V1 threat model under the approved G1b boundary.

CCM operations that exist in the model but are not ready for this milestone include `volume.step`, `volume.mute`, playback operations, catalog enumeration and content/station selection. A method name in local firmware is not proof of CCM support.

## What already exists

### TUNER v1.1.11

- `AudioPlayer` owns radio and Bluetooth audio behavior and exposes local `setVolume()`, `getVolume()`, playback state and now-playing accessors.
- The main loop already serializes local buttons, UI updates, web servicing and audio-loop work on the Arduino execution path.
- `StationManager` provides bounded station/favorite/recent storage, but no CCM catalog identity/generation contract.
- `WiFiManager` supplies network state and existing connectivity behavior.
- `WebPortal` provides configuration/status routes (`/api/status`, `/api/diagnostics`, `/api/stations`, Wi-Fi and timezone operations). These are not the common control API and are not authorized control transport.
- ArduinoJson is already pinned. `ObservedWebServer` and bounded response writers are reusable patterns for bounded parsing/telemetry, subject to a separate secure transport decision.
- The v1.1.11 PSRAM build reports 85,936 bytes static RAM and 2,022,097 bytes linked flash in a 3,145,728-byte app slot. The firmware binary is 2,028,672 bytes, leaving 1,117,056 bytes by binary length and 1,123,631 bytes by the linked-flash metric. Runtime internal-heap pressure remains material because Wi-Fi, Bluetooth and TLS have historically competed for internal memory.

### REMOTE

- The protocol-neutral CCM Core already models capabilities, fields, observations, request capture, lifecycle, ordering, freshness, conflict handling and no-replay behavior.
- `control_home` provides a bounded eight-intent UI boundary, session/capability gating, fixed 3-second command deadlines and safe sleep/wake invalidation. It currently runs only against a development mock adapter.
- `network_manager` provides Wi-Fi provisioning, captive portal operation, reconnect state and sleep recovery. No outgoing common-API client or verified control transport exists.
- The A-010 private source copy contains the validated `remote_persistence` schema-v1 backend for the dedicated `remote_ctl` NVS partition. It supports generation fencing, CRC records, an authority root, three slots, one authoritative payload up to 4,096 bytes, fail-closed ambiguity handling and no generation reuse.
- The A-010 production-backend build was 2,496,400 bytes in each 3 MiB OTA slot, leaving 649,328 bytes. The diagnostic build was 2,503,936 bytes, leaving 641,792 bytes.

## Missing work

- No approved transport, framing, endpoint, port, discovery, pairing or authorization binding exists.
- TUNER lacks a bounded Native/common-API request parser, authenticated session, deduplication store, serialized command owner, capability publisher, state sequence and correlated result publisher.
- REMOTE lacks a network client adapter that converts wire records into CCM Core events and dispatches captured requests.
- Exact identity/association bootstrap and credential lifecycle are undefined.
- TUNER `setVolume()` currently clamps rather than reporting invalid input; the API boundary must validate the closed CCM domain before calling it.
- Playback semantics differ by source. Radio pause is mute-like, Bluetooth play/pause is a toggle, and a safe cross-mode CCM mapping is not verified.
- Station/favorite records lack stable selection references, catalog generation/revision and verified enumeration semantics.
- The named current REMOTE workspace has the earlier six-entry `partitions.csv` and no `remote_persistence` component. The preserved A-010 private source has the installed seven-entry layout and backend. Implementation must start by selecting/reconciling that preserved A-010 source state without publishing it.

## Proposed implementation files after owner approval

No listed file is changed by this kickoff.

### TUNER repository

- Add `src/common_api.h` and `src/common_api.cpp`: bounded neutral records, identity/capability/state snapshots, request validation, deduplication and correlated results.
- Add `src/common_api_transport.h` and `src/common_api_transport.cpp` only after the secure transport binding is approved.
- Modify `src/main.cpp`: drain a bounded API request queue on the existing owner loop and publish coherent state snapshots; preserve all current button/UI/web/audio calls.
- Modify `src/audio.h` and `src/audio.cpp` only for a side-effect-free coherent snapshot or exact result access that cannot be obtained safely through existing accessors. Codec, stream, A2DP and AAC paths remain untouched.
- Modify `platformio.ini` only if the approved secure transport requires a pinned dependency or build option. ArduinoJson is already present.
- Do not change `src/stations.*` or expose station/catalog operations in milestone 1.

### Private REMOTE repository

- Start from/reconcile the preserved A-010 source, including `partitions.csv` and `components/remote_persistence/**`.
- Add `components/tuner_native_client/CMakeLists.txt`, bounded public headers and implementation for the approved transport, framing, session and adapter-to-Core translation.
- Modify `components/control_home/runtime.cpp` to select the real adapter in the production profile while retaining the development mock as an explicit development-only path.
- Modify `components/control_home/CMakeLists.txt` for the new client and persistence dependencies.
- Extend `components/remote_persistence/**` only with a versioned bounded A-011 envelope for association/session/dedup state; preserve the A-010 ordering and failure behavior.
- Modify `components/network_manager/**` only to expose copied connectivity/lifecycle events needed by the client. Provisioning credentials, captive portal behavior and default NVS remain untouched.
- Modify `main/CMakeLists.txt` or top-level build settings only where component registration requires it.

## Resource risks and acceptance measurements

- TUNER flash headroom appears sufficient for a small bounded API, but a secure stack can add a meaningful code footprint. The exact delta must be measured in the v1.1.11 `esp32-lwip-psram` profile.
- TUNER internal RAM is the principal risk. Static RAM is currently 85,936/327,680 bytes, but linked totals do not capture runtime TLS/socket buffers, request documents, task stacks or Wi-Fi/Bluetooth coexistence. The implementation must use fixed bounds, one in-flight request initially, no unbounded `String` growth, and no new long-lived task unless measured.
- REMOTE has 649,328 bytes of OTA headroom in the accepted production-backend build. ESP-TLS/client buffers and Core adapter state still require clean-build and runtime heap/stack measurements across Wi-Fi connect, sleep/wake and reconnect.
- The persistence payload limit is 4,096 bytes, but the first slice should store only compact identity/generation/dedup data. Capacity must be checked from encoded bytes and NVS entry counts, not assumed from the partition size.
- For both devices, acceptance should compare pre/post firmware size, static RAM, minimum free internal heap, largest internal block and task stack watermarks during the relevant Wi-Fi plus Bluetooth/web-manager modes.

## Genuine blockers and next owner decision

Two prerequisites block firmware implementation:

1. Approve a concrete secure transport/framing/authorization binding consistent with the existing Native design constraints. Plain unauthenticated LAN control is not approved by current material.
2. Confirm the preserved A-010 private source copy as the REMOTE implementation baseline, or authorize a controlled private reconciliation into the named workspace. The named workspace is not A-010-complete.

After those decisions, approve or revise milestone 1: identity/version/capability negotiation, fresh `volume.level` and `playback.state`, and `volume.set` only. No playback command, station/catalog, AAC, UI, MQTT or SmartThings work belongs in this slice.

## Verification performed

- Coordination main and task input: exact `8e93c702940d49583f3fdd58046503ae0b8f7354`.
- TUNER: clean detached public checkout at v1.1.11/main `5fb92c95d228d744d1182ae3956e850c5be2f277`; build manifest and relevant source read only.
- REMOTE: named private workspace and preserved A-010 source copy inspected read only; no secret values or private source published.
- Firmware builds, hardware access, flash operations and functional device tests: NOT RUN by design.
