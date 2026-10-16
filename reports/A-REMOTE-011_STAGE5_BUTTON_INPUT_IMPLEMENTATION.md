# A-REMOTE-011 Stage 5 physical button input implementation

Date: 2026-10-15

## Result

PASS for private source implementation and build verification. The owner-approved GPIO38-41 inputs now produce four typed logical press identities with bounded 20 ms debounce and no held-button repeat. No application action or CCM/RTCP command is assigned to any button.

The existing GPIO2/GPIO5 encoder volume path remains intact. GPIO1 external-power sensing, GPIO4 battery sensing and GPIO8 wake behavior are unchanged.

## Private source changes

- `include/physical_input/model.hpp`: increased the fixed button model from three to four inputs while retaining its fixed queue and allocation-free operation.
- `components/user_app/button_inputs.hpp`: added the typed `ENCODER_KEY`, `BUTTON_1`, `BUTTON_2` and `BUTTON_3` router.
- `components/user_app/user_app.cpp`: configured GPIO38-41 as input-only, sampled active-low levels in the existing input task and routed typed events to an intentionally unassigned handler.
- `tests/control/button_input_tests.cpp`: added focused identity, debounce, held-state and boot-held checks.
- `tests/control/physical_input_tests.cpp`: updated the affected shared-model expectations for four buttons.

Private source and firmware binaries were not published.

## Verification

| Check | Result |
| --- | --- |
| Focused button routing | 3/3 PASS, 10 assertions |
| Affected shared physical-input model | 19/19 PASS, 24,627 assertions, 1,000 cycles, zero allocations |
| GPIO/SD ownership check | PASS: input-only GPIO38-41, custom SD components excluded, zero selected application SD-init references |
| Clean production `remote01` build | PASS |

The normal production build generated a 2,518,896-byte application with SHA-256 `6aca8931fcd08b91fcf489bd6d77212cbb0d4c762e70a657d7abec6911ab8e95`. Each unchanged 3 MiB OTA slot retains 626,832 bytes of headroom. PlatformIO reported 47,172 bytes of static RAM use and 2,518,401 bytes of flash use.

The generated application ELF contains no linked `sdmmc_host_init`, `sdspi_host_init`, `esp_vfs_fat_sd*` or `mount_sdcard` symbol. ESP-IDF framework archives may still be built as dependencies, but production application initialization does not acquire the pins.

Previously passing encoder-volume, pairing and RTCP suites were not repeated. The shared physical-input suite was rerun because its fixed button count changed.

## Permanent constraint and remaining commissioning

MicroSD functionality is permanently excluded from this project configuration. The socket must remain empty, GPIO38-41 must remain input-only, and production code must never initialize SDMMC/SDSPI or mount a card.

Hardware remains physically unverified. A separately authorized commissioning step must verify J3 orientation, idle-high electrical levels, each independent button identity, debounce behavior and absence of repeat while held. It must also confirm ordinary UI, touch, encoder, motion wake and sleep behavior. Firmware flashing and device access were outside this task.

No hardware access, flash operation, NVS/pairing change, TUNER change, protocol change or PR merge occurred.
