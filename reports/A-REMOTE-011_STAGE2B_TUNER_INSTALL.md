# A-REMOTE-011 Stage 2B: TUNER application installation

## Result

**PASS — TUNER PHASE 3 APPLICATION INSTALLED AND OWNER-CONFIRMED; PAIRING NOT STARTED.**

The TUNER-only Stage 2B operation used public source commit `18ddd3b16e305341f338afebd7dc725500ecbb73`. The device was positively identified through its classic ESP32 ROM interface as the Stage 1 device with 4 MiB physical flash. REMOTE was not accessed or modified.

## Candidate and rollback checks

- Candidate size: 2,034,800 bytes (`0x1F0C70`).
- Candidate SHA-256: `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4`.
- Source commit, size and hash matched the accepted Phase 3 evidence exactly.
- The verified Stage 1 rollback span remained available: 2,034,800 bytes, SHA-256 `4dc7347191a38a18fe76b1635b446a485443ac6d06406bb6f53d303cd105b88a`.
- Full-flash and rollback-critical backups had already been preserved on separate physical USB storage.

## Write and independent readback

The ROM/stub interface was stable at 921600 baud. Exactly one application write was issued at `0x10000` with flash mode, frequency and size set to `keep`. The only image argument was the authorized TUNER candidate. Esptool necessarily erased the covering application sectors `0x10000–0x200FFF`, wrote the `0x1F0C70` candidate bytes through `0x200C6F`, and reported successful write-time data-hash verification. No retry or rollback occurred.

The independent readback covered exactly `0x10000–0x200C6F`:

- readback size: 2,034,800 bytes;
- readback SHA-256: `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4`;
- candidate/readback equality: PASS.

The bootloader, partition table, OTA metadata and application UART settings were not changed.

## Default-NVS investigation

The post-boot default-NVS hash differed from the Stage 1 capture. The owner stopped Stage 2B and authorized an offline comparison of the two existing private captures. No additional hardware read was performed.

The comparison found exactly 29 changed bytes in one 4 KiB NVS page. All bit transitions were `1→0`; there was no page erase or compaction. The changes converted one empty slot into one valid, CRC-checked `uint32` entry in the existing framework `dhcp_state` namespace for the default Wi-Fi station interface. No pre-existing entry bytes changed.

The stored Wi-Fi configuration, stations, favorites, recent items, timezone and other existing records remained byte-identical. The `remote_pair` namespace was absent in both captures. The TUNER RTCP implementation opens pairing storage read-only. The owner accepted this single append-only DHCP-state record as legitimate ordinary networking-stack persistence and explicitly determined that it was no longer a blocker. NVS was not restored.

## Owner functional confirmation

The owner confirmed that TUNER works correctly after installation, covering the requested Stage 2B checklist:

- normal UI and physical controls: PASS;
- previously stored Wi-Fi configuration: PASS;
- MP3 radio playback: PASS;
- Bluetooth A2DP playback: PASS;
- web manager, including while Bluetooth is active: PASS;
- stations, favorites and recent items: PASS.

Because no `remote_pair` namespace exists, `loadPairing()` cannot enable the RTCP listener. The unpaired RTCP server remains disabled and did not accept a control connection.

## Scope and next gate

No PSK was generated, pairing was not provisioned, no RTCP control command was issued, and REMOTE was not modified. Stage 2B is complete at the approved practical hobby/public-beta level.

Stage 3 pairing remains unauthorized and additionally requires the separately reviewed private commissioning helper identified in the Phase 4 procedure. PR #17 remains open and unmerged.
