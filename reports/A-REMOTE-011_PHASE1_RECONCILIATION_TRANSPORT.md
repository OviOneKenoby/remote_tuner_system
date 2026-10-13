# A-REMOTE-011 Phase 1: REMOTE reconciliation and secure transport decision

## Decision summary

Phase 1 is complete as a read-only design decision. Neither private REMOTE tree was changed, TUNER was not changed, and no hardware was accessed.

The active REMOTE workspace should be reconciled in a disposable private copy from the preserved A-010 source, then promoted only after inventory, host-test and clean-build checks. The comparison is small: after excluding build output, Git metadata and the already excluded credential-bearing component from content inspection, 1,695 files are byte-identical. The preserved A-010 tree contains 11 additional files and six changed files; the active tree contains no unique file.

For the first common-API slice, the recommended transport is a **single persistent TCP connection with a bounded pre-shared-key AES-GCM record layer**, using the mbedTLS AES-GCM and HMAC-SHA-256 primitives already present in both pinned frameworks. CCM 1.1.0 remains the semantic authority. The record layer supplies confidentiality, integrity and mutual proof of the provisioned pair key; CCM supplies identity, generations, request/result, freshness, ordering, deduplication and fail-closed rules.

WebSocket over TLS is rejected for the first slice on the current TUNER baseline. It is framework-compatible in principle, but Espressif documents approximately 40 KiB RAM per HTTPS socket plus server task stack, while the accepted TUNER evidence observed only about 5–10 KiB free internal heap and minimum largest blocks near 1 KiB during Wi-Fi, Bluetooth A2DP and web-manager activity. Adding TLS server state would create a concrete regression risk to the behaviors the owner requires us to preserve.

## 1. Exact private REMOTE reconciliation

### Compared inputs

- Active owner workspace: the owner-named private REMOTE source.
- Accepted source: the preserved A-010 private source used for the validated backend and diagnostic candidate.
- Comparison method: relative-path inventory, byte size and SHA-256; no source content, absolute private path, credential value, binary or backup is published.
- Exclusions from comparison population: generated build directories, Git metadata and `components/esp_wifi_bsp/`. The last directory was already accepted as outside the effective build graph and remains untouched in both trees.

### Exact delta

The following 11 files exist only in the preserved A-010 tree:

- `components/remote_persistence/CMakeLists.txt`
- `components/remote_persistence/backend.cpp`
- `components/remote_persistence/esp_nvs_store.cpp`
- `components/remote_persistence/diagnostic.cpp`
- `components/remote_persistence/diagnostic_runtime.cpp`
- `components/remote_persistence/include/remote_persistence/backend.hpp`
- `components/remote_persistence/include/remote_persistence/esp_nvs_store.hpp`
- `components/remote_persistence/include/remote_persistence/diagnostic.hpp`
- `tests/remote_persistence/backend_tests.cpp`
- `tests/remote_persistence/diagnostic_tests.cpp`
- `sdkconfig.remote01_a010_diag`

The following six files differ:

| File | Accepted A-010 delta |
| --- | --- |
| `partitions.csv` | Adds only `remote_ctl`, data/NVS, offset `0xE20000`, size `0x10000`; all six prior entries and both 3 MiB OTA slots remain byte-identical. |
| `components/control_home/CMakeLists.txt` | Adds the private `remote_persistence` dependency. |
| `components/control_home/runtime.cpp` | Adds the compile-gated A-010 UART diagnostic include, announcement and byte consumer. With the production flag unset, no persistence action occurs at boot. |
| `main/CMakeLists.txt` | Registers `remote_persistence` as a private requirement. |
| `platformio.ini` | Adds only the separate `remote01_a010_diag` environment and its diagnostic compile definition; production `remote01` settings are unchanged. |
| `CHANGELOG.md` | Appends the private A-010 implementation and validation history. |

There are no active-only files in the scoped inventory. All other 1,695 files are SHA-256-identical, including UI, GPIO, network provisioning, power/sleep, control model and device configuration sources.

### Controlled reconciliation procedure

1. Preserve both current trees read-only and record complete private manifests before action.
2. Create a new private disposable copy from the active workspace; do not reconcile in place.
3. Copy the eight `remote_persistence` implementation/header/build files and the two focused host tests byte-for-byte from the preserved A-010 tree.
4. Apply the five source/build deltas above exactly. Append the A-010 changelog material without replacing active history.
5. Carry `sdkconfig.remote01_a010_diag` only as the accepted diagnostic-profile configuration. It must not replace `sdkconfig.remote01` or `sdkconfig.defaults`.
6. Confirm the seven-entry CSV preserves every old offset/size and matches the installed A-009 table; no partition write is part of reconciliation.
7. Re-run the A-010 host tests and a clean serial production build. Verify the production build leaves diagnostics disabled, performs no boot-time `remote_ctl` open/write, and retains prior UI/network/sleep component hashes where expected.
8. Compare candidate firmware size, static RAM, map and partition binary with the accepted A-010 evidence. A changed build timestamp or link layout is recorded but is not by itself a blocker; selected code/configuration and functional deltas are.
9. Keep the reconciled tree private. Promotion into the named active workspace requires a later owner-approved implementation step and a reversible file-level backup.

