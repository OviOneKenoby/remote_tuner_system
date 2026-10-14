# A-REMOTE-011 Stage 5 include-path correction result

Date: 2026-10-14

Verdict: **FAIL — THE AUTHORIZED PRODUCTION BUILD RETAINED THE ORIGINAL HEADER-RESOLUTION ERROR.**

The private source contains `physical_input/model.hpp` under the workspace-level shared `include` tree. The narrow correction registered that tree as a header-only ESP-IDF component and declared `physical_input` as a private dependency of `user_app`. No absolute path, global include directory, encoder logic, GPIO assignment or protocol behavior was changed.

Exactly one production `remote01` build was run after the correction. PlatformIO selected Espressif32 6.13.0 and ESP-IDF 5.5.3, entered release compilation, and failed while compiling `components/user_app/user_app.cpp`. The diagnostic remained:

`fatal error: physical_input/model.hpp: No such file or directory`

No distinct compiler failure appeared. Per the owner instruction, work stopped without another correction or build. Previously passing encoder and quadrature tests were not rerun because their code did not change.

Private build-integration files changed:

- added `components/physical_input/CMakeLists.txt`;
- added `physical_input` to `components/user_app/CMakeLists.txt` private requirements.

No firmware artifact was produced, so firmware size, SHA-256 and OTA headroom remain unavailable. No TUNER modification, GPIO remap, hardware access, flash operation, live RTCP command, pairing/NVS mutation or protocol change occurred. PR #17 remains open and unmerged.

The remaining issue is confined to ESP-IDF/PlatformIO component discovery or propagation of the new header-only component. Any further correction and build require a new owner decision.
