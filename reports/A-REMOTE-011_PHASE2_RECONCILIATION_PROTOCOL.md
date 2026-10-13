# A-REMOTE-011 Phase 2: reconciled REMOTE baseline and authenticated TCP records

## Result

**PASS — PRIVATE RECONCILIATION AND SPECIFICATION COMPLETE; NETWORK INTEGRATION NOT STARTED.**

A disposable private REMOTE source copy now matches the preserved, owner-accepted A-010 source across all 1,715 non-generated files. The named active REMOTE workspace and preserved A-010 tree were not changed. The copy retains the seven-entry partition layout, two 3 MiB OTA slots, existing UI, configuration, GPIO, provisioning and sleep/wake sources, and the validated `remote_ctl` backend.

Focused A-010 host tests pass 28/28. A clean single-job production build passes. The normal `remote01` environment has no A-010 diagnostic definition, identity or mutation-command strings, and no diagnostic runtime path is enabled. No hardware was accessed and no firmware was flashed.

The exact RTCP/1 transport binding is published at [A_REMOTE_011_AUTHENTICATED_TCP_V1.md](../references/A_REMOTE_011_AUTHENTICATED_TCP_V1.md), with executable public vectors and focused tests. It uses one persistent TCP connection, a privately provisioned random 32-byte per-pair PSK, mutually authenticated fresh nonces, RFC 5869 HKDF-SHA-256, directional AES-128-GCM records, strict counters and a 512-byte plaintext ceiling. CCM 1.1.0 remains unchanged.

## 1. Private REMOTE reconciliation

The disposable copy was created from the active workspace, excluding generated build and Git directories. The accepted A-010 additions and controlled build/source deltas identified in Phase 1 were overlaid byte-for-byte from the preserved A-010 tree. A complete relative-path/SHA-256 comparison reported:

| Population | Result |
| --- | ---: |
| Accepted A-010 non-generated files | 1,715 |
| Reconciled non-generated files | 1,715 |
| Missing, additional or hash-different files | 0 |

This establishes source reconciliation without inferring firmware byte reproducibility. The active workspace remains at its pre-reconciliation state. No private source, credential-bearing component, firmware image or absolute private path is published.

The accepted backend behavior is preserved: schema 1; three record slots; 4,096-byte payload bound; generation fence, record and authority-root ordering; explicit erased-partition initialization; fail-closed corruption/ambiguity handling; and no reuse of an uncommitted generation. Production boot still has no caller that initializes or writes `remote_ctl`.

## 2. Verification

### Focused host tests

- Tool: MSYS2 UCRT64 g++ 16.2.0, C++20, `-Wall -Wextra -Werror -pedantic`.
- Backend suite: **14/14 PASS**.
- Diagnostic adapter suite: **14/14 PASS**.
- Combined: **28/28 PASS**.

### Clean production build

- Clean `remote01`, serial `-j1`: **PASS**, 533.92 seconds.
- Platform/framework/toolchain: espressif32 6.13.0, ESP-IDF 5.5.3, xtensa-esp-elf 14.2.0+20251107.
- Linked flash use: 2,495,817 / 8,388,608 bytes.
- Static RAM report: 47,084 / 327,680 bytes, identical to the accepted A-010 production report.
- Packaged firmware: 2,496,320 bytes; 649,408 bytes remain in each 3,145,728-byte OTA slot.
- Firmware SHA-256: `78518cd3734304c1f213f16e870a53ff127b7fe263eaf2be7f671ef547a0fe33`.
- ELF SHA-256: `f471f93133b01ae2db0bb94b853b37aabcf9a416d0be9632c26828c183057108`.
- Map SHA-256: `325a329390896da512080513c94866d80838c39c3e298ca5246d929de9e6a4e4`.
- Bootloader SHA-256: `6154bea1da62e8a2ef54108f8eb630a78c5452c77f149a612b26f57148f99b1d`.
- Partition binary SHA-256: `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`, byte-identical to the accepted/installed A-009 evidence.

