# Candidate layouts (proposals only)
**Recommend A64KiB**, conditional upon physical16MiB/actual layout/tail-use proof and separately qualified partition-table deployment/rollback. Appending a dedicated data/nvs label remote_ctl at0xE20000 uses only configured unallocated tail. It changes no existing slot or partition extent and leaves OTA headroom intact.48KiB minimum is fallback only, not chosen because ideal capacity fits. C current is a negative witness, FAIL as recommended dedicated control storage.

## A_64KiB

| Label | Type/subtype | Offset | Size hex / KiB | End exclusive | Alignment |
| --- | --- | --- | --- | --- | --- |
| nvs | data/nvs (1/2) | 0x9000 | 0x6000 / 24 | 0xF000 | 4KiB |
| phy_init | data/phy (1/1) | 0xF000 | 0x1000 / 4 | 0x10000 | 4KiB |
| factory | app/factory (0/0) | 0x10000 | 0x800000 / 8192 | 0x810000 | 64KiB |
| otadata | data/ota (1/0) | 0x810000 | 0x2000 / 8 | 0x812000 | 4KiB |
| ota_0 | app/ota_0 (0/16) | 0x820000 | 0x300000 / 3072 | 0xB20000 | 64KiB |
| ota_1 | app/ota_1 (0/17) | 0xB20000 | 0x300000 / 3072 | 0xE20000 | 64KiB |
| remote_ctl | data/nvs (1/2) | 0xE20000 | 0x10000 / 64 | 0xE30000 | 4KiB |

Unallocated configured tail:0x1D0000 / 1856KiB. OTA slots unchanged3072KiB each; max firmware3145728 bytes, current headroom659904 bytes(20.9778%). Factory remains8192KiB. Moved/resized partitions:NONE. Existing NVS/Wi-Fi/PHY/app/otadata addresses and lengths unchanged. Bytes affected by future deployment: primary table sector0x8000..0x9000, plus new remote_ctl region only (not authorized/applied); C changes NONE. Old firmware can parse extra data/nvs entry in principle; old firmware control-history compatibility is NOT VERIFIED and unsafe after authority cutover without a qualified bridge. Return-to-old-table is never the operational rollback method after cutover. Data migration risks include unknown physical tail contents, single-sector table update, schema authority, and stale legacy control state. Verdict:CONDITIONAL; configured math PASS is not device PASS.

## B_48KiB

| Label | Type/subtype | Offset | Size hex / KiB | End exclusive | Alignment |
| --- | --- | --- | --- | --- | --- |
| nvs | data/nvs (1/2) | 0x9000 | 0x6000 / 24 | 0xF000 | 4KiB |
| phy_init | data/phy (1/1) | 0xF000 | 0x1000 / 4 | 0x10000 | 4KiB |
| factory | app/factory (0/0) | 0x10000 | 0x800000 / 8192 | 0x810000 | 64KiB |
| otadata | data/ota (1/0) | 0x810000 | 0x2000 / 8 | 0x812000 | 4KiB |
| ota_0 | app/ota_0 (0/16) | 0x820000 | 0x300000 / 3072 | 0xB20000 | 64KiB |
| ota_1 | app/ota_1 (0/17) | 0xB20000 | 0x300000 / 3072 | 0xE20000 | 64KiB |
| remote_ctl | data/nvs (1/2) | 0xE20000 | 0xC000 / 48 | 0xE2C000 | 4KiB |

Unallocated configured tail:0x1D4000 / 1872KiB. OTA slots unchanged3072KiB each; max firmware3145728 bytes, current headroom659904 bytes(20.9778%). Factory remains8192KiB. Moved/resized partitions:NONE. Existing NVS/Wi-Fi/PHY/app/otadata addresses and lengths unchanged. Bytes affected by future deployment: primary table sector0x8000..0x9000, plus new remote_ctl region only (not authorized/applied); C changes NONE. Old firmware can parse extra data/nvs entry in principle; old firmware control-history compatibility is NOT VERIFIED and unsafe after authority cutover without a qualified bridge. Return-to-old-table is never the operational rollback method after cutover. Data migration risks include unknown physical tail contents, single-sector table update, schema authority, and stale legacy control state. Verdict:CONDITIONAL; configured math PASS is not device PASS.

## C_CURRENT

