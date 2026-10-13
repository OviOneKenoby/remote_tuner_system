# A-REMOTE-010 diagnostic validation candidate

Recorded UTC: 2026-10-13T06:43:09.576743+00:00. Continuation input `e7aa84370098e1096bf18d87856de65a440a1c4a`; assignment commit `09930a610de936596a6f3ee2c92cc9aa4d1766b7`; [owner continuation authorization](../references/A010_DIAGNOSTIC_CONTINUATION_OWNER_AUTHORIZATION_2026-10-13.md); [PR #16](https://github.com/OviOneKenoby/remote_tuner_system/pull/16).

**PASS — DIAGNOSTIC CANDIDATE IMPLEMENTED / HOST VERIFIED / CLEAN BUILD; HARDWARE NOT RUN.** The accepted A-REMOTE-010 host phase is preserved. The diagnostic continuation remains private and PR #16 remains open/unmerged.

## Build gate and activation

The normal `remote01` environment has no diagnostic definition and compiles the hook out. Only `remote01_a010_diag` defines `A010_REMOTE_PERSISTENCE_DIAGNOSTIC=1`. Its boot log identifies `build=A010_VALIDATION diagnostic=ENABLED persistence_on_boot=0`. The existing `control_home` USB-serial reader owns all input; the candidate reserves only lines beginning `!A010 `. This avoids a second UART consumer.

Boot calls only the identity announcement. It does not inspect, open, initialize, recover, commit or erase `remote_ctl`. `app_main` has no persistence reference. Target/backend/NVS methods are reachable only after a complete explicit diagnostic line; the disabled-state host test produces zero target calls.

## Exact command set

Read-only commands:

- `!A010 HELP`
- `!A010 INFO`
- `!A010 STATUS`
- `!A010 RECOVER`

Mutating commands, disabled until this exact candidate is running and rejected without the exact token:

- `!A010 INIT CONFIRM-A010-REMOTE-CTL-INIT`
- `!A010 COMMIT1 CONFIRM-A010-REMOTE-CTL-COMMIT1`
- `!A010 COMMIT2 CONFIRM-A010-REMOTE-CTL-COMMIT2`
- `!A010 ERASE CONFIRM-A010-REMOTE-CTL-ERASE`

Every mutation first requires label `remote_ctl`, data/NVS type/subtype, offset `0xE20000` and size `0x10000`. `INIT` additionally requires an erased partition; `COMMIT1` requires clean initialized generation 0; `COMMIT2` requires clean generation 1. `ERASE` is independent and never follows a failure automatically. Commands accept no partition labels, offsets, raw addresses or payloads. The two fixed 24-byte non-secret test payloads are compiled in and never printed. Replies contain before/after state, generation, incomplete flag and safe entry counts only.

## Private source delta for this continuation

Modified: `CHANGELOG.md`, `components/control_home/CMakeLists.txt`, `components/control_home/runtime.cpp`, `components/remote_persistence/CMakeLists.txt`, `components/remote_persistence/esp_nvs_store.cpp`, `components/remote_persistence/include/remote_persistence/esp_nvs_store.hpp`, `platformio.ini`.

Added: `components/remote_persistence/diagnostic.cpp`, `components/remote_persistence/diagnostic_runtime.cpp`, `components/remote_persistence/include/remote_persistence/diagnostic.hpp`, `tests/remote_persistence/diagnostic_tests.cpp`.

The original source tree remains untouched. The private A-010 backend files, installed partition layout and TUNER are otherwise unchanged.

## Verification

Backend regression tests: **14/14 PASS**. Diagnostic tests: **14/14 PASS**. Combined: **28/28 PASS** with MSYS2 UCRT64 g++ 16.2.0 and strict warnings. The diagnostic cases cover disabled state, parsing, token rejection, exact partition identity, erased/valid/corrupt/ambiguous status, ordered init/first/successor commits, out-of-sequence rejection, erase guards, explicit erase and payload-log exclusion. [Sanitized tests](../references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_HOST_TESTS_SANITIZED.log).

ESP-IDF adapter review: **PASS**. It initializes only `remote_ctl` by label after the fixed identity guard, opens with `nvs_open_from_partition`, uses read-only or read-write handles explicitly, closes by RAII, releases iterators on all list exits, stages blobs then calls `nvs_commit`, maps not-found/no-space/no-free-pages/new-version/I/O failures, and contains no hidden automatic erase. The only `nvs_flash_erase_partition` call is the separately confirmed diagnostic `ERASE` path.

Clean serial candidate build: **PASS**, 492.70 seconds. Packaged firmware is **2,503,936 bytes**, leaving **641,792 bytes** in each 3,145,728-byte OTA slot. Firmware SHA-256 `308181d4144494734fe8fae360938f74b9f886fb4c41bff0cba9b89427e4d248`; ELF `d987f5e988ed07ed1b07ef33749108048f5bce4eb047af8de948795b518a7c94`; map `5179002f97c56f3debd78dc9a4fd7d923a0f750078164fe08b430fd1ba6c03f2`; partitions `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`; bootloader `bcb42f4af313d0cdaa10668711f0a82b809073a603cc4ab2d2a34cc2d0ac8bf0`. The ELF contains all backend and diagnostic entry points. The boot identity string is present in the packaged firmware. Generated `partitions.bin` is byte-identical to accepted A-REMOTE-009. Artifacts remain private. [Artifact record](../references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_ARTIFACT_SHA256.json); [build summary](../references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_BUILD_SANITIZED.log).

A secret-pattern scan over all continuation-added/modified source passed. No private source, binaries, payloads, credentials, flash images, device identifiers or absolute private paths are published.

## Remaining checkpoint

No target execution has occurred. Actual USB identity, candidate boot, UART routing, NVS initialization, commits, reboot recovery, capacity reporting and controlled restoration remain untested. The [complete hardware protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md) stops before device contact and again before each mutating stage. Optional `remote_ctl` erase requires separate explicit authorization.

Next owner decision: review this exact candidate and authorize or reject the hardware-validation phase. The first proposed hardware operation is a read-only ESP32-S3 ROM/USB identity query on the newly verified COM port. Candidate flashing and every `remote_ctl` mutation remain separately gated. A-REMOTE-011 is NOT STARTED.
