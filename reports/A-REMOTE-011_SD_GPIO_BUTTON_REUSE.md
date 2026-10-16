# A-REMOTE-011 SD GPIO reuse for physical buttons

Date: 2026-10-15

## Verdict

GPIO38, GPIO39, GPIO40 and GPIO41 are each **SAFE WITH CONDITIONS** as independent active-low button inputs on the Waveshare ESP32-S3-Touch-LCD-3.49B V2 / PCB Rev1.1. No pin in the proposed group is unconditionally free: all four remain electrically connected to the microSD socket.

The approved configuration must keep the socket empty, must never initialize SDMMC/SDSPI, and must configure the four GPIOs only as inputs. Under those conditions, a normally-open contact from each J3 pad to GND is compatible with the board circuit.

## Electrical evidence

The official V2 schematic, SHA-256 `fc82f639dec6ecf9644634c4eba48fff52d9143d62f60aae6d83e9505b9469bf`, shows:

| GPIO / pad | SD socket signal | Board load | Verdict |
| --- | --- | --- | --- |
| GPIO38 / J3-8 | CS / DAT3 | R33, 10 kOhm to 3.3 V | **SAFE WITH CONDITIONS** |
| GPIO39 / J3-9 | CMD / MOSI | R35, 10 kOhm to 3.3 V | **SAFE WITH CONDITIONS** |
| GPIO40 / J3-10 | DAT0 / MISO | R36, 10 kOhm to 3.3 V | **SAFE WITH CONDITIONS** |
| GPIO41 / J3-11 | CLK | R34, 10 kOhm to 3.3 V | **SAFE WITH CONDITIONS** |

The socket supply has local 100 nF decoupling. DAT1 and DAT2 have unpopulated pull-up positions R38 and R37. The optional R27 link from SD_CS to GND is not populated. With no card inserted, the socket adds no active device load; the four fitted pull-ups establish the desired released-high state.

## Firmware and power-management evidence

The active private source defines GPIO38-41 as the board SD pins but contains no selected application call that initializes SDMMC, SDSPI or a filesystem mount. The project explicitly excludes its custom `sdcard_bsp` and `codec_board` components. ESP-IDF framework SD libraries appear in generated dependency metadata, but no application reference or linked runtime symbol was found that claims these four GPIOs.

GPIO38-41 are not ESP32-S3 strapping pins. Current boot logic does not configure them. Current light-sleep wake logic uses the shared expander interrupt on GPIO8 only. Reusing the SD nets as ordinary buttons therefore does not alter present boot or sleep/wake behavior, but these buttons will not wake the device under the current design.

## Required later software boundary

Any separately approved implementation must configure GPIO38-41 as input-only, active-low contacts with bounded debounce. The board's fitted 10 kOhm pull-ups are sufficient; internal pull-ups may be enabled but are redundant. Firmware must keep all SD host and mount paths disabled. It must not assign button actions until the owner approves the wiring and a later scoped task defines those actions.

No microSD card may be inserted while the buttons use these nets. A card would connect the same four signals to an active peripheral, and pressing a button could short a driven SD signal to ground.

## Proposed final wiring

| Control | Connection |
| --- | --- |
| Encoder A / S1 | GPIO2, J6-3 |
| Encoder B / S2 | GPIO5, J6-6 |
| Encoder common | GND, J6-9 |
| Encoder KEY | GPIO38, J3-8 to GND |
| Button 1 | GPIO39, J3-9 to GND |
| Button 2 | GPIO40, J3-10 to GND |
| Button 3 | GPIO41, J3-11 to GND |
| Button common | GND, preferably J3-3 |

GPIO1 external-power sensing and GPIO4 `BAT_ADC` remain unchanged. This investigation performed no source implementation, build, test, flash operation or hardware access.

## Sources

- [Official Waveshare V2 schematic](https://github.com/waveshareteam/ESP32-S3-Touch-LCD-3.49-V2/blob/main/schematic/ESP32-S3-Touch-LCD-3.49%20V2.pdf)
- [Waveshare V2 resources](https://docs.waveshare.com/ESP32-S3-Touch-LCD-3.49/Resources-And-Documents)
- Private source inspected without publication: root component exclusions, board pin definitions, selected application sources and power-management runtime.
