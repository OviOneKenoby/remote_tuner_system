# A-REMOTE-010 private persistence backend report

Recorded UTC: 2026-10-13T03:35:07.084328+00:00. Coordination input `3ed3ff49f8ff6ba548a8b3b23020ad6a32c4566f`; assignment commit `09930a610de936596a6f3ee2c92cc9aa4d1766b7`; [owner authorization](../references/A010_PRIVATE_IMPLEMENTATION_OWNER_AUTHORIZATION_2026-10-12.md); [PR #16](https://github.com/OviOneKenoby/remote_tuner_system/pull/16).

**PASS — PRIVATE IMPLEMENTATION / HOST VERIFIED / CLEAN BUILD; HARDWARE NOT RUN.** A-REMOTE-010 is READY FOR OWNER REVIEW. The implementation remains in a restricted private copy. No device access, upload, flash write, erase, NVS mutation, partition change, recovery action, or A-REMOTE-011 work occurred.

## Small bounded backend

The backend opens only `remote_ctl` / `ctl_v1` after confirming data/NVS type, address `0xE20000`, and size `0x10000`. It never calls the default-NVS initializer or any erase function. Opening, erased-partition initialization, recovery, and commit are explicit; no runtime caller exists, so normal boot does not open or write the partition. Stored payloads are never logged.

Schema v1 has one authoritative generic envelope, three rotating physical record slots, and a 4096-byte maximum payload. Generation is unsigned 64-bit, begins at 1, must equal the next reserved value, and cannot wrap. Commit order is: (1) durably reserve generation in a CRC-protected fence; (2) durably commit a schema-tagged record with payload and envelope CRCs; (3) durably publish a CRC-protected root naming the exact slot, generation and record CRC. A failed transaction consumes its reserved generation. Recovery follows only an exact valid root/record pair; dangling newer fence/record state is reported as incomplete and never gains authority. Corrupt, unknown, duplicate-generation, stale, mismatched or structurally ambiguous state fails closed. NVS full/no-free-pages/new-version errors return failure without erase.

This implements CCM 1.1.0 G1a for the bounded ordinary interruption/corruption model. Deliberate complete coherent restoration of root, fence and records remains G1b, outside the V1 threat model, as already owner accepted.

## Private paths changed

Modified: `CHANGELOG.md`, `main/CMakeLists.txt`, `partitions.csv`. Added: `components/remote_persistence/CMakeLists.txt`, `components/remote_persistence/backend.cpp`, `components/remote_persistence/esp_nvs_store.cpp`, `components/remote_persistence/include/remote_persistence/backend.hpp`, `components/remote_persistence/include/remote_persistence/esp_nvs_store.hpp`, `tests/remote_persistence/backend_tests.cpp`. A byte audit found no other original/private-copy difference outside generated `.pio` output. The original source tree was not edited. The CSV update only mirrors the already installed and accepted A-009 layout; generated `partitions.bin` is byte-identical to A-009.

## Verification

Focused host tests compile the actual backend implementation with MSYS2 UCRT64 g++ 16.2.0 and `-std=c++20 -Wall -Wextra -Werror -pedantic`: **14/14 PASS**. Cases cover erased initialization; first and successor commits; interruption after fence and after record/before root; corrupt record and root; duplicate generation; bounded capacity; restart selection with zero command emission; replay/non-monotonic rejection; NVS capacity/version errors; unknown-key ambiguity; and the explicit coherent-domain rollback exclusion. [Sanitized test log](../references/device_evidence/remote/A-REMOTE-010/HOST_TESTS_SANITIZED.log).

Final clean serial `-j1` target build: **PASS**, 512.09 seconds. Tool identity: PlatformIO 6.2.0, espressif32 6.13.0, ESP-IDF 5.5.3, xtensa-esp-elf GCC 14.2.0+20251107. Both backend sources compiled with warnings as errors. The final ELF contains `Backend::recover()`, `EspNvsStore::open()`, and two linker-only anchors; no runtime caller exists. Firmware is **2,496,400 bytes**; each 3,145,728-byte OTA slot retains **649,328 bytes**. Firmware SHA-256 `b045bbe720091da89871a36686d17aa2ca06a27efdca05a90d2b660120f55dd3`; ELF `8217bdf2ee0f1dcddea2b6532924a07d357ce7b8a8c636327c4117a728929ee0`; map `b0b31e6c977ef91f4e8886f0cb9f6a14cca944cf3e82b5b829dda01344b5bac6`; partitions `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`; bootloader `3b66c48324a1287759e467da62138fd5aeadab069b655561536a718d1be86f97`. Artifacts remain private. [Hashes](../references/device_evidence/remote/A-REMOTE-010/ARTIFACT_SHA256.json); [sanitized build](../references/device_evidence/remote/A-REMOTE-010/BUILD_SANITIZED.log).

A credential-pattern scan over all A-010-added source/test files passed. No source, payload, credential, executable, SDK/toolchain, firmware, ELF, map, flash image, MAC, or absolute private path is published.

## Practical limits and owner checkpoint

Physical initialization, commits, interruption behavior, NVS capacity and reboot recovery are NOT RUN. Host interruption tests use a deterministic store model; target behavior still relies on ESP-IDF NVS commit semantics. Three record slots and a 4096-byte payload cap are implementation limits, not a claim that all 64 KiB is usable application payload. Deliberate coherent whole-domain rollback is undetectable by this partition-local design. Exact byte reproducibility and exact equivalence to the installed A-006 image remain unproven under the accepted A-008 limits.

The clean candidate deliberately has no runtime invocation or diagnostic trigger. This prevents boot-time writes, but means a later physical backend exercise must first add and review a narrowly gated, non-production diagnostic activation with its exact artifact hash. The [hardware protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md) stops at that prerequisite and again before the first persistent operation.

Next owner decision: review the private implementation evidence and choose whether to accept this host phase, then authorize a scoped continuation that adds/reviews the explicit diagnostic activation and separately authorizes the exact firmware flash plus controlled `remote_ctl` writes. PR #16 remains OPEN/unmerged. CCM 1.1.0 remains frozen; Native API unapproved; O01–O17/common gate open; TUNER unchanged; A-REMOTE-011 NOT STARTED.