The new firmware hash is a build result, not a byte-identity claim against the historical A-010 image. Its packaged size differs by 80 bytes while selected source, partition binary and reported static RAM match. No functional/configuration discrepancy was found, so the approved practical scope does not reopen build forensics.

Production checks found zero `A010_REMOTE_PERSISTENCE_DIAGNOSTIC` definitions and zero occurrences of the diagnostic identity, confirmation prefix, INIT or COMMIT command strings in `firmware.bin`. The diagnostic environment remains separate and was not built.

## 3. RTCP/1 authenticated records

The exact profile fixes the previously open transport details:

- three fixed-size handshake messages with independent 128-bit CSPRNG nonces and HMAC-SHA-256 proofs bound to the transcript;
- separate RFC 5869 expansions for directional AES-128 keys, four-byte nonce prefixes and an eight-byte session ID;
- a 28-byte authenticated header, 512-byte maximum plaintext and 16-byte GCM tag, for a 556-byte maximum wire record;
- a 96-bit GCM nonce made from the directional prefix and unsigned 64-bit counter starting at one;
- exact-next-counter acceptance, close-before-wrap and session closure on any framing, authentication, ordering, entropy or allocation failure;
- one command awaiting its CCM result, with no automatic retry;
- complete volatile-session invalidation on disconnect or sleep and a fresh handshake plus full resynchronization after reconnect.

The public vector PSK is sequential test data explicitly forbidden for devices. The Python reference uses the `cryptography` package's HKDF and AESGCM implementations; it does not implement a cryptographic primitive.

Transport host tests: **14/14 PASS**. They cover committed-vector stability, proof sensitivity to PSK, direction separation, authenticated round trip, exact 512/513-byte boundary, header/ciphertext/tag alteration, duplicate and skipped counters, exhaustion, truncation and rejection of an old-session record after reconnect.

## 4. Initial TUNER budget and risks

This is an implementation budget, not a measured firmware delta:

| Item | Initial bound / placement |
| --- | --- |
| RX and TX wire buffers | 556 bytes each; prefer PSRAM on TUNER, fixed allocation |
| Session/counter/parser state | at most 512 bytes internal RAM |
| Reused mbedTLS HMAC/GCM working state | reserve at most 1 KiB internal pending compiled measurement |
| Command concurrency | one command; no retry queue or dynamic JSON document |
| Task stack | no new task; service from the existing main-loop/network owner |
| Incremental application flash | planning ceiling 64 KiB; actual link delta is the gate |

Application-owned long-lived internal RAM should remain below 1.5 KiB when wire buffers are in PSRAM, or below about 2.7 KiB if they must be internal. lwIP PCB/pbuf allocation is framework-owned and must be measured separately. The genuine risk is TUNER's previously observed 5–10 KiB free internal heap and small largest blocks during Wi-Fi + A2DP + web-manager operation. Implementation must fail closed when fixed resources are unavailable and pass measured coexistence checks before merge. Flash headroom is not presently a blocker.

## 5. Minimum implementation sequence

1. With separate owner approval, promote the verified reconciled files into a backed-up private REMOTE implementation workspace.
2. Add a TUNER single-client nonblocking RTCP/1 listener around existing Wi-Fi and main-loop ownership; add no new task and preserve the current web manager.
3. Implement only encrypted identity/version and capability exchange, read-only `volume.level` and `playback.state`, and `volume.set` with one in-flight command.
4. Add the private REMOTE RTCP/1 client and connect authenticated events to existing CCM ingress/Core; persist only the later approved association/non-reuse subset through the accepted backend.
5. Run focused tests and clean builds, then measure TUNER internal free/largest block and behavior with MP3, Bluetooth A2DP, Wi-Fi and the web manager before seeking hardware-flash authorization.

The obsolete Phase 1 ESP-NOW sleep sentence has been corrected to the selected TCP close/session-invalidation behavior. TUNER and REMOTE firmware network integration, operational PSK generation, active-workspace promotion and hardware operations remain unexecuted.
