# A-REMOTE-011 Stage 5 encoder GPIO conflict

Date: 2026-10-14

Verdict: **BLOCKED — GPIO4 is an active battery-sense input; no deployable firmware candidate was produced.**

## Owner hardware decision checked

The owner selected GPIO4 for encoder A/CLK and GPIO5 for encoder B/DT, with the encoder common connected to ground and internal 3.3 V input pull-ups. GPIO1 remains reserved and must not be changed.

The board identity is Waveshare ESP32-S3-Touch-LCD-3.49B V2, PCB Rev1.1. Waveshare's official V2 schematic labels IO4 as `BAT_ADC`. The active private firmware independently confirms the same assignment: its power-management board uses ADC1 channel 3 for the main battery input, asserts that ADC1 channel 3 maps to GPIO4, and samples that channel during normal operation. GPIO1 is separately asserted as ADC1 channel 0 and used for external-power sensing. GPIO5 had no direct active-firmware claim in the inspected tree, but the requested A/B pair is invalid because GPIO4 is already claimed.

Configuring GPIO4 with an encoder pull-up would electrically interfere with the battery divider and change an active firmware input. The strict conflict condition therefore applies. The implementation must not silently remap the pin or disable battery sensing.

Official references:

- [Waveshare board resources and V2/PCB Rev1.1 identification](https://docs.waveshare.com/ESP32-S3-Touch-LCD-3.49/Resources-And-Documents)
- [Waveshare V2 schematic](https://github.com/waveshareteam/ESP32-S3-Touch-LCD-3.49-V2/blob/main/schematic/ESP32-S3-Touch-LCD-3.49%20V2.pdf)

## Bounded implementation experiment

Before the schematic conflict was confirmed, a private transient candidate connected the existing quadrature decoder to a bounded HOME-only volume-intent route with READY/capability/bounds/single-in-flight gates. Focused results were:

- encoder decoding and intent routing: 5/5 PASS, 31 assertions;
- existing quadrature stress suite: 19/19 PASS, 21,621 assertions and zero allocations;
- one production build: PASS.

The transient image was 2,518,640 bytes, SHA-256 `735b07feeb2705110a2f4b4482283ebbb3a6c148cacff069d89f2da341462f03`. Against the unchanged 3,145,728-byte OTA application slot, the raw image headroom was 627,088 bytes. This image is **rejected and non-deployable** because it assumes the conflicting GPIO4 assignment. It remains private and must not be flashed.

All transient source edits were reverted after the conflict was found. The production private source has no Stage 5 encoder changes. No valid firmware size or hash exists for this requested pin assignment.

## Scope and result

- GPIO4/GPIO5 were not enabled on hardware.
- GPIO1 and battery sensing were not changed.
- No hardware access, flash write, live `volume.set`, pairing change or NVS mutation occurred.
- TUNER and CCM/RTCP semantics were not changed.
- PR #17 remains open and unmerged.

## Required owner decision

Select an alternative encoder CLK GPIO that is verified free on the PCB and in the active firmware, or explicitly authorize a hardware/firmware redesign of the battery-sense function. GPIO5 may remain a candidate only after the complete replacement pair is verified. Implementation and physical commissioning remain stopped until that decision is provided.
