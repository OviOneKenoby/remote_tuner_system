# A-REMOTE-009 read-only hardware preflight

Recorded UTC: 2026-10-12T19:36:49.377474+00:00. Coordination input/reviewed preparation head `bd5682d327448696f659000f40ae4b50ab16eeb4`. [Owner acceptance/read-only scope](../references/A009_READ_ONLY_PREFLIGHT_OWNER_AUTHORIZATION_2026-10-12.md); PR15 remains OPEN / UNMERGED. A009 preparation is OWNER ACCEPTED. Current result: **PASS — READ-ONLY HARDWARE PREFLIGHT; PERSISTENT OPERATIONS NOT AUTHORIZED**.

## Exact device, ROM access and tools

Before opening the port, one connected native USB device was positively associated with REMOTE by its USB serial matching the privately recorded A007 MAC identity; owner confirmed connection and closed monitors. Exact current COM, MAC normally reported by esptool, USB serial/location/PNP identity and raw logs are recorded privately, not published. Chip: **ESP32-S3 (QFN56) (revision v0.2)**. Detected physical flash: **16777216bytes /16MiB**, not merely a compile option. Secure boot/flash encryption disabled, security flags0. Selected esptool4.11.0/package2.41100.0, GCC14.2.0+20251107/SDK5.5.3/Python3.11.7 identity recorded.

Initial selected-esptool automatic USB ROM reset (already demonstrated by A007) was used for read access instead of requiring physical button entry. ROM-only security/identity queries succeeded before loading the volatile read stub. Subsequent reads use no_reset before/after; owner explicitly kept115200baud. **ROM USB download entry and flash reading are available without JTAG.** No normal application return reset was requested. Device remains in ROM/stub download mode at the approval checkpoint; installed application is not currently running. Write-based recovery/rollback remains NOT TESTED and NOT AUTHORIZED.

## Complete private backup and independent verification

Two separate full physical-flash reads cover `[0x0,0x1000000)` at115200baud, while the application remains halted in download mode. Both completed exit0, each **16777216bytes**, SHA256:

`f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`

Full byte comparison and independent reopen/stream-read/hash: PASS. No all-FF, all-00 or truncation anomaly. The backup includes all flash sectors, including existing bootloader, table, factory, both OTA slots, NVS, gaps and tail; it is not a firmware-only export or a synthetic fixture. ESP image header/segment bounds/checksum/appended SHA are validated by the published offline verifier. No flash difference was observed between the two complete reads. Raw backup/NVS/credentials remain private and are not parsed for secrets or published.

Bootloader at0x0 independently parsed from the backup:20832bytes, ESP32-S3 chipID9; segment bounds/checksum/appended digest PASS and image ends before table0x8000. This is structural image validity, not a write-based recovery test or new source-equivalence claim.

Both copies are preserved in a durable owner-restricted local directory outside TEMP and the public repository, with owner/SYSTEM/administrator ACLs. Only C: storage is currently available; **owner explicitly deferred the separate-storage copy until before any future write**. Therefore external-copy verification remains a write prerequisite, not a hidden claim of independent-storage protection. No private backup paths, unique identifiers or raw-log hashes are published here.

## Independent partition table and target-region reads

Independent table read:4096bytes at0x8000, SHA256 `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46`. **BYTE-IDENTICAL** to accepted A007 installed baseline sector. First3072bytes SHA256 `d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835`; trailing1024bytes allFF. SDK5.5.3 decode/MD5 PASS; all six32-byte records byte-identical, factory0x10000 and both3MiB OTA slots unchanged. That separately captured sector also matches each complete backup. No table write occurred; candidate seven-entry table is NOT installed.

Independent target read: `[0xE20000,0xE30000)`,65536bytes. **65536FF /0nonFF**, SHA256 `71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063`, byte-identical to the same region in each backup. Still physically erased at this observation; no future unused/durability guarantee and no erase/initialization.

## Installed firmware/OTA identity and limits

Installed factory image at0x10000: **2485824bytes**, SHA256 `7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb`. Valid checksum/appended digest; **BYTE-IDENTICAL to historical A006/A007 installed image**. Descriptor project12_LVGL_Test/version1/IDF5.5.3. Existing OTA metadata in the verified full backup is allFF, so factory is the default boot selection. No OTA selection mutation or app upload. Live pre-reset behavior was not independently observed by this preflight; image identity is read-only byte evidence, not a fresh UI/runtime test.

**Current source equivalence remains NOT DEMONSTRATED**; the private A009 candidate build is not claimed identical to this historical installed image. Accepted A008 practical verdict, non-identical-build limits and unknown exact Ryzen process-failure cause remain preserved; no timestamp/path/linker forensic investigation or A010/backend/API work.

## Stop point and concrete next operation

Read-only protocol steps through backup/installed-state verification are complete, subject to the owner-deferred external-copy prerequisite. [Protocol](../protocols/A-REMOTE-009_USB_ROM_RECOVERY.md), [sanitized result](../references/device_evidence/remote/A-REMOTE-009/READ_ONLY_PREFLIGHT_RESULT.json), [structural checks](../references/device_evidence/remote/A-REMOTE-009/READ_ONLY_STRUCTURAL_VERIFICATION.json) and [operation summary](../references/device_evidence/remote/A-REMOTE-009/READ_ONLY_OPERATION_SUMMARY.json).

**STOP at the first-write checkpoint. Zero persistent write commands, erase commands, firmware uploads, NVS mutations, partition updates or rollback/recovery writes were executed by this preflight.** All target operations were ROM identification/security queries or flash reads; stub loading was RAM-only. Production source/tools/TUNER/CCM remain untouched; Native unapproved, O01–O17/common gate OPEN/NOT PASSED.

Proposed next operation, **NOT EXECUTED**: write the reviewed3072-byte candidate partitions.bin SHA256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184` at0x8000, keeping image-header parameters. Its internal sector erase/program footprint is `[0x8000,0x9000)`. Existing firmware/bootloader/OTA metadata/NVS/new64KiB target are not part of that write. No matching new firmware upload is required. Interruption can prevent normal boot; verified full backup plus ROM USB is the planned recovery path, not a tested restoration.

Before any write: verify a separate-storage copy against this exact backup SHA, recheck the same device and candidate, and obtain explicit owner approval for the table-only operation bound to this backup/preflight. Rollback/recovery writes need their own explicit authorization; nothing in current acceptance authorizes them. PR15 stays OPEN/unmerged.
