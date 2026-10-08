# A-TUNER-002 build and test evidence

Date (UTC): 2026-10-08
Firmware commit: `8fac1da6ccd749a47843d99dc746fc3d6e4bf19b`
Isolated checkout: `C:\Users\RYZEN\AppData\Local\Temp\a-tuner-002-build-8fac1da`

## Deterministic host tests

Compiler: MSYS2 UCRT64 GCC 16.2.0.

```text
g++ -std=c++17 -Wall -Wextra -Werror -Isrc tests/test_correctness_guards.cpp
PASS: 249 deterministic correctness checks
exit: 0
```

Coverage executed against production headers:

- empty, signed, spaced, junk, overlong, overflow and `256` DELETE suffixes;
- `255` conversion boundary and actual-count boundaries;
- rejected DELETE leaves the modeled list byte-for-byte unchanged;
- valid index removal including index zero;
- zero/one/many and stale-index Next/Previous;
- every integer volume from 0 through 100, including 1–4 and zero;
- opaque AAC, opaque MP3 and case-insensitive `.aac` correction;
- persisted/reloaded opaque AAC codec through the production codec resolver.

## Clean isolated PlatformIO build

The first dependency fetch stalled while cloning the pinned A2DP repository and
was cancelled before compilation. The isolated checkout was then seeded with
copies of the already resolved local dependency directories. Git identity was
verified before use:

```text
ESP32-A2DP    3245602afc494f9e62160a0cfb2af864af45a37f
ESP8266Audio  058e131b26e459b9aadcb589a50f07877f1a09fd
```

`pio run -e esp32-dev -t clean` passed, then `pio run -e esp32-dev` rebuilt all
objects in the isolated worktree and passed:

```text
PlatformIO Core 6.2.0
Platform espressif32 7.0.1
Board esp32dev; Arduino framework
framework-arduinoespressif32 3.20017.241212+sha.dcc1105b
toolchain-xtensa-esp32 8.4.0+2021r2-patch5

RAM:   83,056 / 327,680 bytes (25.3%)
Flash: 1,992,833 / 3,145,728 bytes (63.4%)
SUCCESS in 136.93 seconds
```

Libraries resolved:

```text
GxEPD2 1.6.9
Adafruit GFX 1.12.6
Adafruit BusIO 1.17.4
Bounce2 2.72.0
ArduinoJson 7.4.3
ESP32-A2DP 1.8.11+sha.3245602
ESP8266Audio 2.2.0+sha.058e131
```

Warnings were limited to the existing ESP32-A2DP optional AudioTools warning
and the two existing `ADC_ATTEN_DB_11` framework deprecation warnings.

## Artifacts

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `firmware.bin` | 1,999,408 | `AF066BA215F863A7D2583A6313ACEE00020CCFAD4F8F8C3168DEDA76BCD6F5D4` |
| `firmware.elf` | 29,151,308 | `8B44B12174E3647D5A0E12011FF3FE8EC2D0DAAFF5191645A62B2A32B5421881` |
| `firmware.map` | 18,831,130 | `63EABF93DEF9A3ACCFD9805B8CFB92EDE093A7A25203F4EDF1677D61137491D3` |
| `partitions.bin` | 3,072 | `AAAE2888C5A6A348004B5B436F47ABB25AE32E72D9003902955A998EDA723EDD` |

No platform, dependency pin, partition, GPIO or firmware version changed.
Upload, flashing, reset, NVS erase and physical hardware tests: **NOT RUN**.
