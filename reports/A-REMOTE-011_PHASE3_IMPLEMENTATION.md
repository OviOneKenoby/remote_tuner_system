# A-REMOTE-011 Phase 3: first RTCP/1 and CCM integration slice

## Result

**IMPLEMENTED AND BUILD-VERIFIED — HARDWARE COMMISSIONING NOT STARTED.**

The accepted A-010 source was promoted into the active private REMOTE workspace after a complete reversible private backup. The promoted population matched the reconciled source across all 1,715 non-generated files with zero missing, additional or hash-different files before implementation.

TUNER commit `18ddd3b16e305341f338afebd7dc725500ecbb73` and the private REMOTE candidate implement the Phase 3 slice without changing CCM 1.1.0 or RTCP/1. No firmware was flashed, no device was accessed, no operational PSK was generated, and no private REMOTE source or binary is published.

## Implemented behavior

- TUNER services one nonblocking TCP client from its existing main loop. It adds no task and uses fixed 556-byte receive and transmit buffers.
- Both peers implement the frozen three-message mutual authentication, transcript-bound HMAC proofs, RFC 5869 HKDF-SHA-256, directional AES-128-GCM keys, exact counters, 512-byte plaintext limit, fail-closed record handling and complete volatile-session invalidation.
- Pairing material is read only from private persistent storage. Missing or invalid association data disables transport without modifying storage or changing existing behavior.
- REMOTE reserves a successor association/session generation with the accepted A-010 fence/record/root commit before a connection attempt. A failed or interrupted reservation is never reused.
- After authentication, REMOTE validates CCM 1.1.0 identity and the bounded capability snapshot, obtains fresh `volume.level` and `playback.state`, and periodically resynchronizes the snapshot.
- `volume.set` is range and exact-grid validated, admits one request at a time and reports a correlated result. It is never retried automatically.
- TUNER request dispatch remains on the existing main-loop owner. The TUNER playback enum is mapped explicitly to CCM rather than relying on incompatible numeric enum order.
- REMOTE closes its session during the existing power suspend path and requires a fresh handshake and resynchronization after resume.

## Files changed

Public TUNER source:

- `src/rtcp_server.h`, `src/rtcp_server.cpp`
- `src/ccm_wire.h`, `src/ccm_wire.cpp`
- `src/main.cpp`
- `tests/test_ccm_wire.cpp`
- `CHANGELOG.md`

Private REMOTE source (relative paths only):

- `components/rtcp_client/{CMakeLists.txt,association.cpp,client.cpp,wire.cpp}` and its three public headers
- `components/control_home/{CMakeLists.txt,rtcp_device.cpp,runtime.cpp}`
- `components/control_home/include/control_home/{development.hpp,power_suspend.hpp,rtcp_device.hpp}`
- `tests/rtcp_client/host_tests.cpp`
- `main/CMakeLists.txt`, `sdkconfig.defaults`, `sdkconfig`, `sdkconfig.remote01`, `CHANGELOG.md`

The seven-entry partition layout is unchanged. The production partition binary remains byte-identical to the installed A-009 table.

## Verification

Existing Phase 2 inputs remain valid: A-010 tests are 28/28 PASS and the RTCP/1 reference suite is 14/14 PASS. New bounded application-codec tests are 10/10 PASS on TUNER and 10/10 PASS on REMOTE. Final production builds compile the actual transport and adapters:

| Result | REMOTE `remote01` | TUNER `esp32-lwip-psram` |
| --- | ---: | ---: |
| Clean serial build | PASS | PASS |
| Linked flash | 2,515,085 bytes | 2,028,225 bytes |
| Packaged firmware | 2,515,584 bytes | 2,034,800 bytes |
| OTA slot | 3,145,728 bytes | 3,145,728 bytes |
| Packaged OTA headroom | 630,144 bytes | 1,110,928 bytes |
| Static RAM report | 47,076 / 327,680 bytes | 87,408 / 327,680 bytes |

Against the accepted Phase 2 evidence, REMOTE packaged flash increased 19,264 bytes and reported static RAM decreased 8 bytes. TUNER packaged flash increased 6,128 bytes and static RAM increased 1,472 bytes. The TUNER increase is within the 64 KiB planning ceiling; runtime internal-heap coexistence remains the principal hardware-test risk because prior Wi-Fi plus A2DP plus web-manager evidence had only 5–10 KiB free internal heap.

Artifact hashes are evidence identities, not publication artifacts:

| Artifact | SHA-256 |
| --- | --- |
| REMOTE firmware | `ceae9f64329c5409fdfe92e5ac5394885010abf1cf66ac24a5ab7fcc35f11647` |
| REMOTE ELF | `fa06311f2e1e60971c6fa6ef7907ef7c5793f79dff833d1abf6bf60960b4d5c4` |
| REMOTE map | `c24be41275e1b66377b2e8a138719b857bdb8b6dc94f04fb8b4211cdffd5f549` |
| REMOTE partitions | `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184` |
| TUNER firmware | `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4` |
| TUNER ELF | `9d650ec9e55ef4e249117c09356be26b04561412dd6fe39bcd15587080f9c778` |
| TUNER map | `8735b3bd642f8a47c0cb57bbec602f297944777ecc507a918574b747fc62d22e` |
| TUNER partitions | `aaae2888c5a6a348004b5b436f47abb25ae32e72d9003902955a998eda723edd` |

REMOTE production diagnostics are disabled: the production configuration does not define `A010_REMOTE_PERSISTENCE_DIAGNOSTIC`, and its identity/confirmation strings are absent from `firmware.bin`.

## Remaining practical risks and next decision

Compilation and bounded host tests establish source-level integration, not end-to-end device behavior. Pairing provisioning, authenticated inter-device traffic, reconnect after real Wi-Fi loss/sleep, actual TUNER heap margin during MP3 and A2DP coexistence, and retained device UI/configuration require owner-authorized hardware commissioning. The existing A-010 generation-2 test record is not a valid A-011 association, so the uncommissioned REMOTE candidate remains on its prior local behavior and performs no persistence write.

The next owner decision is whether to authorize a staged, reversible hardware protocol covering backup verification, exact candidate flashing, private pairing provisioning, authenticated read-only negotiation/snapshot, one controlled `volume.set`, reconnect/resynchronization, MP3/A2DP/web-manager coexistence measurements, and rollback. PR #17 remains open and unmerged.
