# A-TUNER-003 integration and artifact evidence

Date (UTC): 2026-10-08T17:53:04Z

## Execution identities

- Absolute coordination checkout: `C:\Users\RYZEN\.codex\.chatgpt-projects\g-p-6a7e93a34018819180def7348d65b3fd\remote_tuner_system`
- Coordination execution input: `531aa8cd0435ed9813ab39664888992583df0d28`
- Firmware checkout: `C:\Users\RYZEN\Downloads\InternetRadio_ESP32_EPaper\ESP32-WROVER-Internet radio`
- Firmware PR #2 reviewed head: `8fac1da6ccd749a47843d99dc746fc3d6e4bf19b`
- PR #2 base before merge: `371cdebce7ba2648ea71636d5bdb5d738b42e680`
- Ordinary software merge: `d1e51765179f99567df3b5d18a451152adac514c`
- Reviewed and software-merge tree: `01a23382bf54be3e1a04fa992984e62c4570be8d`
- Documentation/artifact commit: `315e5528562ac0dd3eff325e3412dde3a9a8fc2a`
- Documentation-only PR #3 merge / final firmware main: `cb17e945b9c0e086a03e7176d9ad442a8c78d89b`
- Firmware version: 1.1.0, unchanged

The live firmware worktree was clean at the reviewed PR head at start. Remote
`main` still matched the assigned base. PR #2 was open, non-draft, mergeable
and clean, with exactly two commits and ten reviewed changed paths. GitHub had
no configured check runs/status contexts; the documented deterministic and
isolated build evidence therefore remained the actual software gate.

## Final source/call-path review

| Scope | Inspected production path | Result and boundary |
| --- | --- | --- |
| B01 DELETE | `WebPortal::onNotFound` prefix routing; both delete handlers; `parseListIndex`; `removeStation`/`removeFavorite` | PASS for code integration. Full nonempty ASCII decimal parsing occurs before narrowing/mutation; signs, spaces, junk, overlength, overflow, index equal/above live count reject. HTTP/NVS behavior remains physically PENDING. |
| B04 empty/stale traversal | `handlePlayingInput`; `nextStationIndex`; `previousStationIndex`; `playStation` bounds | PASS for bounded scope. Zero/stale lists log and no-op before modulo/subtraction/playback. Durable identity and active deletion semantics remain outside scope. |
| B06 volume | radio and Bluetooth encoder paths; `AudioPlayer::volumeDown`; `setVolume` | PASS for code integration. Values 1–5 saturate to zero and zero stays unchanged; real radio/BT behavior remains PENDING. |
| B03 codec | Browse/Recent/Favorite entry points; `playDiscoveredStation`; value-owned `CurrentStationContext`; playing-screen Favorite; `addToFavorites`; NVS save/load; `stationCodecForURL`; audio codec selection | PASS for code integration. Supplied AAC survives opaque URLs and NVS representation; legacy MP3 upgrades only on explicit case-insensitive `.aac`. Actual storage/reboot/decoder/audio remains PENDING. |
| Prior fixes | decoder lifetime, Recent copy, metadata synchronization, Bluetooth reporting, HTTPS EOF and current configuration diff | No conflicting change found. No unrelated correction made. |

`git diff 8fac1da6..d1e5176` showed identical trees. The only paths added after
the software merge were `CHANGELOG.md` and `artifacts/A-TUNER-003/*`; a scoped
diff through final `main` showed no change under `src`, `tools`, `tests`,
`platformio.ini` or partition configuration.

## Reused software/build evidence

The executable input did not change, and the exact original build artifact was
available. Per A-TUNER-003, the verified A-TUNER-002 evidence was reused rather
than replacing it with a needless rebuild:

- MSYS2 UCRT64 GCC 16.2.0 host suite: PASS, 249 checks.
- Independent PM Ubuntu GCC 13.3.0 host suite: PASS, 249 checks.
- Isolated PlatformIO clean/build: PASS, 136.93 seconds.
- PlatformIO Core 6.2.0, espressif32 7.0.1, Arduino package
  3.20017.241212+sha.dcc1105b, Xtensa 8.4.0+2021r2-patch5.
