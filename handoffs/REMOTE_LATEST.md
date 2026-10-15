# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-STAGE5-BUTTON-INPUT-20261015
- Updated (UTC): 2026-10-15
- Task ID: A-REMOTE-011
- Status: STAGE 5 BUTTON INPUT IMPLEMENTATION BUILD PASS -- HARDWARE COMMISSIONING NOT STARTED
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `9df28bbee2b0d567537fe13bd376dd132f3516f6`

## Result

The owner permanently excluded microSD functionality and approved GPIO38/J3-8, GPIO39/J3-9, GPIO40/J3-10 and GPIO41/J3-11 as input-only active-low physical buttons using the board's fitted 10 kOhm pull-ups. The socket must remain empty and SDMMC/SDSPI initialization and card mounting remain prohibited.

The private REMOTE source now exposes four typed logical press identities: `ENCODER_KEY`, `BUTTON_1`, `BUTTON_2` and `BUTTON_3`. A fixed 20 ms debounce produces one event per press and no repeat while held. Boot-held inputs produce no unsolicited event. The runtime handler intentionally assigns no application action and dispatches no CCM/RTCP command. The existing GPIO2/GPIO5 encoder volume path remains intact; GPIO1, GPIO4 and GPIO8 behavior is unchanged.

Focused button checks passed 3/3 with 10 assertions. The affected shared physical-input suite passed 19/19 with 24,627 assertions, 1,000 cycles and zero allocations. GPIO ownership checks confirmed input-only configuration, custom SD-component exclusion and zero selected application SD initialization references.

One clean `remote01` build passed. The private application is 2,518,896 bytes with SHA-256 `6aca8931fcd08b91fcf489bd6d77212cbb0d4c762e70a657d7abec6911ab8e95`; each unchanged 3 MiB OTA slot retains 626,832 bytes of headroom. PlatformIO reported 47,172 bytes static RAM use and 2,518,401 bytes flash use.

## Scope guard

No hardware access, flash operation, NVS/pairing change, TUNER change, CCM/RTCP semantic change, button action assignment, private source/binary publication or PR merge occurred. The wiring remains owner-approved but physically unverified. PR #17 remains open and unmerged.

## Next owner decision

Authorize or reject hardware installation and commissioning of the Stage 5 candidate. Commissioning should verify J3 orientation, idle-high inputs, each independent identity, debounce/no-repeat behavior and ordinary UI, touch, encoder, motion-wake and sleep operation. Firmware flashing remains separately gated.

## Evidence

- `docs/REMOTE_GPIO_MAP.md`
- `reports/A-REMOTE-011_STAGE5_BUTTON_INPUT_IMPLEMENTATION.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_BUTTON_INPUT_IMPLEMENTATION.json`
- Prior electrical investigation: `reports/A-REMOTE-011_SD_GPIO_BUTTON_REUSE.md`
