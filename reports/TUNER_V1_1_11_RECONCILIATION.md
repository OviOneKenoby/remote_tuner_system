# Current TUNER v1.1.11 reconciliation
Reviewed 2026-10-11T17:37:47Z; coordination input `531aa8cd0435ed9813ab39664888992583df0d28`. [Owner scope](../references/PM_RECONCILIATION_SCOPE_2026-10-11.md). This supersedes the baseline in historical [A-TUNER-003](A-TUNER-003.md); its old 1,999,408-byte BIN and reports remain unchanged historical evidence.

## Exact current identity
- [Firmware PR5](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/pull/5) MERGED; main/tag v1.1.11/merge `5fb92c95d228d744d1182ae3956e850c5be2f277`, independently checked with metadata and git ls-remote.
- Executable validated source `124e84801b06f9e07764dabc3985a573dffaff3b`; build_git_id `124e84801b06`.
- [Final release](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/releases/tag/v1.1.11): published 2026-10-11T17:10:33Z, draft=false, prerelease=false.
- Explicit PlatformIO `esp32-lwip-psram`; validated firmware `1.1.11-psram-validation`. Default `esp32-dev` remains and is not this selected release profile.
- BIN `firmware-1.1.11-psram-124e84801b06.bin`, 2,028,672 bytes, SHA256 `796221b3521800eb5d6e41f6932c81f600ea9f6e57e9bbc240640c9e8522dbf2`.
- ELF `firmware-1.1.11-psram-124e84801b06.elf`, 29,599,964 bytes, SHA256 `c1bc29571b7ac59d12bab006ec0761464cebb4c76e7f14686606c73866f7c209`.

## Verification and accepted scope
[Evidence index](../references/pm/2026-10-11/INDEX.md) contains all five downloaded asset SHA checks and pinned reports. Production-selected source/config unchanged from executable source to release merge. Comparison also adds two host verification scripts tools/test_lwip_psram_policy.py and tools/verify_lwip_psram_elf.py plus validation artifacts/changelog; these were not introduced by this publisher. Historical build SUCCESS 242.32s, RAM 85,936 and flash 2,022,097 bytes are executor evidence, not a PM build.

Owner accepted functional PASS for Bluetooth SBC audibility, web/diagnostics, continuous ping and recovery, with lwIP >=512-byte allocations routed to PSRAM and original fallback. Two independent boots use the same BIN/ELF. Each has three transient 1622-byte DMA failures; no persistent NO_MEM, headNULL or retained pbuf refs; TX/ref/free resume balanced. TEST01: 377 ping replies/no loss, final 438/438/438, recovery observation 123.010s. SUSTAINED01: 224 replies/no loss, final 463/463/463, conversion resumes within 4.016s.

Strict zero-DMA-failures criterion **FAIL**. SUSTAINED01 ping window **3m44.566s**, not 30-minute soak. Current local flashed residency and exact wiring not re-inspected by PM; NOT VERIFIED. Endurance/resources outside observed windows UNKNOWN. Candidate BUILD_MANIFEST OPEN headers are historical and superseded by final validation, retained unchanged.

## Functional gaps
B01/B03/B06 and B04 empty/stale physical cases remain PENDING; BT/network/web evidence is not their exact case proof. Full B04 identity and B02/B05/B07-B11 unresolved/outside scope. A-TUNER003 software integration/artifact preparation reviewed/delivered, distinct from incomplete physical matrix.

CCM 1.0.0 OWNER APPROVED/FROZEN; Native v1 UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; O01-O17 OPEN; common gate OPEN/NOT PASSED. No firmware edit/release/build/flash by PM.
