# A-REMOTE-010 Stage 4 recovery continuation stop

Recorded UTC: 2026-10-13T08:33:00Z. Stage input `cc660e417b73f0aae29d50866bacb990c80eee90`; [owner authorization](../references/A010_STAGE4_RECOVERY_CONTINUATION_OWNER_AUTHORIZATION_2026-10-13.md); [protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md); [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE4_RECOVERY_CONTINUATION_STOP.json).

**STOPPED — THE AUTHORIZED RESET ENTERED ESP32-S3 ROM DOWNLOAD MODE; NORMAL BOOT WAS NOT CONFIRMED; `RECOVER` WAS NOT SENT.** Stage 4 remains incomplete.

COM3 opened successfully for an initial five-second passive check, but no bytes were emitted. That proved the serial connection was available but could not establish normal runtime or whether the earlier reset had occurred. The continuation therefore used its one authorized reset while capturing serial output.

The reset produced exactly one `ESP-ROM:esp32s3-20210327` banner with reset reason `USB_UART_CHIP_RESET`, boot mode `DOWNLOAD(USB/UART0)` and `waiting for download`. The normal `A010_VALIDATION` identity did not appear within 20 seconds. The guard requiring confirmed normal boot before recovery inspection applied, so `!A010 RECOVER` was not transmitted.

The 152-byte private capture has SHA-256 `ac99e9c9fca775238cfd74483f79a86d666f432f510790e59b18dd5a36c2e15f` and is not published. No payload, private path, MAC or source is included in public evidence.

`INIT` was not repeated. No `COMMIT1`, `COMMIT2`, `ERASE`, flash write or source-code change occurred. The device was left in ROM download mode. Normal UI/configuration and post-reboot persistence recovery remain NOT VERIFIED. The last directly verified persistence state remains initialized-empty generation 0/next 1 from the immediate pre-reset Stage 4 status.

A new owner decision is required for one normal hard reset out of ROM download mode, confirmation of the A010 application boot and UI/configuration, followed by exactly one read-only `!A010 RECOVER`. Stage 5 remains prohibited.
