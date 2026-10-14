# A-REMOTE-011 Stage 5 encoder implementation stop

Date: 2026-10-14

Verdict: **STOPPED AT THE FIRST PRODUCTION-BUILD FAILURE.**

The owner-approved GPIO2/J6-3 and GPIO5/J6-6 encoder path was implemented in the private REMOTE source. The implementation uses input-only GPIOs with internal pull-ups, the existing bounded quadrature model, HOME-only routing, the CCM `volume.set` admission path and the existing RTCP/1 adapter. It gates commands on a READY session, advertised capability, authoritative volume and bounds; permits one request in flight; clears pending intent on disconnect or session/capability change; and generates no command from the initial sampled level. GPIO1 external-power sensing and GPIO4 `BAT_ADC` were not changed.

Focused verification passed:

- encoder routing and volume admission: 5/5 cases, 25 assertions;
- existing quadrature model: 19/19 cases, 21,621 assertions, 1,000 randomized cycles, zero allocations.

The single clean production build stopped while compiling `user_app`. The component could not resolve `physical_input/model.hpp`; the shared header exists in the private source root, but that directory is absent from the component's ESP-IDF include path. The exact diagnostic was `fatal error: physical_input/model.hpp: No such file or directory`. Per the owner's stop condition, no include-path correction or second build was attempted.

Private files changed and retained for review:

- `include/physical_input/model.hpp`;
- `components/control_home/include/control_home/api.hpp`;
- `components/control_home/facade.cpp`;
- `components/control_home/include/control_home/rtcp_device.hpp`;
- `components/control_home/include/control_home/development.hpp`;
- `components/control_home/development.cpp`;
- `components/user_app/CMakeLists.txt`;
- `components/user_app/encoder_volume.hpp`;
- `components/user_app/user_app.cpp`;
- `tests/control/encoder_volume_tests.cpp`.

No deployable firmware was produced, so firmware size, SHA-256 and OTA headroom are unavailable. No hardware access, flash operation, pairing/NVS change or live `volume.set` occurred. TUNER and protocol semantics were unchanged. PR #17 remains open and unmerged.

The minimum next action is a narrow private build-integration correction that exposes the existing shared header to `user_app`, followed by the one production build. Hardware commissioning remains unauthorized.
