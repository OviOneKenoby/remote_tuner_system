# A-REMOTE-009 table-only hardware validation

Recorded 2026-10-12T20:24:27.882825+00:00. Input `1e549d4d6be00c77d61c020adf0b82ed4a04e729`; [exact owner scope](../references/A009_TABLE_ONLY_WRITE_OWNER_AUTHORIZATION_2026-10-12.md); [sanitized checks/exit codes/hashes](../references/device_evidence/remote/A-REMOTE-009/TABLE_ONLY_HARDWARE_RESULT.json). **PASS — TABLE-ONLY HARDWARE VALIDATION; READY FOR OWNER REVIEW. PR15 OPEN / UNMERGED.** Earlier preparation/read-only reports remain historical evidence. No backend/API/A010 work.

## Before writing

Primary recovery backup reopened and rehashed:16777216bytes, SHA256 `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`. Candidate3072bytes/SHA256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`. Owner reports independently verified same-size/same-hash Orange Pi separate-storage copy; executor did not remotely access it. USB identity and ROM MAC matched private A007/A009 evidence before writing; ESP32-S3revisionv0.2/physical16MiB/securitydisabled, esptool4.11.0/115200. Exact COM3 used; unique MAC/USB serial remain unpublished. ROM-only identity/flash queries succeeded, no JTAG. Original table4096bytes independently saved privately; SHA256 `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46`, byte-identical to full backup and accepted baseline.

## Exact authorized operation

```text
python -B esptool.py --chip esp32s3 --port COM3 --baud 115200 --before no_reset --after no_reset write_flash --flash_mode keep --flash_freq keep --flash_size keep 0x8000 partitions.bin
```

This relocatable command representation replaces only private tool/artifact paths; actual exact invocation is recorded privately. One command, exit0. Internal sector erase/program footprint **0x8000–0x8FFF only**. No standalone erase command, other-sector write, firmware upload, NVS/OTA/app/remote_ctl initialization or settings TX. No rollback trigger or rollback command.

## Readback and preservation

Full4096-byte table readback SHA256 `fd62ef669cdbab98ac5372777a686d8dcd9813f7eb5302a67cc5136e96e90f69` equals candidate3072bytes plus1024FF. Independent SDK5.5.3 decode/MD5 PASS; all six previous32-byte entries byte-identical. Seven entries:

| Partition | Offset | Size |
| --- | --- | --- |
| nvs | 0x9000 | 0x6000 |
| phy_init | 0xf000 | 0x1000 |
| factory | 0x10000 | 0x800000 |
| otadata | 0x810000 | 0x2000 |
| ota_0 | 0x820000 | 0x300000 |
| ota_1 | 0xb20000 | 0x300000 |
| remote_ctl | 0xe20000 | 0x10000 |

Both OTA slots remain3MiB, factory0x10000 unchanged. Alignment/bounds/no-overlap PASS within16MiB. New remote_ctl data/nvs flags0, ends0xE30000. Independent complete target read65536bytes remains65536FF/0nonFF; SHA256 `71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063`.

Published protocol full16MiB preservation read completed before reboot,115200baud/exit0; SHA256 `d333b3d4ac6443de094a66c95a0c238d73445a189698e3d0780549336567c8d6`. **Every byte outside `[0x8000,0x9000)` equals the verified pre-write backup.** 50 differing bytes, all in the approved table sector. Installed bootloader, NVS, OTA metadata, all application images, gaps/tail and target stayed byte-identical before reboot. Historical factory image2485824bytes/SHA7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb retained. This is flash-byte preservation, not source equivalence.

## Normal boot and final state

One selected-esptool native USB HardReset, passive115200 capture45seconds/no application TX. Existing firmware booted from factory0x10000. No partition error, panic, watchdog indication or reset loop observed in capture; one ROM boot banner. [Selected sanitized structural boot lines](../references/device_evidence/remote/A-REMOTE-009/TABLE_ONLY_BOOT_SELECTED_LINES.log) confirm all seven entries and project12_LVGL_Test/version1/IDF5.5.3. Owner confirms normal display/UI and existing observable configuration without changing settings. Raw logs remain private. Device left running its existing firmware normally with new unused table entry; target observed erased before reboot. Existing firmware normal housekeeping after boot is not claimed globally frozen or a durable-backend test.

Rollback **NOT REQUIRED / NOT EXECUTED**. ROM download/read path demonstrated without JTAG; an actual restoration write remains untested. Table-write interruption can prevent normal boot; original sector plus complete verified local/separate-storage backup support the bounded recovery plan. Full-flash restore requires separate owner approval. No industrial power-loss campaign.

## Review and limits

Request owner acceptance of A009 limited layout hardware result and review/disposition of PR15; no automatic merge or A010. A008 remains DONE/OWNER ACCEPTED; no reproducible source defect demonstrated, Dell20+20compiles/3clean builds PASS, Ryzen intermittent host/environment/compiler-process failure exact causeUNKNOWN. Byte-reproducible builds/exact historical source-runtime equivalence remain unproven and nonblocking at approved practical level. Persistence/backend/common API/G1a/migration qualification remain separate. CCM frozen/Native unapproved/O01–O17/common gate OPEN; TUNER untouched. Private source/backup/NVS/credentials/raw paths not published.
