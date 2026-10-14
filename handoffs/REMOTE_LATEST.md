# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-STAGE5-GPIO-RESOLUTION-20261014
- Updated (UTC): 2026-10-14
- Task ID: A-REMOTE-011
- Status: STAGE 5 GPIO PROPOSAL READY -- OWNER WIRING APPROVAL REQUIRED
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `d4123f5e2baed4b0c3649d1ad1d87627a810fbda`

## Result

The official Waveshare V2 schematic/interface table, ESP32-S3 strapping rules and current production source were reconciled into `docs/REMOTE_GPIO_MAP.md`. GPIO1 remains occupied by external-power sensing and GPIO4 by `BAT_ADC`. GPIO0 and GPIO3 are exposed on J6 but are strapping pins. All LCD, touch, shared interrupt, power, USB, UART, system-I2C, SD and onboard audio nets remain reserved.

The preferred encoder proposal is:

- A/CLK: GPIO2 at J6-3;
- B/DT: GPIO5 at J6-6;
- common: GND at J6-9;
- input-only with internal 3.3 V pull-ups;
- push button not connected.

GPIO2 and GPIO5 are direct MCU expansion breakouts with no other V2 schematic load, current production claim or strapping role. This is an owner-selected proposal pending physical wiring approval. The owner must confirm J6 pin-1 orientation before soldering. Direction and transitions per detent remain later commissioning observations.

Stage 4 remains PASS. The rejected GPIO4/GPIO5 transient candidate remains non-deployable and its source edits remain reverted.

## Scope guard

No production source was edited. No test, build, device access, firmware flash, live command, pairing/NVS change or wiring operation occurred. Private source and binaries remain private. PR #17 remains open and unmerged.

## Next owner decision

Approve or reject the exact GPIO2/J6-3 A, GPIO5/J6-6 B and J6-9 GND wiring. Implementation must not resume until that decision is explicit.

## Evidence

- `docs/REMOTE_GPIO_MAP.md`
- `reports/A-REMOTE-011_STAGE5_GPIO_RESOLUTION.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_GPIO_RESOLUTION.json`
- Historical conflict: `reports/A-REMOTE-011_STAGE5_ENCODER_GPIO_CONFLICT.md`
- Historical control stop: `reports/A-REMOTE-011_STAGE5_CONTROL_STOP.md`
- Stage 4 completion: `reports/A-REMOTE-011_STAGE4_COMPLETE.md`