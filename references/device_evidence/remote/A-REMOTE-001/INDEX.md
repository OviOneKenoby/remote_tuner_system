# A-REMOTE-001 evidence index

Read-only capture on 2026-10-08 from the owner-provided REMOTE workspace.
Coordination input: `769c4dc1f50acebbf855b06d4bcf9cfc5eba7e16`.
Snapshot files are byte-preserved entry evidence, not synchronized firmware.
Do not edit them; add later revision-specific evidence separately.

- [Baseline and existing artifact identity](BASELINE.json): BIN/ELF/partition sizes/hashes and parsed ESP app descriptor. No binary files uploaded; flashed artifact and source-to-artifact correspondence UNKNOWN.
- [Entry source SHA-256 inventory](SOURCE_SHA256.json): all 1704 non-`.pio/` entry files, including generated test products where present; path/hash inventory, not a source-only build recipe. Whole-workspace 4038-file entry inventory retained locally for final preservation checking.
- [Original owner freeze instruction excerpt](OWNER_FREEZE_APPROVAL_EXCERPT.txt): exact bytes of lines 1?135 from owner attachment73e8283c-9f10-4dec-aa3f-7db8d6a9e94a/Pasted text.txt. Full original source hash/path in BASELINE.json; later API-task text omitted, excerpt never presented as the complete attachment. Explicit approval at original line24; promotion/status-only instructions at lines54?69; no new approval issued.
- [Historical candidate versus recovered frozen file](CCM_CANDIDATE_TO_FROZEN.diff): informational text diff. Byte comparison of sections1?20 independently PASS with exactly two version substitutions. Header/section21 are status records.
- [Inspection command/result record](INSPECTION.md).
- [Final documentation validation](VALIDATION.md).

Recovered CCM SHA-256 `7a46f9fffe706476de458aac078d0af1c94844df339248d3f9f4b5cf033011d7`; Native candidate remains unapproved/unfrozen. Current handoff SHA matches imported canonical requirements exactly. Source findings are not fresh build or physical verification.

## Byte-preserved snapshots

