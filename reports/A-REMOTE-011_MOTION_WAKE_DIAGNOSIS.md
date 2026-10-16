# REMOTE//01 motion-wake regression diagnosis

Date: 2026-10-15

Verdict: **NO A-REMOTE-011 SOURCE REGRESSION DEMONSTRATED; CURRENT RUNTIME STATE REQUIRED.**

## Confirmed source findings

The active A-011 production source was compared with the preserved A-010 reconciliation source, the A-011 Phase 2 source and the pre-promotion active-workspace backup. The relevant power runtime, IMU access, board initialization, wake-cycle, GPIO-expander setup and pin-configuration files are byte-identical. The main power runtime, IMU hardware layer, state model and board initialization are also byte-identical to the published A-REMOTE-001 snapshot associated with the earlier owner motion-wake PASS. Stage 5 encoder changes do not touch this path, and the Stage 5 firmware has not been installed.

Motion wake remains enabled in the source. At boot, POWER configures the QMI8658 at I²C address `0x6B` for wake-on-motion at 200 mg and approximately 21 Hz, maps the event to IMU INT1, and reads QMI `STATUS1` bit `0x04` to acknowledge and classify motion. On the V2 Rev1.1 board, IMU INT1 reaches TCA9554 input EXIO2; the expander's shared active-low interrupt reaches ESP32-S3 GPIO8. Awake operation uses a GPIO8 falling-edge ISR and also polls every two seconds. Before light sleep, the runtime masks the edge interrupt, arms GPIO8 as a low-level GPIO wake source, enters light sleep, then disarms the wake source and restores falling-edge operation. Touch and motion share the expander interrupt, so the TCA input read and QMI status read distinguish their source.

The routing agrees with the official Waveshare V2 schematic and resources: Rev1.1 identifies V2; QMI8658 is the IMU; INT1 is routed through EXIO2/TCA9554; and V2 places the shared expander interrupt on GPIO8. The production configuration sets EXIO2 and EXIO3 as inputs and retains the SYS_EN power hold on EXIO6.

## Specific weakness and historical evidence

QMI wake-on-motion initialization is attempted exactly once per boot. If any identity, reset, command-acknowledgement, register-write or readback step fails, `imu_ready` becomes false. A later QMI status-read failure also clears `imu_ready`. Either event disables `sleep_hardware` for the remainder of that boot; there is no bounded reinitialization attempt. This is a confirmed recovery limitation, not proof that it caused the current report.

Historical project evidence records the same externally visible condition on earlier firmware: `IMU_WOM=0`, `sleep_ready=0` and failed lift wake after one boot, followed by restored physical lift wake after a software reboot. Later instrumentation recorded successful initialization and repeated lift wake, while the exact cause of the failed boot remained unknown. The current A-011 source preserves that implementation byte-for-byte, so the last known working behavior predates A-011 and an A-011 code regression is not supported.

## Minimum next verification

The smallest safe observation is two read-only diagnostics snapshots from the currently running device: one before movement and one immediately after a deliberate lift. Record only power state, `IMU`, motion count, wake count, bus-error count and last sleep cause.

- `IMU=0` confirms that the current boot has disabled the motion path. A passive boot-log capture on one separately authorized normal reboot would then identify the exact failed QMI stage from the existing `POWER_WOM` summary.
- `IMU=1` with an increasing motion count but no display wake isolates the problem after sensor detection, in state/display wake handling.
- `IMU=1` with no motion-count change isolates the problem to QMI event generation, INT1/expander routing or status acquisition; one read-only GPIO8/TCA/QMI observation would then be the next bounded step.

No source edit, build, test, device access, reset, flash, NVS/configuration write or control command was performed. PR #17 remains open and unmerged.

## Public hardware sources

- [Waveshare V2 resources and Rev1.1 identification](https://docs.waveshare.com/ESP32-S3-Touch-LCD-3.49/Resources-And-Documents)
- [Official Waveshare V2 schematic repository](https://github.com/waveshareteam/ESP32-S3-Touch-LCD-3.49-V2/tree/main/schematic)
- [QMI8658 datasheet linked by Waveshare](https://files.waveshare.com/wiki/common/QMI8658A_Datasheet_Rev_A.pdf)
