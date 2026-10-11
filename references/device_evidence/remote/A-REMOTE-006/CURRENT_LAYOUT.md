# A-REMOTE-006 current layout and authority
Input authoritative main00d190a7484aa76185c47b7185c0c7f9a1854711; published assignment `81d7d2f4d2c3d7625d6c6f5618785ffd90b93940`. Entire CCM1.1.0, D-006/owner approval, A005 report and180 capacity cases read. No TUNER files/config used. Source workspace C:/Users/RYZEN/Documents/REMOTE01/Code is root Git-less; no repository initialized. Original4036-file inventory and selectedSDK hashes checked before/after, unchanged. No build/device access performed.

## Classified facts
| Fact | Classification | Evidence / qualification |
| --- | --- | --- |
| PlatformIO environment remote01; espressif32@6.13.0; ESP-IDF / framework-espidf@3.50503.0; toolchain14.2.0+20251107 | VERIFIED FROM BUILD plus CONFIGURED ONLY for next invocation | platformio.ini, project_description selected compiler/idf_path/git_revision5.5.3, build.ninja selected utility; ELF-linked BIN descriptor5.5.3. Separate6.0.1 not selected |
| Board esp32-s3-devkitc-1 | CONFIGURED ONLY | Board JSON default N8/8MB/QIO vs project16MB override and actual generated DIO config; board name is not physical board/flash evidence |
| Flash16MB, DIO80MHz, partition-table offset0x8000 | VERIFIED FROM BUILD/ARTIFACT as configured image metadata | sdkconfig.remote01 + generated config/header + flash_args; app/boot image headers size nibble4,mode2,freq15; not a physical measurement |
| Actual flash capacity/JEDEC/chip/installed offsets | REQUIRES DEVICE EVIDENCE | No serial/flash_id/readback/eFuse inspection performed; physical size UNKNOWN |
| Effective CSV partitions.csv | VERIFIED FROM BUILD | build.ninja exact source/generator5.5.3; selected sdkconfig custom filename |
| Existing .pio/build/remote01/partitions.bin3072 bytes | VERIFIED FROM ARTIFACT | selected SDK gen_esp32part decode; sourceCSV regenerated full binary BYTE IDENTICAL including MD5/padding, published snapshots |
| Application2485824 bytes, project12_LVGL_Test/version1, IDF5.5.3, Oct6 build | VERIFIED FROM ARTIFACT | esptool4.11.0 local image_info validates checksum/digest. No installed-firmware assertion |
| Local ELF/BIN pairing | VERIFIED FROM ARTIFACT | BIN embedded ELF SHA61d077235a971919807bcff38aede169554f60de1ea7152625e5aa5b0b730525 equals actual firmware.elf SHA; source-to-BIN and flashed residency UNKNOWN |
| Bootloader20832 bytes at configured0x0 | VERIFIED FROM ARTIFACT / BUILD | local bootloader.bin validated; table reservation0x8000 means11936 bytes arithmetic headroom. Bootloader physically installed UNKNOWN |
| OTA metadata0x810000/8KiB; blank initial8192 bytes FF | VERIFIED FROM ARTIFACT | generated ota_data_initial.bin, not device metadata; does not prove current boot slot or rollback state |
| Automatic bootloader rollback disabled | VERIFIED FROM BUILD | sdkconfig.remote01 CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE not set; no automatic health-confirmation/fallback guarantee |
| Six current partition definitions, flags0, no NVS keys/filesystem/coredump/custom storage | VERIFIED FROM ARTIFACT | decoded table; coredump flash disabled in config. Other data physically in unallocated tail UNKNOWN |
| PHY partition present; PHY init data in partition not enabled | VERIFIED FROM BUILD/ARTIFACT | reserved4KiB retained; do not erase calibration/default NVS |
| remote_wifi credentials route nvs / remote_wifi / credentials | INFERRED from verified source and selected SDK API | runtime.cpp nvs_flash_init+nvs_open; SDK nvs_open delegates NVS_DEFAULT_PART_NAME nvs; source Blob108. Actual saved credentials/namespace contents UNKNOWN, never read/published |
| Current control state | INFERRED from source; runtime UNKNOWN | Journal interface with MockJournal in control_profile/control_home; no persistent control backend or control namespace defined. Candidate remote_ctl partition/control namespace would be future code, not existing state |
| Assets/filesystem location | INFERRED | no flash filesystem partition in artifact; UI/assets are compiled application or separate SD component, no physical external storage inspection |

## Exact current partition table
| Label | Type/subtype | Offset | Size hex / KiB | End exclusive | Alignment |
| --- | --- | --- | --- | --- | --- |
| nvs | data/nvs (1/2) | 0x9000 | 0x6000 / 24 | 0xF000 | 4KiB |
| phy_init | data/phy (1/1) | 0xF000 | 0x1000 / 4 | 0x10000 | 4KiB |
| factory | app/factory (0/0) | 0x10000 | 0x800000 / 8192 | 0x810000 | 64KiB |
| otadata | data/ota (1/0) | 0x810000 | 0x2000 / 8 | 0x812000 | 4KiB |
| ota_0 | app/ota_0 (0/16) | 0x820000 | 0x300000 / 3072 | 0xB20000 | 64KiB |
| ota_1 | app/ota_1 (0/17) | 0xB20000 | 0x300000 / 3072 | 0xE20000 | 64KiB |

Bootloader0x0..0x8000 reservation and primary table0x8000..0x9000 are implicit (not CSV entries). Table binary3072 fits its4096-byte sector;1024 padding/reserved bytes are not independent storage. Gap after otadata0x812000..0x820000 is57344 bytes. Allocated partition end0xE20000; configured16MiB tail0xE20000..0x1000000 is1966080 bytes (1920KiB), not verified physically free flash. Never place64KiB before ota_0: gap only56KiB;48KiB there would fit arithmetic but preferred append-at-tail avoids interfering with existing addressing.

OTA slot size0x300000=3145728 bytes (3072KiB) each; combined6MiB. Effective dual-OTA firmware ceiling is the smaller slot3145728, not board maximum8MiB or factory8MiB. Local image2485824 =>659904 bytes644.4375KiB headroom per OTA slot,20.9778% slot /26.547% current image. Factory0x800000 =>5902784 bytes headroom; a factory-fitting image may still be impossible to OTA. These margins exclude future secure-signature/alignment/update-framework overhead and future code growth. Physical installed active slot/end-of-image UNKNOWN.

## Discrepancies retained explicitly
Board default8MB/QIO differs from effective configured16MB/DIO; selected flash args/image agree with16MB/DIO80m. sdkconfig.defaults header5.3.2 and root sdkconfig header5.5.4 are historical/unselected; actual SDK5.5.3 sdkconfig.remote01/generated config/app descriptor authoritative for this build. Existing CMake/flash files name12_LVGL_Test.bin/.elf, partition_table/partition-table.bin and bootloader/bootloader.bin, but those paths are absent; PlatformIO outputs firmware.bin/.elf, partitions.bin, bootloader.bin exist. This is observed path/provenance divergence, not an upload command or proof the missing paths can be used. CSV/binary exact agreement and ELF/BIN pairing verified independently. No fresh build was necessary or run. A005 source/build inventories still match, no retrospective acceptance upgrade. Local docs/CCM1.0.0 copies are historical; coordination1.1.0 is current contract.