This procedure preserves the validated A-010 ordering: generation fence, CRC record, authority root, three bounded slots, 4,096-byte maximum payload, explicit initialization, fail-closed ambiguity/corruption handling and no generation reuse. It does not erase or rewrite the installed generation-2 test records.

## 2. Recommended secure transport

### Persistent TCP with a PSK AES-GCM record layer

Both devices already use Wi-Fi station mode and already contain TCP/IP plus mbedTLS. TUNER's ordinary web manager has been exercised while Bluetooth A2DP is active, so this choice reuses a demonstrated coexistence path rather than adding another radio protocol. Both pinned frameworks enable AES-GCM and HMAC-SHA-256; no third-party network or cryptographic library is required.

The bounded security profile proposed for owner approval is:

- one TUNER listener on a dedicated private port and one REMOTE connection;
- a random 32-byte per-pair PSK, generated outside source control and provisioned privately to both devices;
- mutual challenge/response using independent 128-bit random nonces and HMAC-SHA-256 over a fixed, versioned transcript;
- directional AES-128-GCM keys derived from the PSK, both nonces, direction labels and transcript with RFC 5869 HKDF-SHA-256 implemented over the existing HMAC primitive;
- a 96-bit GCM nonce composed from a fresh per-session directional salt and a 64-bit strictly increasing record counter;
- a fixed header authenticated as associated data, a 16-byte GCM tag and a maximum plaintext record of 512 bytes;
- reject-before-parse on bad version, length, tag, session or counter; close the connection on any authentication or ordering failure;
- never compile the operational PSK into the public TUNER repository or publish it in coordination evidence;
- persist only the pairing identity and CCM-required durable non-reuse state. Session keys/nonces remain volatile and are zeroized on disconnect/sleep;
- all socket bytes enter a fixed queue. TUNER control dispatch stays on its existing main-loop owner and REMOTE Core ingress stays on its existing owner.

TCP delivery is not operation completion. Each CCM request still carries its request/session identity and receives a correlated CCM lifecycle/result. Automatic retry remains disabled.

Reconnect/resynchronization is explicit:

1. Establish TCP, exchange the fixed-version challenge transcript and prove possession of the provisioned PSK in both directions.
2. Derive fresh directional record keys and reset record counters only for that fresh authenticated session.
3. Negotiate device/version identity and capability revision inside the authenticated channel.
4. REMOTE invalidates old-session observations and requests a complete capability/state snapshot.
5. TUNER publishes monotonically sequenced `volume.level` and `playback.state` observations for that session.
6. Socket loss or bounded heartbeat timeout marks the binding unreachable. Reconnect creates new nonces/keys/session generation, performs full resynchronization and discards queued old-session commands.

This defines transport behavior only. It does not add or change CCM operations, fields or result semantics.

## 3. Alternatives rejected for milestone 1

### WebSocket over TLS with device authentication

**Framework fit:** REMOTE has ESP-IDF TLS/client facilities. TUNER's pinned Arduino/IDF package contains `esp_https_server` and client-certificate support, but no WebSocket dependency is currently pinned; adding WSS would require another library or a low-level HTTPS/WebSocket server integration alongside the existing synchronous port-80 manager.

**Security fit:** pinned server certificate plus client certificate, or a pinned server certificate plus an application pairing credential, can provide strong mutual device authentication.

**Reason rejected now:** Espressif's HTTPS server declares roughly 40 KiB RAM per SSL socket and a default 10 KiB server task stack. TUNER evidence shows free internal heap commonly around 5–10 KiB and largest blocks as low as 980–1,396 bytes during relevant Wi-Fi/Bluetooth/web activity, including observed recoverable allocation failures. WSS also adds certificates, TLS buffers, handshake peaks and another long-lived service. Flash headroom is ample, but internal RAM is not. This alternative can be reconsidered only after a measured memory redesign; it is not suitable for the minimum milestone.

### HTTPS request/response or long polling

This has simpler application behavior than WebSocket and good reconnect semantics, but it uses the same TLS server and handshake memory on TUNER. Repeated connections can be worse than one persistent WSS connection. Reusing the existing plaintext `WebServer` with tokens or HMAC would reduce memory, but it does not provide an approved secure transport and would expose state/commands to passive observers. Rejected.

### Encrypted ESP-NOW