| Original REMOTE-relative path | Bytes | SHA-256 |
| --- | ---: | --- |
| [`docs/COMMON_CONTROL_MODEL_V1.md`](snapshot/docs/COMMON_CONTROL_MODEL_V1.md) | 113347 | `7a46f9fffe706476de458aac078d0af1c94844df339248d3f9f4b5cf033011d7` |
| [`docs/TUNER_NATIVE_API_V1.md`](snapshot/docs/TUNER_NATIVE_API_V1.md) | 66310 | `0405e1844d194406f7a150568835e3bf1fda73ddb5ef18d434870f4458c0bb08` |
| [`docs/TUNER_REQUIREMENTS_FROM_REMOTE.md`](snapshot/docs/TUNER_REQUIREMENTS_FROM_REMOTE.md) | 36321 | `fc6303f73c231e3abad91171ce0ea29ad05afe2b4c27833c5bd8743f79246c12` |
| [`docs/CONTROL_ARCHITECTURE.md`](snapshot/docs/CONTROL_ARCHITECTURE.md) | 57559 | `bd5094d5df626abef6c3ab8c1cd547168e7dfb3c99030d23ed9b060848da1c56` |
| [`docs/REMOTE01_PRODUCT_DECISIONS.md`](snapshot/docs/REMOTE01_PRODUCT_DECISIONS.md) | 14644 | `e99b042dae494bdf8eee89d882e326cf59b134f6fcd64a201b7d85528b440d49` |
| [`docs/COMMON_CONTROL_MODEL_V1_FREEZE_REVIEW.md`](snapshot/docs/COMMON_CONTROL_MODEL_V1_FREEZE_REVIEW.md) | 23260 | `e1d9c0706a707c181f5d5674ef531a614cd4906e9495af8ed74b48b17b3d1297` |
| [`docs/COMMON_CONTROL_MODEL_V1_CORRECTION_REVIEW.md`](snapshot/docs/COMMON_CONTROL_MODEL_V1_CORRECTION_REVIEW.md) | 31404 | `dcb434f86ab5661c9db1fee1a0f414b608943470d04247f9538b8c1ca4602d18` |
| [`docs/COMMON_CONTROL_MODEL_V1_CANDIDATE_3_FREEZE_REVIEW.md`](snapshot/docs/COMMON_CONTROL_MODEL_V1_CANDIDATE_3_FREEZE_REVIEW.md) | 10186 | `9e67c6f6933c6797ea5c413691e90a9e64a67b0c48dcbcab1f159a311115d283` |
| [`docs/COMMON_CONTROL_MODEL_V1_CANDIDATE_4_FREEZE_REVIEW.md`](snapshot/docs/COMMON_CONTROL_MODEL_V1_CANDIDATE_4_FREEZE_REVIEW.md) | 28513 | `cd91a00164dc1f1f19cc6da4a9bedaa6b93eb1480ecc42b38087e8840ce24044` |
| [`docs/UNIVERSAL_CONTROL_CORE_V1_IMPLEMENTATION.md`](snapshot/docs/UNIVERSAL_CONTROL_CORE_V1_IMPLEMENTATION.md) | 39064 | `f8f67e855b9bdbf23ff1dc2867a5cd550152060c6d3eff79ef0ea60ea6e2f246` |
| [`docs/PHASE_D_GENERIC_ADAPTER_BOUNDARY.md`](snapshot/docs/PHASE_D_GENERIC_ADAPTER_BOUNDARY.md) | 31572 | `59fb955e0d5fa02882669b38e53577ce66340a850b2f92a3575ac3a59429b4b2` |
| [`docs/STAGE_2B_2_POWER_STACK_PATH_MEASUREMENT.md`](snapshot/docs/STAGE_2B_2_POWER_STACK_PATH_MEASUREMENT.md) | 40854 | `012c0efc24fa9a46844307fa83c80a4f77d38204e9bba71a89f63a87c73d9a91` |
| [`docs/SYSTEM_SLEEP_CURRENT_AUDIT.md`](snapshot/docs/SYSTEM_SLEEP_CURRENT_AUDIT.md) | 37848 | `2aeb479f0d3a722e9c831b042bf8ca93437b248294cb4677905ed8c6c55d2491` |
| [`docs/SYSTEM_SLEEP_NETWORK_IMPLEMENTATION.md`](snapshot/docs/SYSTEM_SLEEP_NETWORK_IMPLEMENTATION.md) | 16376 | `63f756e38dc82c64f5d506d1120d2c43480342113e5425111452eed49cf329ff` |
| [`docs/GPIO1_EXTERNAL_POWER_SENSING.md`](snapshot/docs/GPIO1_EXTERNAL_POWER_SENSING.md) | 18558 | `86971fcc9aba37e19f2a04e32d945285b237dd6b4b5e0da5f3696882734d7ccb` |
| [`docs/REMOTE01_COMPLETION_ROADMAP.md`](snapshot/docs/REMOTE01_COMPLETION_ROADMAP.md) | 72620 | `aa0eece918d84492b241d8a59095ca00f746fda1a1a9d814fb52dc4209d6a8e9` |
| [`CHANGELOG.md`](snapshot/CHANGELOG.md) | 132636 | `6c566cfd6fa798938690fcc982d53b781da7723f44c87722a6cecd54ec3fbe3d` |
| [`platformio.ini`](snapshot/platformio.ini) | 429 | `e455b728cecf0d72d391e7bb841e8795ce899c7af85a0ed64e15db67d0c9f175` |
| [`partitions.csv`](snapshot/partitions.csv) | 404 | `fb9b79c3f9b92f43633569e6159e4d0522f0e4289b4e081d864cc4587ce496fc` |
| [`sdkconfig.defaults`](snapshot/sdkconfig.defaults) | 1089 | `08c722635f0271dc2cb3fbd898d9189b02cdcdc3f87e114093fd6e861dabb883` |
| [`components/control/core.cpp`](snapshot/components/control/core.cpp) | 82181 | `b0e37fa24fcbd7d81ff0f3fc2e9739ea0f4f1df4b494a364e4c23c0aff066413` |
| [`components/control/ingress.cpp`](snapshot/components/control/ingress.cpp) | 20913 | `0093272f5a2f274eeb26c5425a841e662a96e37d904293f146d995a672afe86b` |
| [`components/control/include/control/core.hpp`](snapshot/components/control/include/control/core.hpp) | 7778 | `8c2e46b3e6a76261104c706f22f4abf5bc1746433cba7770d121b3ae5f00db21` |
| [`components/control/include/control/model.hpp`](snapshot/components/control/include/control/model.hpp) | 17471 | `97b46b13b274e0f41b1c1c333fa64b9fe09ec25a2118accc9cad329218cdcf99` |
| [`components/control/include/control/storage.hpp`](snapshot/components/control/include/control/storage.hpp) | 8087 | `de8b3a189fb6bb2ec49fc5562a8f5f6a5cdfc290fc0a4f278b2b8435c25eab07` |
| [`components/control/include/control/ingress.hpp`](snapshot/components/control/include/control/ingress.hpp) | 6742 | `e102d5bb7680843c1e6fafa935aa129b52ba17c79f7360ac7f67b63a3f6f84c9` |
| [`components/control/include/control/mock_adapter.hpp`](snapshot/components/control/include/control/mock_adapter.hpp) | 1499 | `48da2641acb1e917b413bc916f77520f24fc4e547fd1792141c5d8a108cd1d99` |
| [`components/control_home/runtime.cpp`](snapshot/components/control_home/runtime.cpp) | 12213 | `6c43e02cffae19ea76733c06893ab471c593ffd0cd7aed5bb8ea9fa792fc91b9` |
| [`components/control_home/development.cpp`](snapshot/components/control_home/development.cpp) | 8279 | `94ce07bbad18f2e91c367118718c294d346b332f627a0f19f8b2fbcfb5f3cac6` |
| [`components/control_home/facade.cpp`](snapshot/components/control_home/facade.cpp) | 5367 | `fd10ab46fcaf0d85c54e5a0b4f96f53dc726e5b383db5fb45cf708ea9ad20f88` |
| [`components/control_home/include/control_home/development.hpp`](snapshot/components/control_home/include/control_home/development.hpp) | 3504 | `eebaec5c0851508b74b081b27a413a8dafb82b305707c6cee02df23f2ca6054f` |
| [`components/control_home/include/control_home/power_suspend.hpp`](snapshot/components/control_home/include/control_home/power_suspend.hpp) | 1919 | `08f3ac052954c814c7fee4e58207ff2d4059d458b83a5136f65a5841346ac680` |
| [`components/control_home/include/control_home/facade.hpp`](snapshot/components/control_home/include/control_home/facade.hpp) | 714 | `5de8ccc70ba466eccd4b4c0bac196299c236a88fbd21cc167579e26cac32454f` |
| [`components/power_management/runtime.cpp`](snapshot/components/power_management/runtime.cpp) | 27335 | `bb15530f50579382cdc86c458222508412726131175de4d61246f290608ee7f1` |
| [`components/power_management/hardware.cpp`](snapshot/components/power_management/hardware.cpp) | 5727 | `dedf3754397f8571dac1b02845bb2046b13887b5381f1a2459867bcf6712c523` |
| [`components/power_management/model.cpp`](snapshot/components/power_management/model.cpp) | 2464 | `cf83e8e27b72cfebc9debd5abb3ec72053aad8ff758678342d683154d370f12f` |
| [`components/network_manager/runtime.cpp`](snapshot/components/network_manager/runtime.cpp) | 28527 | `869b6b0dd77a40dd20f71d11c781be94babae8a206ac4a0f6ba61ad9f434ef39` |
| [`components/network_manager/include/network_manager/sleep.hpp`](snapshot/components/network_manager/include/network_manager/sleep.hpp) | 3086 | `e037ea26371b526b2468de8a7bf8f69db4fd37737e7e44856fe940b1ce0700ef` |
| [`components/user_app/user_app.cpp`](snapshot/components/user_app/user_app.cpp) | 12991 | `620b116e848ef8c98c80edb603483c206812fe10d44d992686c2f8b40a0d91a0` |
| [`main/main.cpp`](snapshot/main/main.cpp) | 13264 | `da1db6329e2b07b5396beb414f4314398d7fdfd3bad7388d8b3597084d073075` |
| [`CMakeLists.txt`](snapshot/CMakeLists.txt) | 528 | `c02762f0c1b98608697e850c6143b9ac94b77e08d95d22c1ff6a0e6c59720d25` |
