# A-REMOTE-010 Stage 7 restoration preparation

Recorded UTC: 2026-10-13T15:03:05Z. Input commit `009698dc618858365a0c4cc267bbca1bff478b22`; [owner decision](../references/A010_OWNER_ACCEPTANCE_AND_CLOSURE_PREPARATION_2026-10-13.md); [sanitized evidence](../references/device_evidence/remote/A-REMOTE-010/STAGE7_PREPARATION.json).

**READY / NOT AUTHORIZED — STOPPED BEFORE FLASHING.**

The retained private prior-byte restore span was reverified offline at 2,506,752 bytes (`0x264000`) and SHA-256 `57736494ea726600c68e25ae6a8f5b3bd109f5e5c1d5d858a05afd7ee8603aca`. It is byte-identical to the slice at offset `0x10000`, length `0x264000`, of the verified 16 MiB pre-A009 recovery backup, whose SHA-256 remains `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`. Its 2,485,824-byte factory-image prefix retains the accepted pre-A010 installed identity SHA-256 `7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb`.

The prepared write begins at `0x10000` and ends at `0x273FFF`, using flash mode, frequency and size `keep`. It supplies only the verified restore-span file. It cannot overlap the partition table, default NVS, OTA metadata, OTA images or `remote_ctl`; the dedicated partition begins at `0xE20000`. Generation 2 and both test records therefore remain present and are intentionally not erased. After a separately authorized write, the full span must be read back and match the restore SHA-256 before one normal boot verification.

The exact operation, when separately authorized, is equivalent to:

`esptool.py --chip esp32s3 --port <VERIFIED_COM> --baud 115200 write_flash --flash_mode keep --flash_freq keep --flash_size keep 0x10000 <PRIVATE_VERIFIED_RESTORE_SPAN>`

No hardware access, reset, flash write, erase, source change or PR merge occurred during preparation. A final closure report and merge recommendation will be prepared only after restoration and owner confirmation of the original firmware, UI and configuration. A-REMOTE-011 remains not started.
