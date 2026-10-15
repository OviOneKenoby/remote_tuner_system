# REMOTE//01 motion-wake runtime diagnosis

Date: 2026-10-15

Verdict: **FAIL — CURRENT BOOT HAS THE IMU MOTION PATH DISABLED.**

The currently running REMOTE was reached through the retained verified private LAN association and its existing read-only `/api/status` interface. Exactly one HTTP GET captured snapshot A before any requested movement. The complete private response was preserved and hashed; no address, network identity or device identifier is published.

Snapshot A reported:

- power state: display idle (`1`);
- IMU readiness: false (`0`);
- motion events: `0`;
- wake count: `4`;
- I²C/bus errors: `0`;
- last sleep/wake cause: `0`;
- diagnostics age: 53 ms;
- private snapshot SHA-256: `9e75b3cfced0ca12125f3302890d3931ef68f9dcb9b7252d75e87c901aea4af3`.

The mandatory stop condition applied immediately. No lift was requested and snapshot B was not taken.

The failure is classified at IMU wake-on-motion initialization for the current boot. In this implementation, failed boot initialization leaves `imu_ready=false` without incrementing the runtime bus-error counter. A later QMI status-read failure would increment that counter before disabling the IMU path. The observed `IMU=0` with `bus_errors=0` therefore supports boot initialization failure, rather than motion-event detection or wake/display handling. The exact failed QMI transaction or acknowledgement stage is not available from the runtime snapshot.

The minimum next verification is one separately authorized passive UART capture during an owner-performed normal reboot. The existing `POWER_WOM` boot summary will identify the failed stage, operation, register, expected/actual value and transport error without adding instrumentation or issuing a device command.

No reboot, movement request, source change, build, test, flash access, NVS/configuration write or control command occurred. PR #17 remains open and unmerged.
