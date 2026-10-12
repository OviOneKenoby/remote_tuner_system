# A-REMOTE-009: owner USB/ROM layout validation and full-backup rollback

**PREPARED / NOT EXECUTED. This document does not authorize hardware access or writes.**
Preparation starts at coordination `e6fa6f4911eb6bcd342d1db9600ad66f134636ab`. Use the final reviewed PR15 head and its artifact manifest. Current execution authority is host preparation only. Obtain a separate owner decision for hardware validation; additionally stop at step6 and obtain explicit approval of the actual backup/preflight record before the first persistent hardware operation. Owner approval of later rollback must explicitly cover complete-backup restoration. Do not paste this whole document into PowerShell as an unattended script.

This practical hobby/public-beta protocol validates the partition addition and return to existing behavior. It does not qualify a durable backend, migration, power-failure campaign, exact source/runtime equivalence or industrial recovery. The candidate contains seven entries; the six existing records are byte-identical. The addition is `remote_ctl,data,nvs,0xE20000,0x10000,`, flags0. Existing factory/OTA addresses and sizes remain fixed. The new area must stay erased; no NVS initialization is performed by this task.

## 1. Stage the reviewed files and protect private evidence

After separate hardware-access approval, use Windows amd64/PowerShell with Python3.11.7 and the selected esptool4.11.0 package (`tool-esptoolpy2.41100.0`). Use the already validated host tools; do not update them as part of validation. Copy the safe generated candidate CSV/BIN and `ARTIFACT_SHA256.json` from the exact reviewed PR head, together with this protocol and `a009_verify_backup.py`. No private source or candidate firmware is required for the recommended table-only operation.

Choose a new private local directory with at least64MiB free for two16MiB reads and rollback verification (plus logs). Keep the entire backup, security/device identifiers and local reports private: full flash includes NVS credentials and personal/device data. Keep a second verified copy of the backup on separate owner-controlled storage before writing. Backups must be for this exact device; never restore another device's backup. Do not publish backups or raw logs. Keep stable USB power/cable and disable host sleep for the operation.

Use these owner-filled variables, not guessed paths:

```powershell
$PythonExe = 'OWNER_SELECTED_PYTHON_3_11_7_EXE'
$EspTool = 'OWNER_SELECTED_TOOL_ESPTOOLPY_4_11_0_ESPTOOL_PY'
$PrivateDir = 'OWNER_PRIVATE_BACKUP_DIRECTORY'
$CandidateBin = 'OWNER_REVIEWED_partitions.bin'
$ArtifactManifest = 'OWNER_REVIEWED_ARTIFACT_SHA256.json'
$OfflineVerifier = 'OWNER_REVIEWED_a009_verify_backup.py'
$Backup = Join-Path $PrivateDir 'REMOTE01-before-A009-16MiB.bin'
$BackupCheck = Join-Path $PrivateDir 'REMOTE01-before-A009-check-16MiB.bin'
$SecondBackup = 'OWNER_SEPARATE_STORAGE_FULL_BACKUP_PATH'
```

Check the candidate BIN size3072 and SHA-256 against the reviewed manifest. Baseline table artifact SHA is `d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835`; installed4096-byte baseline sector SHA is `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46`. Candidate table SHA must match the final manifest and independent local generation. Stop on missing files/tool identity, insufficient storage, any hash mismatch or an existing backup filename; never overwrite earlier evidence.

```powershell
$ExpectedCandidateHash = (Get-Content -LiteralPath $ArtifactManifest -Raw | ConvertFrom-Json).'partitions.bin'.sha256
if ((Get-Item -LiteralPath $CandidateBin).Length -ne 3072) { throw 'STOP: candidate size' }
if ((Get-FileHash -LiteralPath $CandidateBin -Algorithm SHA256).Hash -ne $ExpectedCandidateHash) { throw 'STOP: candidate hash' }
if ((Test-Path -LiteralPath $Backup) -or (Test-Path -LiteralPath $BackupCheck)) { throw 'STOP: backup filename exists' }
```

## 2. Identify this device and exact COM port

Close PlatformIO monitors, terminals and all other serial users. Observe the device's ordinary display/function without changing settings and record it privately. With owner control, use one known data cable and identify the port by unplug/replug association, Device Manager or the inventory below. A007 previously used COM3, USB VID303A/PID1001; **COM3 is historical, not a current selection**. Record the exact current COM and USB identity. If there are multiple plausible ports or no positively associated port, STOP. Never use esptool auto-port selection.

```powershell
Get-CimInstance Win32_SerialPort | Select-Object DeviceID,Name,PNPDeviceID
$RemotePort = 'COM_REPLACE_WITH_POSITIVELY_IDENTIFIED_DEVICE'
if ($RemotePort -notmatch '^COM[0-9]+$') { throw 'STOP: exact COM required' }
```

