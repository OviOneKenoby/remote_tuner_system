# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-SD-GPIO-BUTTON-REUSE-20261015
- Updated (UTC): 2026-10-15
- Task ID: A-REMOTE-011
- Status: SD GPIO BUTTON REUSE VERIFIED WITH CONDITIONS -- OWNER WIRING APPROVAL PENDING
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `c80b79268aabbfaef00c737a7a5da250ed3f6b1f`

## Result

The official Waveshare V2 schematic shows GPIO38/J3-8 SD CS/D3, GPIO39/J3-9 SD CMD, GPIO40/J3-10 SD DAT0 and GPIO41/J3-11 SD CLK. Each signal has a fitted 10 kOhm pull-up to 3.3 V. The optional R27 SD_CS-to-GND link and DAT1/DAT2 pull-up positions are unpopulated.

The active private application defines these board pins but does not initialize SDMMC/SDSPI or mount a card. Custom `sdcard_bsp` and `codec_board` components are excluded. Framework SD libraries in dependency metadata do not create a runtime claim on the pins. GPIO38-41 are not boot strapping pins, and current light-sleep wake uses GPIO8 only.

All four proposed button GPIOs are **SAFE WITH CONDITIONS**: the microSD socket must remain empty, SD support must remain disabled, and the GPIOs must be input-only active-low contacts to GND. The fitted 10 kOhm pull-ups already provide the released-high state. The buttons will not wake the device under the current power design. Inserting a card while these buttons are connected is prohibited because both would share active SD nets.

Proposed wiring pending owner approval: encoder KEY GPIO38/J3-8; Button 1 GPIO39/J3-9; Button 2 GPIO40/J3-10; Button 3 GPIO41/J3-11; common GND preferably J3-3. Existing encoder A GPIO2/J6-3, B GPIO5/J6-6 and common J6-9 remain unchanged. GPIO1 external-power sensing and GPIO4 `BAT_ADC` remain unchanged. No button actions are assigned.

## Scope guard

This was a read-only investigation. No private source implementation, build, test, flash operation, hardware access, TUNER change, encoder-routing change, pairing/NVS mutation, protocol change or PR merge occurred. PR #17 remains open and unmerged.

## Next owner decision

Approve or reject the proposed four-button wiring and the permanent no-microSD condition. Button actions and any wake behavior require separate scope.

## Evidence

- `docs/REMOTE_GPIO_MAP.md`
- `reports/A-REMOTE-011_SD_GPIO_BUTTON_REUSE.md`
- `references/device_evidence/remote/A-REMOTE-011/SD_GPIO_BUTTON_REUSE.json`
- Official Waveshare V2 schematic SHA-256: `fc82f639dec6ecf9644634c4eba48fff52d9143d62f60aae6d83e9505b9469bf`