ESP-NOW is available in both frameworks and supports CCMP with per-peer keys, but the version-specific evidence rejects it for this baseline. The TUNER is pinned to ESP-IDF 4.4.7; Espressif's 4.4 coexistence table marks ESP-NOW receive with Classic Bluetooth as unsupported. Later ESP-IDF tables report stable STA-mode coexistence, but those results cannot be imported into v1.1.11. ESP-NOW also binds both peers to the current Wi-Fi channel and would add a new coexistence path when ordinary TCP is already proven with A2DP/web-manager operation. Rejected for milestone 1.

### MQTT/TLS or an external broker

Adds broker availability, credentials, topic policy and cloud/LAN infrastructure to a direct two-device feature. It is explicitly outside the milestone and retains TLS memory on at least the clients. Rejected.

### CoAP/DTLS

Can be compact, but no such path exists in either application, DTLS still requires cryptographic buffers and session management, and it adds more implementation risk than the built-in encrypted ESP-NOW path. Rejected.

## 4. Expected memory and flash impact

These are planning bounds, not measured build results.

### TUNER

- TCP/IP and AES-GCM/HMAC primitives are already in the pinned framework. Incremental application flash should be small relative to the current 1.12 MiB app-slot headroom; exact size remains build-measured.
- Use one client, two fixed 640-byte wire buffers, a small fixed queue and no dynamic JSON document on the socket path.
- Internal RAM target for new long-lived application state: under 6 KiB, including socket owner stack delta but excluding existing Wi-Fi-driver memory; exact delta must be measured.
- Main risk is fragmentation and transient buffer pressure in the already tight Wi-Fi/A2DP/web-manager workload. The acceptance gate is measured internal free/largest block and unchanged audio/web behavior, not a linked-RAM total alone.

### REMOTE

- The accepted A-010 production-backend build has 649,328 bytes OTA headroom, so flash is not the expected constraint.
- Add fixed transport queues/envelopes, peer/session state and compact persisted association/dedup state. Keep the persisted envelope far below the 4,096-byte backend maximum.
- Sleep must deinitialize/reinitialize ESP-NOW through the existing network/power owner path, increment session generation and discard old callbacks/queued commands.
- Do not write `remote_ctl` on every observation or heartbeat. Persist only association and required non-reuse/dedup state at bounded transitions.

## 5. Minimum implementation sequence

1. Privately reconcile REMOTE into a disposable A-010-complete source copy and repeat A-010 host/build checks.
2. Approve the persistent-TCP/PSK-AES-GCM transport profile and private pairing method.
3. Specify the exact authenticated transcript, RFC 5869 inputs, nonce layout and bounded record bytes; publish non-secret host test vectors for owner review before device integration.
4. TUNER: add the single-client socket/record adapter and main-loop owner; implement authenticated handshake, identity/version, capability snapshot and independently sampled volume/playback state. Preserve every existing radio, MP3, A2DP, Wi-Fi and web-manager path.
5. TUNER: implement only validated `volume.set`; reject invalid normalized values before `AudioPlayer::setVolume()`. Do not expose playback or station operations.
6. REMOTE: add the authenticated TCP client adapter, translate session/capability/state events into the existing CCM Core, and route captured `volume.set` results back to Core.
7. REMOTE: persist only the approved association/non-reuse subset through `remote_persistence`; no automatic initialization merely on boot.
8. Run focused host tests and clean builds on both devices. Measure flash/static RAM and runtime internal heap/largest block/stack under TUNER radio, A2DP plus web-manager, and reconnect scenarios.
9. Publish sanitized hashes/results, then request separate hardware-flash authorization. Hardware work is not part of this phase.

## 6. Owner decisions required

Implementation remains stopped pending explicit owner acceptance of both items:

1. **REMOTE baseline:** authorize the disposable-copy reconciliation described above and later promotion into the active private workspace after verification.
2. **Transport and commissioning:** approve one persistent TCP client with the bounded PSK/HMAC/AES-GCM record profile above, and a private serial commissioning procedure that provisions a random per-pair PSK and TUNER address without committing or publishing them.

No decision is needed on CCM semantics: CCM 1.1.0 remains frozen and unchanged. Exact envelope bytes and test vectors can be prepared after the transport decision, before firmware integration.

## Sources and evidence

- Frozen contract: `references/CCM_1_1_0.md`.
- Kickoff: `reports/A-REMOTE-011_KICKOFF.md`.
- Private source comparison: local SHA-256 inventory; only aggregate and paths above are published.
- TUNER resource evidence: v1.1.11 build and hardware records already present in its public repository.
- Version-specific ESP-NOW/Classic Bluetooth limitation: [ESP-IDF 4.4 RF coexistence guide](https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-guides/coexist.html).
- HTTPS-server RAM statement: [ESP-IDF HTTPS server](https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-reference/protocols/esp_https_server.html).