The inventory can omit native USB devices on some Windows hosts; use Device Manager when needed, rather than treating an absent inventory row as a valid guessed port. Use USB serial/ROM download transport only. A combined USB Serial/JTAG device name does not require or authorize JTAG debugging. Do not use JTAG, openocd, provisioning, eFuse operations or a hardware debugger.

## 3. Enter ESP32-S3 ROM download mode and recheck size/security

Use the board's documented BOOT/RESET controls: hold BOOT(GPIO0 low), press/release RESET, then release BOOT. GPIO46 must retain its board-provided download-compatible state; do not improvise jumpers or change wiring. If those controls are inaccessible or unknown, STOP for a board-specific safe entry decision. ROM USB may re-enumerate; positively identify and update `$RemotePort` again. Recovery must use this same ROM entry path, independent of application/partition-table boot. A007 already demonstrated ROM/stub reads on this device; no recovery test is claimed by A009.

Use115200, no automatic port selection, no force override, no reset loop. The following commands leave the chip in download mode. The identification commands do not load the RAM stub; read/write commands may load the esptool RAM stub, which is volatile and does not write target flash by itself. Re-enter ROM manually and recheck the port before a new command if synchronization fails; stop on a communication warning rather than escalating retries/baud.

```powershell
$Rom = @('--chip','esp32s3','--port',$RemotePort,'--baud','115200','--before','no_reset','--after','no_reset')
& $PythonExe $EspTool @Rom --no-stub flash_id
if ($LASTEXITCODE -ne 0) { throw 'STOP: flash identification failed' }
& $PythonExe $EspTool @Rom --no-stub get_security_info
if ($LASTEXITCODE -ne 0) { throw 'STOP: security query failed' }
```

Privately record chip ESP32-S3 and detected physical flash16MiB, not just the configured size. A007 manufacturer20/device4018 and disabled secure boot/flash encryption are historical. If current physical size is not16MiB, security/encryption/download policy differs or either output is ambiguous/restricted, STOP: do not override protection, burn eFuses or continue this plaintext-backup/write protocol. USB ROM download must remain available under the confirmed current security policy; do not infer availability from a compile option alone.

## 4. Make and verify the complete16MiB backup before any write

Remain in ROM/stub mode, with no application running between reads. Read exactly addresses `[0x0,0x1000000)` twice, including bootloader, table, factory, both OTA slots, NVS, gaps and tail. These are read operations only. Do not read merely a firmware image or omit the unused tail. If a fresh session is necessary, re-enter ROM/recheck the same port; do not boot the app between verification reads.

```powershell
& $PythonExe $EspTool @Rom read_flash --flash_size 16MB 0x0 0x1000000 $Backup
if ($LASTEXITCODE -ne 0) { throw 'STOP: complete backup failed' }
& $PythonExe $EspTool @Rom read_flash --flash_size 16MB 0x0 0x1000000 $BackupCheck
if ($LASTEXITCODE -ne 0) { throw 'STOP: verification read failed' }
if ((Get-Item -LiteralPath $Backup).Length -ne 16777216 -or (Get-Item -LiteralPath $BackupCheck).Length -ne 16777216) { throw 'STOP: incomplete backup' }
$BackupHash = (Get-FileHash -LiteralPath $Backup -Algorithm SHA256).Hash
if ($BackupHash -ne (Get-FileHash -LiteralPath $BackupCheck -Algorithm SHA256).Hash) { throw 'STOP: backup reads differ' }
$BackupHash
```

Record backup size/hash, time, exact device/port and tool versions privately. Copy `$Backup` to a separate owner-controlled storage location, rehash that copy and require the same16777216bytes/SHA before writing. Record that backup path privately. Do not proceed with a single unverified/partial backup or rely on an earlier A007 partial capture.

```powershell
if (Test-Path -LiteralPath $SecondBackup) { throw 'STOP: second-copy filename exists' }
Copy-Item -LiteralPath $Backup -Destination $SecondBackup
if ((Get-Item -LiteralPath $SecondBackup).Length -ne 16777216 -or (Get-FileHash -LiteralPath $SecondBackup -Algorithm SHA256).Hash -ne $BackupHash) { throw 'STOP: separate backup copy differs' }
```

## 5. Verify the currently installed table, target region and firmware identity

The complete backup is a fresh physical flash read; offline extraction checks its installed table sector byte-for-byte against the accepted baseline, checks the entire target64KiB remainsFF, and requires the accepted blank otadata/factory image. The verifier bounds/parses the factory ESP image, validates checksum/appended digest, hashes the actual image without padding, and records its descriptor. It never prints raw flash or NVS bytes.

