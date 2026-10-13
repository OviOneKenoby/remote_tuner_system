# A-REMOTE-010 hardware validation protocol

**STAGES 1–5 EXECUTED / PASS; STAGE 6 PRECONDITION PASS, STOPPED BEFORE COMMIT2.** One saved read-only RECOVER verified valid-recoverable generation 1/next 2/incomplete 0. Never repeat `INIT` or `COMMIT1`; COMMIT2 still requires explicit owner authorization. Practical hobby/public-beta scope applies.

## Fixed identities

- Candidate environment: `remote01_a010_diag`; definition `A010_REMOTE_PERSISTENCE_DIAGNOSTIC=1`.
- Candidate `firmware.bin`: 2,503,936 bytes; SHA-256 `308181d4144494734fe8fae360938f74b9f886fb4c41bff0cba9b89427e4d248`.
- Candidate flash address: `0x10000`; esptool sector span affected by this image: `0x10000–0x273FFF` (2,506,752 bytes including sector padding).
- Candidate partitions SHA-256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`, exact A-009; it must not be flashed.
- Retained full backup: 16,777,216 bytes; SHA-256 `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`; primary Ryzen and independent Orange Pi copies required.
- Original table-sector backup: 4096 bytes; SHA-256 `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46`; retained but not written in this protocol.
- Previous installed factory image: 2,485,824 bytes; SHA-256 `7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb`.
- Exact prior-byte restore span extracted privately from the verified full backup: offset `0x10000`, length 2,506,752 (`0x264000`) bytes, SHA-256 `57736494ea726600c68e25ae6a8f5b3bd109f5e5c1d5d858a05afd7ee8603aca`.

## Stage 0 — offline verification

Verify both full-backup copies, original table sector, restore span and every candidate hash above. Verify the candidate image header, ESP32-S3 target, image length and flash parameters with esptool without connecting hardware. Require PR #16 to remain open/unmerged and record the exact candidate publication head. STOP on any mismatch or missing recovery copy.

## Stage 1 — separately approved read-only hardware preflight

1. Connect the owner-identified REMOTE through its USB data cable; close all serial monitors.
2. Enumerate ports and bind the session to the newly observed device. Never assume historical COM3.
3. First hardware command: `esptool.py --chip esp32s3 --port <VERIFIED_COM> --baud 115200 chip_id`.
4. Read flash identity and require physical 16 MiB. Record tool version and sanitized chip/revision result; keep MAC private.
5. Read `0x8000–0x8FFF`; require the accepted seven-entry A-009 table. Read `0xE20000–0xE2FFFF`; require 65,536 bytes of `0xFF`. Read the current factory-image range and require the accepted prior identity where reproducible.
6. Confirm ROM/USB recovery remains available without JTAG. STOP on device, flash, table, target-region, security or backup mismatch.

Executed 2026-10-13 under exact owner authorization: PASS. See [Stage 1 report](../reports/A-REMOTE-010_STAGE1_READ_ONLY_PREFLIGHT.md). No Stage 2 or later command was executed.

Return the preflight to the owner and obtain explicit approval before Stage 2. Read-only approval does not authorize flashing.

## Stage 2 — candidate firmware only

After exact approval, run once:

`esptool.py --chip esp32s3 --port <VERIFIED_COM> --baud 115200 write_flash --flash_mode keep --flash_freq keep --flash_size keep 0x10000 <PRIVATE_CANDIDATE_FIRMWARE_BIN>`

No bootloader, partition table, OTA data, default NVS or `remote_ctl` image is supplied. Read back 2,503,936 bytes from `0x10000` and require candidate SHA-256 `308181d4144494734fe8fae360938f74b9f886fb4c41bff0cba9b89427e4d248`. STOP without retry on write/readback mismatch.

Executed 2026-10-13 under exact owner authorization: PASS. Write and full readback matched the candidate; controlled boot identity, normal UI/configuration and unchanged erased `remote_ctl` passed. See [Stage 2 report](../reports/A-REMOTE-010_STAGE2_DIAGNOSTIC_FLASH.md). No Stage 3 or diagnostic command was executed.

Reset once to normal factory boot. Require no boot loop, panic, watchdog or partition error; require the normal UI and existing observable configuration. Require the boot line `build=A010_VALIDATION diagnostic=ENABLED persistence_on_boot=0`. Before any diagnostic command, read `remote_ctl` through ROM again and require all `0xFF`; this proves candidate boot caused no persistence activity. STOP on any UI/configuration or target-byte change.

## Stage 3 — read-only diagnostic status

Open one serial monitor at 115200. Send `!A010 INFO`, then `!A010 STATUS`. Require the exact partition identity and `state=erased`, generation 0, no payload output. Close the monitor before every ROM read/reset. STOP on any other state or any unexpected target change.
Executed 2026-10-13 under exact owner authorization: PASS. Both commands were accepted once with exact partition identity, erased schema-1 generation-zero state, no incomplete transaction, no unexpected error and `payload_logged=0`. See [Stage 3 report](../reports/A-REMOTE-010_STAGE3_READ_ONLY_UART.md). Stage 4 was not executed.

## Stage 4 — separately staged initialization

Obtain explicit owner approval for initialization alone. Send exactly `!A010 INIT CONFIRM-A010-REMOTE-CTL-INIT` once. Require before `erased`, after `initialized_empty`, generation 0, next 1. Send `!A010 STATUS`; record entry counts. Reboot once and send `!A010 RECOVER`; require initialized empty generation 0/next 1 and normal UI/configuration. STOP without retry on any mismatch.
Executed partially 2026-10-13: `INIT` once and immediate `STATUS` passed exactly. One serial reset signal produced no boot banner or A010 identity in 20 seconds, so the STOP rule applied. `RECOVER` was not sent and `INIT` must not be repeated. See [Stage 4 partial report](../reports/A-REMOTE-010_STAGE4_PARTIAL_INITIALIZATION.md). A new owner decision is required before reset/reboot verification or read-only recovery inspection.
A separately authorized continuation also stopped: its one reset produced an ESP32-S3 ROM banner in `DOWNLOAD(USB/UART0)` mode and `waiting for download`, without normal A010 boot. `RECOVER` was not sent. See [Stage 4 recovery-continuation stop](../reports/A-REMOTE-010_STAGE4_RECOVERY_CONTINUATION_STOP.md). The device remains in ROM download mode pending a new owner decision for one normal hard reset and read-only recovery verification.
Final continuation completed 2026-10-13: the owner performed the normal reset out of ROM mode and confirmed functional UI. One read-only `!A010 RECOVER` passed with exact initialized-empty generation 0/next 1/no-incomplete state and no payload logging. See [Stage 4 completion](../reports/A-REMOTE-010_STAGE4_COMPLETE.md). Stage 5 was not executed.

## Stage 5 — separately staged first record

Obtain explicit owner approval for COMMIT1. Send exactly `!A010 COMMIT1 CONFIRM-A010-REMOTE-CTL-COMMIT1` once. Require before generation 0, after valid generation 1/next 2. Reboot once; send `!A010 RECOVER`; require generation 1, recoverable, no payload output, and normal UI/configuration. STOP without retry on any mismatch.
Executed 2026-10-13 under exact owner authorization: PASS. COMMIT1 ran once with the required transition, the owner performed the proven normal hardware reset, and one read-only RECOVER verified valid generation 1/next 2/no-incomplete state with normal UI/configuration. See [Stage 5 report](../reports/A-REMOTE-010_STAGE5_FIRST_RECORD.md). Stage 6 was not executed.

## Stage 6 — separately staged successor

Precondition check stopped execution on 2026-10-13: a read-only INFO returned the correct diagnostic/partition identity but `storage_error`, generation 0/next 0 rather than valid generation 1/next 2. COMMIT2 was not sent. See [stop report](../reports/A-REMOTE-010_STAGE6_PRECONDITION_STOP.md).

An owner-authorized retry also stopped before mutation: COM3 identity remained correct, but one read-only RECOVER produced serial bytes without an A010 response. Passive follow-up found no diagnostic or fault line. The missing-output stop condition applied; COMMIT2 remained unsent. See [retry report](../reports/A-REMOTE-010_STAGE6_RETRY_STOP.md).

Diagnosis corrected the interpretation of the preceding INFO: INFO uses `inspect(false)`, which returns `storage_error` for any exact, non-erased partition without opening NVS. The retry's raw 3,460-byte buffer was never persisted and cannot be inspected retrospectively. Minimum next step is one separately authorized, read-only RECOVER using the proven ten-second capture procedure, saving raw bytes privately before parsing. See [diagnosis](../reports/A-REMOTE-010_STAGE6_DIAGNOSIS.md).

Read-only precondition verification completed 2026-10-13: PASS. Exactly one RECOVER using the proven ten-second private capture procedure verified valid generation 1/next 2/incomplete 0 and the Stage 5 capacity counts. The 250-byte raw capture was saved and hashed privately. No COMMIT2 was sent. See [precondition report](../reports/A-REMOTE-010_STAGE6_READ_ONLY_PRECONDITION.md).

Obtain explicit owner approval for COMMIT2. Send exactly `!A010 COMMIT2 CONFIRM-A010-REMOTE-CTL-COMMIT2` once. Require before generation 1, after valid generation 2/next 3. Reboot once; send `!A010 RECOVER`; require generation 2 and recoverable. Send `!A010 STATUS` and record safe used/free/available entry counts. Require normal UI/configuration. STOP without retry on any mismatch.

## Stage 7 — restore prior firmware

Close the monitor and enter ROM mode. After explicit rollback approval, write only the verified 2,506,752-byte prior-byte restore span at `0x10000` with keep mode/frequency/size. Read back that full span and require SHA-256 `57736494ea726600c68e25ae6a8f5b3bd109f5e5c1d5d858a05afd7ee8603aca`. Reset once and require the accepted previous factory identity, normal UI and retained configuration. Do not write the table, bootloader, OTA data or default NVS.

Diagnostic records remain in `remote_ctl` unless the owner separately authorizes Stage 8. The restored pre-A010 firmware ignores this dedicated partition.

## Stage 8 — optional separate `remote_ctl` erase

This stage is optional and requires its own explicit owner authorization. While the exact diagnostic candidate is running, send `!A010 ERASE CONFIRM-A010-REMOTE-CTL-ERASE` once. Require before state/generation and after `erased`; independently read all 64 KiB and require `0xFF`. Never erase after failure automatically. If prior firmware has already been restored, reflashing the candidate merely to erase also requires new exact approval and subsequent prior-firmware restoration.

## Universal STOP and recovery rules

Stop on unexpected reset, boot loop, panic, watchdog, identity mismatch, wrong partition, non-FF initial target, default-NVS/configuration change, corrupt/ambiguous status, wrong generation, unexpected write range, missing output, hash mismatch or any command retry request. Preserve sanitized evidence and do not repeat a mutation. ROM/USB and the verified full backup remain the recovery path. Whole-flash restoration requires separate owner approval. Never use JTAG. Never publish raw flash, NVS bytes, payloads, MAC, credentials, source, binaries or private paths.
