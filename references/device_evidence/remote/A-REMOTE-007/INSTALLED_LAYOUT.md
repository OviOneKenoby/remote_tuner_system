# Installed chip, flash, security and layout
Measured via selected esptool4.11.0 on COM3/USB-Serial-JTAG,115200 baud. Chip ESP32-S3 QFN56 rev0.2, chipID9; reported PSRAM8MB,40MHz crystal. flash_id manufacturer0x20/device0x4018 detects **16MiB physically**; configured/header16MiB are separate agreeing observations. Secure Boot DISABLED, Flash Encryption DISABLED; security flags0. ROM/stub read access succeeded; individual download/eFuse restriction bits not exhaustively queried and remain UNKNOWN. No bypass or persistent setting change. Full MAC remains only in private raw logs; public suffix redacted.

## Installed table
| Label | Type/subtype numeric | Offset | Size hex / KiB | End exclusive |
| --- | --- | --- | --- | --- |
| nvs | 1/2 | 0x9000 | 0x6000 / 24 | 0xF000 |
| phy_init | 1/1 | 0xF000 | 0x1000 / 4 | 0x10000 |
| factory | 0/0 | 0x10000 | 0x800000 / 8192 | 0x810000 |
| otadata | 1/0 | 0x810000 | 0x2000 / 8 | 0x812000 |
| ota_0 | 0/16 | 0x820000 | 0x300000 / 3072 | 0xB20000 |
| ota_1 | 0/17 | 0xB20000 | 0x300000 / 3072 | 0xE20000 |

Primary table offset0x8000 confirmed from build before access, sector4096 read, decoded using selectedSDK5.5.3 gen_esp32part. Sector SHA256 `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46`. Build/A006 generated BIN length3072; installed prefix3072 is byte-identical to that BIN and independently regenerated currentCSV, SHA `d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835`. Remaining1024 bytes allFF. Classification **MATCH EXACT** on equal-length3072 artifact and equal-length4096 padded expected-sector comparisons. Direct4096-vs3072 file lengths differ; no silent claim their whole-file hashes are equal. Decoded structure agrees entirely, no unexplained differences.

Bootloader/table reservation0x0..0x9000; no installed filesystem/coredump/custom partition. OTA slots each3MiB retained. Region0xE20000..0xE30000 lies after all installed entries, below detected16MiB. Whole bootloader binary not read/hashed; banner reportsIDF5.5.3/Oct6. Board PCB model/bootloader bytes/eFuse inventory and permanent tail ownership remain unverified, but no installed partition conflicts with candidate. NVS0x9000..0xF000 not read; remote_wifi usage/health/preservation statistics UNKNOWN.