| Label | Type/subtype | Offset | Size hex / KiB | End exclusive | Alignment |
| --- | --- | --- | --- | --- | --- |
| nvs | data/nvs (1/2) | 0x9000 | 0x6000 / 24 | 0xF000 | 4KiB |
| phy_init | data/phy (1/1) | 0xF000 | 0x1000 / 4 | 0x10000 | 4KiB |
| factory | app/factory (0/0) | 0x10000 | 0x800000 / 8192 | 0x810000 | 64KiB |
| otadata | data/ota (1/0) | 0x810000 | 0x2000 / 8 | 0x812000 | 4KiB |
| ota_0 | app/ota_0 (0/16) | 0x820000 | 0x300000 / 3072 | 0xB20000 | 64KiB |
| ota_1 | app/ota_1 (0/17) | 0xB20000 | 0x300000 / 3072 | 0xE20000 | 64KiB |

Unallocated configured tail:0x1E0000 / 1920KiB. OTA slots unchanged3072KiB each; max firmware3145728 bytes, current headroom659904 bytes(20.9778%). Factory remains8192KiB. Moved/resized partitions:NONE. Existing NVS/Wi-Fi/PHY/app/otadata addresses and lengths unchanged. Bytes affected by future deployment: primary table sector0x8000..0x9000, plus new remote_ctl region only (not authorized/applied); C changes NONE. Old firmware can parse extra data/nvs entry in principle; old firmware control-history compatibility is NOT VERIFIED and unsafe after authority cutover without a qualified bridge. Return-to-old-table is never the operational rollback method after cutover. Data migration risks include unknown physical tail contents, single-sector table update, schema authority, and stale legacy control state. Verdict:FAIL as dedicated-control recommendation; configured math PASS is not device PASS.

## Real-layout capacity recalculation
Selected NVS126 entries per4096-byte page,32-byte entries. P4 pending5587/resolved6383 bytes, proof growth796. Old/new BASE6447*2, PROOF1146*2, ALLOC162*2 =15510 bytes; old/new76-byte roots152; mandatory logical peak15662. Partial512-byte chunk entry bound BASE432+PROOF80+ALLOC16+root10=538. Dedicated metadata32+GC126+stranded fragmentation252 =>948 entries. remote_wifi remains in original24KiB nvs, so no Wi-Fi migration or274 external entries in dedicated pool. Its old/new108-byte schema12 entries belong to separate756-entry pool; other real default-NVS occupants/stats UNKNOWN. No double-count of GC/metadata/fragmentation with payload. Persistent journal does not yet exist; source-level bounds are not real NVS capacity measurements.

| Pool | Entries | Previous conservative1222 margin / %pool | Dedicated948 margin / %pool |
| --- | --- | --- | --- |
| Current24KiB |756|-466 / -61.64%|-192 / -25.40% (hypothetical dedicated negative witness; current Wi-Fi shares pool) |
| Candidate48KiB |1512|290 /19.18%|564 /37.30% |
| Candidate64KiB |2016|794 /39.38%|1068 /52.98% |

Retain the1222 envelope as conservative policy/contingency rather than assigning Wi-Fi to control storage.64KiB has794 entries25408 byte margin even under that envelope, and1068 entries34176 under separated948 accounting.48KiB has290/564 entries9280/18048 bytes. No shrink of existing OTA is needed to choose64, so64 preferred. Quotas/codec/proof retention and actual page allocation/GC/endurance/latency remain BLOCKED for production. Full broader A00344284-byte two-bank payload lower bound88568 plus metadata still FAIL at64KiB; P4 lossless limits/refusal unchanged, no mandatory data dropped.

## Exact future diff (NOT APPLIED)
Preferred [A64 patch](A_64KiB.patch) adds exactly `remote_ctl, data, nvs, 0xE20000, 0x10000,` to current partitions.csv. [B48 patch](B_48KiB.patch) alternatively uses0xC000. Existing CSV lines/offsets unchanged. [Candidate CSVs/binaries](LAYOUT_MEASUREMENTS.json) were generated/validated only in a temporary directory with selected SDK5.5.3 utility; candidate BINs are proposals, never flashed. platformio.ini diff:NONE; sdkconfig/defaults diff:NONE for layout proposal. Future durable backend APIs/namespace and rollback-enabled bridge firmware require separate code/design tasks; CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE is not silently turned on here.

Selected utility validates alignment/nonoverlap/16MB bounds for all three. Application offsets64KiB aligned; data offsets/sizes4KiB aligned. Physical capacity, active slot, bootloader/table installed version and all tail data still REQUIRES DEVICE EVIDENCE. Neither64 nor48 is a production PASS. See [migration](MIGRATION_AND_ROLLBACK.md) for the primary table atomicity blocker.