- RAM 83,056 / 327,680 bytes (25.3%); linked flash 1,992,833 / 3,145,728
  bytes (63.4%).

An optional A-TUNER-003 MSYS2 host recompile attempt returned from `cc1plus`
with status 1 before linking and emitted no source diagnostic. No test binary
ran, so this attempt is recorded as NOT RUN / no verdict, not FAIL or PASS. It
did not replace the two immutable prior PASS results and did not justify a new
artifact because reviewed executable bytes were unchanged.

## Exact recovered artifact

Source directory:
`C:\Users\RYZEN\AppData\Local\Temp\a-tuner-002-build-8fac1da\.pio\build\esp32-dev`

The isolated checkout HEAD remained exactly
`8fac1da6ccd749a47843d99dc746fc3d6e4bf19b` and was clean/detached.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `firmware.bin` | 1,999,408 | `AF066BA215F863A7D2583A6313ACEE00020CCFAD4F8F8C3168DEDA76BCD6F5D4` |
| `firmware.elf` | 29,151,308 | `8B44B12174E3647D5A0E12011FF3FE8EC2D0DAAFF5191645A62B2A32B5421881` |
| `firmware.map` | 18,831,130 | `63EABF93DEF9A3ACCFD9805B8CFB92EDE093A7A25203F4EDF1677D61137491D3` |
| `partitions.bin` | 3,072 | `AAAE2888C5A6A348004B5B436F47ABB25AE32E72D9003902955A998EDA723EDD` |
| `bootloader.bin` | 17,568 | `5B1B0CD6BCBFD6DE6D388652A46E9B6E341F36ADB9127D1E654D21DADEAE74BD` |

Only `firmware.bin` is the owner-regression app asset. It embeds build ID
`8fac1da6ccd7`; the ordinary merge commit has the identical reviewed tree.

## Public artifact route and readback

- Non-production prerelease: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/releases/tag/a-tuner-003-regression-8fac1da
- Binary: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/releases/download/a-tuner-003-regression-8fac1da/firmware.bin
- Manifest: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/releases/download/a-tuner-003-regression-8fac1da/SHA256SUMS.txt
- Checklist: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/blob/cb17e945b9c0e086a03e7176d9ad442a8c78d89b/artifacts/A-TUNER-003/OWNER_REGRESSION_CHECKLIST.md

GitHub release ID 407112224 is `prerelease=true`, `draft=false`, targets exact
commit `8fac1da6ccd749a47843d99dc746fc3d6e4bf19b`, and has three assets. A fresh
public download of `firmware.bin` was read back as 1,999,408 bytes with the
expected SHA-256. The fetched tag resolves to the same tested source commit.
This is not a production release.

## Configuration retained

- Board/target: `esp32dev`, classic ESP32-WROVER, PSRAM flags, 240 MHz CPU,
  80 MHz DIO flash.
- Partition: framework `huge_app.csv`; NVS `0x9000/0x5000`, OTA data
  `0xe000/0x2000`, app0 `0x10000/0x300000`, SPIFFS and coredump unchanged.
- GPIO: e-paper 5/18/23/19/21/4; I2S 26/25/33; buttons 34/35/39; encoder
  13/32/14.
- Libraries: GxEPD2 1.6.9, Adafruit GFX 1.12.6, BusIO 1.17.4, Bounce2
  2.72.0, ArduinoJson 7.4.3, ESP32-A2DP
  `3245602afc494f9e62160a0cfb2af864af45a37f`, ESP8266Audio
  `058e131b26e459b9aadcb589a50f07877f1a09fd`.

## Hardware boundary

Upload, flashing, serial interaction, reboot, reset, NVS erase and physical
testing were NOT RUN by the executor. Actual flashed identity is UNKNOWN.
Every owner matrix row remains PENDING until the exact artifact/date,
diagnostics build ID, serial log, HTTP before/after evidence, physical result
and restoration record are returned. A successful physical matrix may support
only B01, B03, B04 empty/stale traversal and B06; it cannot close full B04,
other B items, Native/API decisions, O01–O17 or the common gate.
