# A-REMOTE-009 preparation report

Recorded UTC: 2026-10-12T18:35:41.124995+00:00. Coordination input `e6fa6f4911eb6bcd342d1db9600ad66f134636ab`; assignment `b55176d8f9a2a18f175c6eae027a62e235f63d1f`. [Owner authorization](../references/A009_PREPARATION_OWNER_AUTHORIZATION_2026-10-12.md); [PR15](https://github.com/OviOneKenoby/remote_tuner_system/pull/15) stays OPEN/unmerged.

**PASS â€” HOST LAYOUT/RECOVERY PREPARATION; HARDWARE NOT RUN.** Preparation complete / READY FOR OWNER REVIEW. No device access, protocol execution or persistent hardware operation. A009 hardware phase remains BLOCKED pending separate explicit owner approval; A010 NOT STARTED. A008 stays DONE / OWNER ACCEPTED, without reopening its limits or diagnosis. Firmware/source/SDK/bundles remain private; only the safe generated partition table and sanitized evidence are public.

## Exact candidate and installed-baseline comparison

The only partition CSV delta is:

```diff
+remote_ctl, data, nvs,     0xE20000, 0x10000,
```

| Partition | Type/subtype | Offset | Size | End exclusive | Existing record |
| --- | --- | --- | --- | --- | --- |
| nvs | 0x01/0x02 | 0x9000 | 0x6000 | 0xf000 | byte-identical |
| phy_init | 0x01/0x01 | 0xf000 | 0x1000 | 0x10000 | byte-identical |
| factory | 0x00/0x00 | 0x10000 | 0x800000 | 0x810000 | byte-identical |
| otadata | 0x01/0x00 | 0x810000 | 0x2000 | 0x812000 | byte-identical |
| ota_0 | 0x00/0x10 | 0x820000 | 0x300000 | 0xb20000 | byte-identical |
| ota_1 | 0x00/0x11 | 0xb20000 | 0x300000 | 0xe20000 | byte-identical |
| remote_ctl | 0x01/0x02 | 0xe20000 | 0x10000 | 0xe30000 | new |

All six complete32-byte records are byte-identical to accepted A006 CURRENT_PARTITIONS.bin, whose3072-byte SHA is `d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835`. A007 physically compared that artifact/padded4096-byte sector with the installed table, observed factory0x10000 and measured the target65536bytes allFF on physical16MiB flash. These are accepted historical measurements, not a fresh inspection. Candidate generation with selected IDF5.5.3 `gen_esp32part.py --flash-size 16MB --offset 0x8000` reproduces the approved A00664KiB candidate exactly; appended-entry MD5 and binary roundtrip verified.

Data offsets/sizes4KiB-aligned; app offsets64KiB-aligned; bootloader/table reserved region preserved; all seven ranges in16MiB/no overlaps. Both OTA slots remain3145728bytes. New partition ends at0xE30000, leaving1900544bytes unallocated through0x1000000. The table artifact is3072bytes, occupying sector0x8000â€“0x8FFF when written. Its six old entries stay192bytes unchanged; the MD5 position/value and table padding necessarily change after adding entry7.

Candidate CSV450bytes SHA `8c4b9d3561957750e89e7dab8bbebd523607c9a9c53428037595ef0edcbe4b33`; BIN3072bytes SHA `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`. Expected padded4096-byte sector SHA `fd62ef669cdbab98ac5372777a686d8dcd9813f7eb5302a67cc5136e96e90f69`. [Artifact hashes](../references/device_evidence/remote/A-REMOTE-009/ARTIFACT_SHA256.json); [record/bounds verification](../references/device_evidence/remote/A-REMOTE-009/TABLE_VERIFICATION.json).

## Current private inputs, tools and local build

Read current original source/configuration without editing them. The1613 accepted included files remain byte-unchanged after preparation. Of these1612 match the accepted Dell bundle; the sole current unselected changelog update was preserved. The14 host-only control test files omitted from that bundle are not selected by the configured target build. No selected input difference was found. The owner-accepted complete credential-component transfer exclusion is reused, not re-investigated; the original component is untouched and unexposed.

Current target ESP32-S3/project12_LVGL_Test/version1; remote01; PlatformIO6.2.0/espressif32 platform6.13.0, IDF5.5.3 framework3.50503.0, GCC14.2.0+20251107/binutils2.43.1, Python3.11.7. Build uses private copied pinned tools/runtime, fresh configuration and `python -m platformio run -e remote01 -j 1`, offline guards and a serial-access denial guard. No installed tool mutation. Effective config dictionary matches current original exactly, including16MiB/DIO80MHz/custom table0x8000/MD5 and disabled automatic OTA rollback. Only the disposable CSV is changed. Effective CMake database1449entries:1383C/49C++/17assembly,125 selected components. Selected project481 translation units contain no remote_ctl/named-partition NVS initialization/open/erase references; one default `nvs_flash_init` use. No new durable backend, named NVS initialization or API is implemented.

Clean serial build: **PASS**, 1 attempt(s), recorded exit codes and raw-log hashes in [build result](../references/device_evidence/remote/A-REMOTE-009/BUILD_RESULT.json); [compact sanitized log](../references/device_evidence/remote/A-REMOTE-009/CLEAN_BUILD_SANITIZED.log). Candidate partitions.bin from the build matches independent generation. Firmware ESP32-S3 chipID9/16MiB header, all segment bounds, checksum, appended SHA-256 and exact image length PASS; factory headroom5903024bytes. Firmware size: **2485584bytes**; OTA capacity3145728bytes each, headroom **660144bytes** per slot. Firmware/ELF/map/bootloader hashes are recorded but their private contents are not published. No build-byte reproducibility or exact installed A006 runtime equivalence is claimed; those accepted A008 limits remain non-blocking at the hobby/public-beta level. Maximum one extra clean retry is reserved only for a recognized intermittent Ryzen ICE; no exhaustive analysis is authorized.

## Unexecuted protocol, risk and decision

[Single owner hardware protocol](../protocols/A-REMOTE-009_USB_ROM_RECOVERY.md) identifies an exact current COM (UNKNOWN now; historicalCOM3 is not reused automatically), checks physical16MiB/security policy, makes two complete16MiB reads with equal SHA and a separate verified backup copy, and verifies current installed table/factory/blank OTA/erased target before requesting write approval. Recommended deployment is **table-only at0x8000**, preserving installed firmware, bootloader, OTA metadata and NVS. **No matching new firmware upload is required for the unused partition addition.** The generated private firmware is build evidence only. Whole-project upload and ota_data_initial writes are forbidden by the protocol.

Interruption during the table-sector erase/write can prevent normal boot. Recovery is manual ESP ROM USB download mode plus restoration of the complete verified prewrite backup at0x0 with header options kept, followed by whole-flash readback equality and owner-observed normal function. ROM/security/USB availability must be reconfirmed for the actual device; this preparation does not prove recovery, immunity to power loss, a backend's durability or automatic OTA rollback. No JTAG or industrial power-failure campaign.

Protocol PowerShell syntax:10/10 blocks parsed without executing any block. Offline verifier: synthetic accepted fixture PASS and four concrete safety mismatches rejected (table, non-erased target, OTA selection, wrong factory image). Synthetic16MiB fixture is NOT a device backup and must NEVER be used for recovery. [Validation](../references/device_evidence/remote/A-REMOTE-009/PROTOCOL_LOCAL_VALIDATION.json).

Next owner decision: review/accept this exact candidate and protocol, then separately authorize hardware read-only preflight. Stop again before any persistent operation and obtain explicit approval against the fresh complete-backup/preflight record for the table-only write and any complete-backup rollback. No A010/backend/API execution follows. CCM1.1.0 frozen; historical1.0.0 untouched; Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; O01â€“O17 and common gate OPEN/NOT PASSED. TUNER unchanged.
