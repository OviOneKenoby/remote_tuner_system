# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-STAGE5-ENCODER-GPIO-CONFLICT-20261014
- Updated (UTC): 2026-10-14
- Task ID: A-REMOTE-011
- Status: STAGE 5 BLOCKED -- GPIO4 CONFLICTS WITH ACTIVE BATTERY SENSING
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `4864eba87e46677d58ac5e5e5e0fff4c9aaba6c8`

## Result

The owner selected GPIO4 for encoder CLK and GPIO5 for DT on Waveshare ESP32-S3-Touch-LCD-3.49B V2 PCB Rev1.1, while reserving GPIO1. Hardware and source verification found a real conflict: the official schematic labels IO4 `BAT_ADC`; the active private firmware samples its main-battery divider on ADC1 channel 3 and asserts that this channel maps to GPIO4. GPIO1 separately remains ADC1 channel 0 for external-power sensing. GPIO5 had no direct active-source claim, but the requested pair cannot be enabled.

A bounded transient private encoder-to-volume implementation passed focused tests and a production build. Its image is explicitly rejected and non-deployable because it assumes the conflicting GPIO4 assignment. All transient source edits were reverted, leaving no Stage 5 change in the production private source.

Stage 4 remains PASS. Both production devices remain paired and synchronized, and zero `volume.set` commands have been dispatched.

## Scope guard

No device was accessed. No firmware was flashed. No live control command, pairing/NVS change, GPIO remap, battery-sense change, TUNER change or contract change occurred. Private source and binaries remain private. PR #17 remains open and unmerged.

## Next owner decision

Choose an alternative encoder CLK GPIO verified free on this PCB and in the active firmware, or explicitly authorize redesign of the battery-sense function. GPIO5 can remain a candidate only after the complete replacement pair is checked. No firmware installation or physical encoder test is ready for authorization.

## Evidence

- `reports/A-REMOTE-011_STAGE5_ENCODER_GPIO_CONFLICT.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_ENCODER_GPIO_CONFLICT.json`
- Historical routing blocker: `reports/A-REMOTE-011_STAGE5_ENCODER_ROUTING_BLOCKER.md`
- Historical control stop: `reports/A-REMOTE-011_STAGE5_CONTROL_STOP.md`
- Stage 4 completion: `reports/A-REMOTE-011_STAGE4_COMPLETE.md`