```powershell
& $PythonExe $OfflineVerifier --backup $Backup --output (Join-Path $PrivateDir 'A009-prewrite-private.json')
if ($LASTEXITCODE -ne 0) { throw 'STOP: installed baseline or target region differs' }
```

Accepted historical factory image SHA is `7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb`, actual length2485824, offset0x10000, project12_LVGL_Test/version1/IDF5.5.3. The backup proves current bytes only; the prior visual observation and later reboot log provide running behavior evidence. If table, region, otadata or image differ, STOP for a focused review; do not select a different slot/image or erase the region. Default NVS/settings can have changed normally; retain their current bytes in the full backup without exposing them. No matching newly built firmware is required for adding an unused NVS partition to this accepted baseline; retain installed firmware. The candidate firmware is a private build-confidence artifact, not an upload instruction.

## 6. Mandatory owner write-approval checkpoint

**STOP before the first persistent operation.** Return the reviewed PR/head, exact candidate table SHA, backup size/hash and second-copy verification, fresh physical/security/table/region/image preflight results, exact port and planned write footprint to the owner. Request explicit approval for **the table-only write of this candidate at0x8000 and, if needed, full-backup rollback**. Do not execute step7/9 unless that approval explicitly covers them. Preparation approval, architecture approval, a backup or a PASS report is not write approval.

The write below internally erases/reprograms sector `[0x8000,0x9000)`. An interrupted table write can prevent normal boot even while firmware/NVS/OTA partitions are intact. ROM download mode plus the verified complete backup are the recovery path. This is a concrete boot risk, not an industrial power-failure qualification claim. If stable power/ROM access or a verified backup is unavailable, STOP without writing.

## 7. Approved table-only write and immediate readback

Only after the explicit checkpoint approval, re-enter ROM/reconfirm the same device/port and rehash both candidate and preserved backup. Do not use PlatformIO upload, a generated whole-project flash command, an erase command, bootloader update, OTA metadata initialization or NVS provisioning. Only the table sector is written. Keep all image header parameters; no matching firmware upload is required or authorized by this plan.

```powershell
$Rom = @('--chip','esp32s3','--port',$RemotePort,'--baud','115200','--before','no_reset','--after','no_reset')
& $PythonExe $EspTool @Rom write_flash --flash_mode keep --flash_freq keep --flash_size keep 0x8000 $CandidateBin
if ($LASTEXITCODE -ne 0) { throw 'STOP: table write failed; stay in ROM for approved rollback' }
$Readback = Join-Path $PrivateDir 'A009-candidate-table-readback-4096.bin'
& $PythonExe $EspTool @Rom read_flash --flash_size 16MB 0x8000 0x1000 $Readback
if ($LASTEXITCODE -ne 0) { throw 'STOP: table readback failed' }
$ReadbackBytes = [IO.File]::ReadAllBytes($Readback)
if ($ReadbackBytes.Length -ne 4096) { throw 'STOP: readback size' }
$ExpectedSector = New-Object byte[] 4096
[IO.File]::ReadAllBytes($CandidateBin).CopyTo($ExpectedSector,0)
for ($i=3072; $i -lt 4096; $i++) { $ExpectedSector[$i]=255 }
if ([Convert]::ToBase64String($ReadbackBytes) -ne [Convert]::ToBase64String($ExpectedSector)) { throw 'STOP: candidate readback differs; do not boot' }
```

For a successful write, read the complete flash once more while still in ROM/stub mode, before reboot. Compare all bytes outside `[0x8000,0x9000)` with the prewrite backup; require unchanged bootloader, all app slots, OTA metadata, NVS and the still-erased64KiB target. Store this read privately. An unexpected changed byte outside the table sector is a concrete risk: STOP and use only the separately approved rollback path, not an explanation based on timestamps.

```powershell
$Postwrite = Join-Path $PrivateDir 'A009-after-table-before-boot-16MiB.bin'
& $PythonExe $EspTool @Rom read_flash --flash_size 16MB 0x0 0x1000000 $Postwrite
if ($LASTEXITCODE -ne 0) { throw 'STOP: preservation read failed' }
$BeforeBytes=[IO.File]::ReadAllBytes($Backup); $AfterBytes=[IO.File]::ReadAllBytes($Postwrite)
if ($AfterBytes.Length -ne 16777216) { throw 'STOP: preservation read incomplete' }
for ($i=0; $i -lt 16777216; $i++) {
    if (($i -lt 32768 -or $i -ge 36864) -and $BeforeBytes[$i] -ne $AfterBytes[$i]) { throw "STOP: changed byte outside table sector at $i" }
}
```

## 8. Reboot and check the existing behavior

