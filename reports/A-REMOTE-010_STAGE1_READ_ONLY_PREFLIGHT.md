# A-REMOTE-010 Stage 1 read-only hardware preflight

Recorded UTC: 2026-10-13T07:00:27Z. Candidate publication input `a1f7b3bb69b4bfa3823c3ba3c5a27c0958a4ab85`; [owner authorization](../references/A010_STAGE1_READ_ONLY_OWNER_AUTHORIZATION_2026-10-13.md); [protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md); [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE1_READ_ONLY_RESULT.json).

**PASS — STAGE 1 READ-ONLY PREFLIGHT COMPLETE. STOPPED BEFORE STAGE 2.**

The newly enumerated device was bound to COM3. Esptool 4.11.0 identified an ESP32-S3 QFN56 revision 0.2, a 40 MHz crystal, 8 MB embedded PSRAM, USB-Serial/JTAG ROM access and 16 MiB physical flash. The device-specific MAC was retained privately and is not published. ROM/USB recovery remains available without JTAG.

The complete 4 KiB sector at `0x8000` was read. Its first 3,072 bytes have SHA-256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184` and are byte-identical to the accepted A-009 partition image. The remaining 1,024 bytes are all `0xFF`. Independent ESP-IDF decoding produced exactly seven valid entries: the six accepted earlier entries remain unchanged, both 3 MiB OTA slots remain unchanged, and `remote_ctl` is data/NVS at `0xE20000` with size `0x10000`. Table verification found no overlap or bounds error.

The complete `0xE20000–0xE2FFFF` range was read. It is exactly 65,536 bytes, contains zero non-`0xFF` bytes, and has SHA-256 `71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063`. The dedicated partition therefore remains erased and uninitialized.

The accepted 2,485,824-byte factory-image range at `0x10000` was read. Its SHA-256 is `7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb`, an exact match to the accepted pre-A010 installed identity. Offline image inspection reported a valid image checksum and validation hash. This demonstrates installed-byte identity only; it does not claim private-source equivalence.

Only `chip_id`, `flash_id` and three `read_flash` operations were executed at 115200 baud. Esptool hard-reset the device after each successful operation. No firmware upload, flash write, erase, NVS initialization, partition mutation, serial diagnostic command or implementation change occurred. Raw reads, the MAC, private paths and logs remain private.

Stage 2 remains unauthorized and was not started. The next decision is whether to authorize the protocol's single candidate-firmware write at `0x10000`; every later `remote_ctl` mutation remains separately gated.
