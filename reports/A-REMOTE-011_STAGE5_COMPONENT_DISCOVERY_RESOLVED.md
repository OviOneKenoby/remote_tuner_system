# A-REMOTE-011 Stage 5 component-discovery resolution

Date: 2026-10-14

Verdict: **PASS — PRODUCTION BUILD SUCCEEDED.**

The private source and generated build metadata were inspected before further change. `physical_input/model.hpp` was present in the workspace-level shared include tree. Its header-only component registration and the `user_app` private dependency were correct, but the generated ESP-IDF project description did not contain a `physical_input` component and the generated `user_app` compile group did not contain the shared include directory. The failed builds had reused component-discovery metadata generated before the new component directory existed.

The demonstrated root cause was stale generated component metadata, rather than an incorrect header path or visibility declaration. The existing generated `remote01` build directory was preserved under a private sibling name, forcing PlatformIO to configure a fresh component graph. No additional source or CMake change was required. The regenerated graph contains the `physical_input` component and exposes the shared include directory to `user_app`.

Exactly one production build was run after that correction:

- environment: `remote01`;
- platform: Espressif32 6.13.0;
- framework: ESP-IDF 5.5.3;
- result: PASS in 150.28 seconds;
- reported static RAM use: 47,172 / 327,680 bytes (14.4%);
- reported flash use: 2,517,997 / 8,388,608 bytes (30.0%);
- application binary size: 2,518,496 bytes;
- application binary SHA-256: `58d09a4d7b39a287d80b48270b5236986657f27fb716692b77ff4af3e573cab7`;
- OTA slot size: 3,145,728 bytes;
- OTA headroom by application binary length: 627,232 bytes.

Previously passing encoder/admission and quadrature tests were not rerun because their relevant source did not change. The approved GPIO2/J6-3 and GPIO5/J6-6 assignments and all Stage 5 logic remain unchanged. No TUNER change, hardware access, firmware flash, live RTCP command, pairing/NVS mutation or protocol change occurred. The firmware artifact remains private. PR #17 remains open and unmerged.

Stage 5 is ready for a separately authorized, reversible REMOTE hardware commissioning step covering application-only installation, encoder direction/detent observation and at most one controlled volume change.