Release BOOT and reset normally using the board's documented controls. Observe/passively capture boot at115200 with a normal serial monitor (no diagnostic/provisioning TX). Require a valid seven-entry table, factory boot at0x10000, the accepted image/project identity where logged, no partition/MD5/load error, panic/reset loop, and the same ordinary display/basic function as preflight. Do not change network settings or trigger OTA/NVS/backend tests. Record PASS/FAIL and the owner's visual observation, keeping raw logs private. Normal existing firmware may maintain its default NVS during boot; that is not an A009 feature test. Automatic OTA rollback is not enabled; the rollback here is USB/ROM restoration, not an OTA promise.

On a failed boot or any unexpected behavior: STOP normal-boot retries; return to ROM with BOOT/RESET, recheck the COM, and use the separately approved complete-backup recovery. Do not guess a matching firmware or flash a newly built image to hide the failure.

## 9. Approved full-backup rollback through ROM/USB

If necessary, and only if the checkpoint approval explicitly authorizes rollback, enter ROM manually regardless of whether the table/application boots. Positively identify the same device/COM, confirm unchanged16MiB/security policy and rehash the preserved full backup against `$BackupHash`. Restore the complete device image at0x0 with all header options `keep`; selected esptool4.11.0 returns bootloader bytes unchanged when all three options are `keep`. This restore replaces all flash content, including settings/NVS/OTA state, with the prewrite snapshot. Do not run a separate erase, `--force`, eFuse operation or application upload. Restoring flash does not restore changed eFuses; this task never changes them.

```powershell
$Rom = @('--chip','esp32s3','--port',$RemotePort,'--baud','115200','--before','no_reset','--after','no_reset')
if ((Get-Item -LiteralPath $Backup).Length -ne 16777216 -or (Get-FileHash -LiteralPath $Backup -Algorithm SHA256).Hash -ne $BackupHash) { throw 'STOP: rollback backup integrity' }
& $PythonExe $EspTool @Rom write_flash --flash_mode keep --flash_freq keep --flash_size keep 0x0 $Backup
if ($LASTEXITCODE -ne 0) { throw 'STOP: rollback write failed; retain evidence and remain in ROM' }
$RollbackRead = Join-Path $PrivateDir 'A009-rollback-verification-16MiB.bin'
& $PythonExe $EspTool @Rom read_flash --flash_size 16MB 0x0 0x1000000 $RollbackRead
if ($LASTEXITCODE -ne 0) { throw 'STOP: rollback read failed' }
if ((Get-Item -LiteralPath $RollbackRead).Length -ne 16777216 -or (Get-FileHash -LiteralPath $RollbackRead -Algorithm SHA256).Hash -ne $BackupHash) { throw 'STOP: complete rollback differs; do not claim recovered' }
```

Only after exact complete-flash readback equality, release BOOT/reset normally. Require baseline table, accepted factory boot and ordinary owner-observed function. Record rollback outcome separately. Stop if ROM cannot be entered, USB communication is unreliable, security differs or verification fails. Do not repeatedly rewrite or escalate to JTAG; request a focused owner recovery decision.

## References and current execution status

Official guidance: [ESP-IDF5.5.3 ESP32-S3 partition tables](https://docs.espressif.com/projects/esp-idf/en/v5.5.3/esp32s3/api-guides/partition-tables.html), [esptool4 basic commands](https://docs.espressif.com/projects/esptool/en/release-v4/esp32/esptool/basic-commands.html), and [ESP32-S3 ROM boot selection](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/advanced-topics/boot-mode-selection.html). Command spelling/parameter preservation were also checked against the selected local esptool4.11.0 source. Use that pinned version, not renamed esptool5 syntax.

**Every protocol command is NOT RUN in A009 preparation. Current COM, new complete backup, new security preflight, write/readback/reboot/rollback hardware results are UNKNOWN / NOT RUN. No persistent hardware operation, hardware access or protocol execution occurred.**


## Read-only execution record — 2026-10-12T19:36:49.377474+00:00
[Owner accepts preparation and authorizes read-only preflight](../references/A009_READ_ONLY_PREFLIGHT_OWNER_AUTHORIZATION_2026-10-12.md); [actual execution report](../reports/A-REMOTE-009_READ_ONLY_PREFLIGHT.md). Steps through installed-state/backup verification PASS; initial USB ROM entry used selected automatic reset, owner retained115200baud and deferred separate-storage copy until before writing. Earlier NOT RUN paragraphs remain historical preparation records. Current mode ROM/stub; no normal return reboot. **Steps6–9 persistent operations remain NOT AUTHORIZED / NOT EXECUTED.** No table/firmware/NVS/erase/rollback write or recovery test. External-copy verification and explicit fresh-backup-bound approval are required before any write.
