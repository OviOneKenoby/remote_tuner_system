# A-REMOTE-010 Stage 2 diagnostic firmware validation

Recorded UTC: 2026-10-13T07:19:42Z. Stage input `38a8f3b7fc1629f6cb4e60038a30737d83e5015c`; [owner authorization](../references/A010_STAGE2_FLASH_OWNER_AUTHORIZATION_2026-10-13.md); [protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md); [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE2_RESULT.json).

**PASS — EXACT DIAGNOSTIC FIRMWARE FLASHED AND FUNCTIONALLY BOOTED; STOPPED AFTER STAGE 2.**

Before the write, the private candidate was reverified as 2,503,936 bytes with SHA-256 `308181d4144494734fe8fae360938f74b9f886fb4c41bff0cba9b89427e4d248`. The retained 16 MiB recovery backup was reverified at SHA-256 `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`. COM3 reopened and identified the same ESP32-S3 revision 0.2 device.

Exactly one write command completed with exit code 0:

`esptool.py --chip esp32s3 --port COM3 --baud 115200 write_flash --flash_mode keep --flash_freq keep --flash_size keep 0x10000 <PRIVATE_CANDIDATE_FIRMWARE_BIN>`

Only the 2,503,936-byte application image was supplied, beginning at `0x10000`; its bytes end at `0x2734FF` and its erase/write sector span ends at `0x273FFF`. No bootloader, partition-table, default-NVS, OTA-data or `remote_ctl` image was supplied. Esptool reported successful data-hash verification.

An independent read of the complete 2,503,936-byte installed application produced the same SHA-256 and was byte-identical to the candidate. A single controlled boot produced the exact identity `build=A010_VALIDATION diagnostic=ENABLED persistence_on_boot=0`, with one boot banner and the factory application offset. The sanitized review found no panic, watchdog, partition error, abort, Guru Meditation or boot-loop evidence. The owner then confirmed that the display/UI appeared normal and the existing observable configuration remained present without changing settings.

Before any diagnostic command, the full 64 KiB `remote_ctl` region was independently read again. All 65,536 bytes remained `0xFF`, with SHA-256 `71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063`, exactly matching Stage 1. This confirms that booting the diagnostic candidate performed no persistence initialization or write.

Raw serial output, flash reads, firmware, backup, device MAC, private paths and source remain private. No `!A010` command was sent. `INIT`, `COMMIT1`, `COMMIT2`, `ERASE`, Stage 3 and all later stages were not executed. Rollback was not required. The installed physical firmware is now the exact diagnostic candidate; `remote_ctl` remains erased and uninitialized.
