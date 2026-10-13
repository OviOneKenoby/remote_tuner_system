# A-REMOTE-010 hardware validation protocol

**PREPARED / NOT EXECUTED. Current authority stops before all hardware access and persistent operations.** This practical hobby/public-beta protocol is for a later owner-authorized A-REMOTE-010 hardware phase. It does not authorize upload, flash write, erase, NVS mutation, partition change, recovery write, or A-REMOTE-011.

## 1. Retain and verify recovery evidence

Before connecting the device, verify both owner-retained 16 MiB A-009 backups are exactly 16,777,216 bytes with SHA-256 `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`. Verify the original 4096-byte `0x8000–0x8FFF` sector backup SHA-256 `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46`. Keep one full backup on the owner-controlled Orange Pi. Stop on a missing copy or mismatch.

## 2. Freeze exact test artifacts before requesting write approval

The current clean candidate firmware is 2496400 bytes, SHA-256 `b045bbe720091da89871a36686d17aa2ca06a27efdca05a90d2b660120f55dd3`; its partition table SHA-256 is `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184` and is byte-identical to installed A-009. It contains the backend but deliberately has no runtime caller, so it cannot initialize or exercise `remote_ctl` merely by booting.

Before hardware validation, add in the restricted private source and review one narrowly gated diagnostic activation. It must require an explicit operator action after normal boot, accept only fixed non-secret test payloads, expose only status/generation/CRC-safe summaries, have no network/UI/common-API path, and perform no automatic partition erase or write. Build it cleanly and record exact firmware/ELF/map hashes and the complete source delta. Do not proceed with the dormant candidate alone and do not improvise a raw NVS image. Stop until the owner has approved that exact diagnostic artifact and the operations below.

## 3. Read-only preflight

After separate hardware-access approval, positively identify the REMOTE device and current COM port; never assume historical COM3. Enter ESP32-S3 ROM download mode through USB, confirm 16 MiB flash and unchanged security policy, then read the installed table sector, factory image identity, and all 64 KiB at `0xE20000`. Require the seven-entry A-009 table and an entirely `0xFF` target. Rehash the retained backup immediately before any write. Stop on identity, table, target, security, tool, artifact or backup mismatch.

## 4. Mandatory first-write checkpoint

Return the exact COM/device match, backup verification, read-only preflight, diagnostic firmware hash, flash footprint and planned record operations to the owner. Obtain explicit approval before the first persistent operation. Approval must state whether it covers only the factory application write at `0x10000`, the controlled `remote_ctl` initialization/records, and any bounded rollback. It must not imply table, bootloader, OTA-data, default-NVS, whole-flash or recovery-test permission.

## 5. Exact bounded write sequence after approval

1. Flash only the owner-approved diagnostic `firmware.bin` at factory offset `0x10000` with mode/frequency/size kept. Do not write bootloader, partition table, OTA metadata, default NVS, or `remote_ctl` directly.
2. Read back the exact application image range and verify its image/hash identity. Reset once and require normal factory boot, UI and existing observable configuration.
3. Confirm `remote_ctl` is still erased. Invoke the gated diagnostic action once to initialize schema/root/fence, then read/reboot/recover and require generation 0 with no payload and no command emission.
4. Explicitly commit fixed non-secret record A at generation 1; reboot and require exact recovery of A. Commit fixed non-secret record B at generation 2; reboot and require B as sole authority and next generation 3. Never log full payload bytes.
5. Read the entire `remote_ctl` region privately. Require changes only inside it, a valid NVS structure, the bounded namespace/keys, and no default-NVS change. Recheck UI/configuration.
6. Do not simulate power loss on hardware in this practical phase. Host tests remain the interruption evidence. Stop after the two controlled commits.

STOP immediately on boot loop, panic, watchdog reset, partition/NVS error, unexpected erase, default-NVS/configuration change, ambiguous recovery, wrong generation/payload, unexpected flash range, or any artifact/readback mismatch. Preserve logs without credentials or payloads. Do not retry persistent operations.

## 6. Bounded rollback plan

Normal rollback requires a separately approved exact prior factory-image restoration at `0x10000`. Restoring `remote_ctl` to its accepted erased state requires a separately approved erase of only `0xE20000–0xE2FFFF`; do not perform it implicitly. If the table is unexpectedly affected, stop and seek approval to restore only the retained original/candidate table sector as appropriate. A complete 16 MiB restore remains a separate owner decision. Use USB/ROM recovery without JTAG and verify every restored range by readback before one normal boot.

## Expected evidence

Publish only sanitized command classes, exit codes, artifact hashes, structural partition/NVS results, generations/statuses, reboot behavior and owner UI/configuration observation. Never publish source, full flash, NVS bytes, payloads, credentials, MAC, private paths, or raw logs. Keep PR #16 open until owner review. A-REMOTE-011 remains NOT STARTED.
