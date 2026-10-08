# A-TUNER-001 baseline evidence

Captured (UTC): 2026-10-08T14:17:01Z  
Inspection only: no clean, build, upload, reset, NVS erase or hardware action was run.

## Checkout identity

Device checkout: `C:\Users\RYZEN\Downloads\InternetRadio_ESP32_EPaper\ESP32-WROVER-Internet radio`

```text
git status --short --branch
## main...origin/main

git rev-parse HEAD
371cdebce7ba2648ea71636d5bdb5d738b42e680

git log -1 --oneline
371cdeb Release v1.1.0
```

At inspection start the checkout was clean and `main` matched `origin/main`.
`src/config.h` declared `FIRMWARE_VERSION "1.1.0"`.

## Resolved configuration and installed packages

`platformio.ini` selects environment `esp32-dev`, board `esp32dev`, Arduino,
`espressif32@7.0.1`, `huge_app.csv`, PSRAM flags, the five exact registry
library versions, ESP32-A2DP commit
`3245602afc494f9e62160a0cfb2af864af45a37f`, ESP8266Audio commit
`058e131b26e459b9aadcb589a50f07877f1a09fd`, and the build-info/AAC patch
scripts.

The local PlatformIO executable reported Core 6.2.0. Dependency resolution
reported `Platform espressif32 @ 7.0.1 (required: espressif32 @ 7.0.1)` before
`pio pkg list` aborted while rendering Unicode tree characters to the cp1252
console. The exact installed platform metadata at
`.platformio/platforms/espressif32@7.0.1/platform.json` reports 7.0.1. The
installed framework package reports
`3.20017.241212+sha.dcc1105b`; the installed Xtensa package reports
`8.4.0+2021r2-patch5`. The seven expected library directories are present in
`.pio/libdeps/esp32-dev`. This inventory is not a build result.

The active built-in `huge_app.csv` contains:

```text
nvs      0x009000 0x005000
otadata  0x00e000 0x002000
app0     0x010000 0x300000 (ota_0 subtype; one application slot)
spiffs   0x310000 0x0e0000
coredump 0x3f0000 0x010000
```

`partitions/ota_4mb_proposed.csv` exists only as an inactive proposal.

## Existing build artifacts (historical, not rebuilt)

These files predated this inspection and all have UTC timestamps on
2026-09-27. Their presence and hashes do not prove which firmware is flashed.

| Artifact | Bytes | Last write UTC | SHA-256 |
| --- | ---: | --- | --- |
| `.pio/build/esp32-dev/firmware.bin` | 1,999,088 | 2026-09-27T09:50:03.3719139Z | `4E5CBC4851CC00778A964815F82C5BE6FF7D802372CE1B84F8FAA898D2AAEEB7` |
| `.pio/build/esp32-dev/firmware.elf` | 29,145,084 | 2026-09-27T09:50:02.8803936Z | `CA83E2149B786095733748AD2FA8293E781FD81FE0B237D0DDE84AEB19D604AD` |
| `.pio/build/esp32-dev/firmware.map` | 18,829,131 | 2026-09-27T09:50:02.8808957Z | `5E9E7A9494F5B32256A00CE2794187BC150B228318142CFEC0852E2A4BC00422` |
| `.pio/build/esp32-dev/partitions.bin` | 3,072 | 2026-09-27T09:48:32.3487632Z | `AAAE2888C5A6A348004B5B436F47ABB25AE32E72D9003902955A998EDA723EDD` |

Selected map sections from that existing ELF are `.dram0.data` 28,752 bytes,
`.dram0.bss` 54,296, `.iram0.vectors` 1,027, `.iram0.text` 125,363,
`.flash.rodata` 326,660 and `.flash.text` 1,510,703. ELF/map disk size includes
debug/link information and is not flash consumption.

## Runtime and physical evidence boundary

The repository changelog records an owner hardware regression on 2026-08-21
for the then-current V1 baseline and a 2026-09-27 encoder hardware test. This
task did not reproduce those tests. No current serial log was found or
captured as an immutable task artifact. The physical flash size, currently
flashed commit/binary, current heap/stack minima and long-run coexistence
margins therefore remain unknown in A-TUNER-001.
