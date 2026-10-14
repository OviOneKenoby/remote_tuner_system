# REMOTE//01 GPIO map

Date: 2026-10-14
Board: Waveshare ESP32-S3-Touch-LCD-3.49B V2, PCB Rev1.1

## Evidence and status vocabulary

This map combines the official Waveshare V2 schematic and interface table with the current private production firmware. Waveshare identifies PCB `Rev1.1` as V2 and documents two 11-pad, 2.54 mm expansion rows. The official schematic used for this review has SHA-256 `fc82f639dec6ecf9644634c4eba48fff52d9143d62f60aae6d83e9505b9469bf`.

- **CONFIRMED USED**: connected by the V2 schematic and used by current production firmware or established owner hardware.
- **CONFIRMED BOARD FUNCTION**: connected by the V2 schematic; the related production feature may be dormant.
- **CANDIDATE FREE**: direct expansion pad, no other onboard function shown in the V2 schematic, no current production claim, and not an ESP32-S3 strapping pin.
- **OWNER SELECTED / PENDING**: proposed use; no wiring or firmware activation has occurred.
- **UNKNOWN**: the reviewed evidence does not establish availability.

## Expansion-pad identification

Pin numbers follow the `J3` and `J6` pin-1 markers in the official V2 schematic and PCB silkscreen. The owner must confirm the physical pin-1 orientation before soldering.

| Pad | Net | Status and function |
| --- | --- | --- |
| J6-1 | GPIO0 | CONFIRMED BOARD FUNCTION: BOOT0 and ESP32-S3 strapping pin; unavailable for encoder use. |
| J6-2 | GPIO1 | CONFIRMED USED: owner-installed external-power ADC sensing. |
| J6-3 | GPIO2 | CANDIDATE FREE: direct MCU GPIO breakout; no other V2 schematic load or production claim found. |
| J6-4 | GPIO3 | CONFIRMED BOARD FUNCTION: direct breakout, but ESP32-S3 strapping pin; unavailable for encoder use. |
| J6-5 | GPIO4 | CONFIRMED USED: `BAT_ADC`, ADC1 channel 3. |
| J6-6 | GPIO5 | CANDIDATE FREE: direct MCU GPIO breakout; no other V2 schematic load or production claim found. |
| J6-7 | VBUS | Power net; not a GPIO. |
| J6-8 | 3V3 | Regulated supply; not an encoder signal. |
| J6-9 | GND | Preferred encoder common connection. |
| J6-10 | USB D- / GPIO19 | CONFIRMED USED: native USB; unavailable. |
| J6-11 | USB D+ / GPIO20 | CONFIRMED USED: native USB; unavailable. |
| J3-1 | VBAT | Battery rail; not a GPIO. |
| J3-2 | 3V3 | Regulated supply. |
| J3-3 | GND | Ground. |
| J3-4 | GPIO48 | CONFIRMED USED: system I2C SCL. |
| J3-5 | GPIO47 | CONFIRMED USED: system I2C SDA. |
| J3-6 | GPIO44 | CONFIRMED USED: UART RX/console. |
| J3-7 | GPIO43 | CONFIRMED USED: UART TX/console. |
| J3-8 | GPIO38 | CONFIRMED BOARD FUNCTION: SD CS/D3. |
| J3-9 | GPIO39 | CONFIRMED BOARD FUNCTION: SD CMD/MOSI. |
| J3-10 | GPIO40 | CONFIRMED BOARD FUNCTION: SD D0/MISO. |
| J3-11 | GPIO41 | CONFIRMED BOARD FUNCTION: SD CLK. |

## MCU GPIO assignments

| GPIO | Electrical or board function | Availability |
| --- | --- | --- |
| 0 | BOOT0, J6-1, strapping pin | Reserved; do not use. |
| 1 | External-power ADC1 channel 0, J6-2 | CONFIRMED USED. |
| 2 | Direct breakout J6-3; no other schematic load | CANDIDATE FREE. |
| 3 | Direct breakout J6-4, strapping pin | Reserved; do not use. |
| 4 | Battery divider `BAT_ADC`, ADC1 channel 3, J6-5 | CONFIRMED USED. |
| 5 | Direct breakout J6-6; no other schematic load | CANDIDATE FREE. |
| 6, 7, 15, 45, 46 | Onboard I2S/audio nets; GPIO45 and GPIO46 are also strapping pins | Reserved from encoder use. |
| 8 | TCA9554 shared interrupt for touch/IMU/RTC and wake | CONFIRMED USED. |
| 9-14 | LCD QSPI CS, clock and data 0-3 | CONFIRMED USED. |
| 16 | `SYS_OUT` power/key network | Reserved. |
| 17, 18 | Touch I2C SDA/SCL | CONFIRMED USED. |
| 19, 20 | Native USB D-/D+ and J6-10/J6-11 | CONFIRMED USED. |
| 21 | LCD TE | CONFIRMED BOARD FUNCTION; reserved. |
| 22-37 | Not usable as general external GPIO on this board/package; includes flash/PSRAM resources and invalid ESP32-S3 GPIO numbers | Reserved. |
| 38-41 | SD interface and J3-8 through J3-11 | CONFIRMED BOARD FUNCTION; reserved. |
| 42 | LCD backlight PWM | CONFIRMED USED. |
| 43, 44 | UART console and J3-7/J3-6 | CONFIRMED USED. |
| 47, 48 | System I2C SDA/SCL and J3-5/J3-4 | CONFIRMED USED. |

The TCA9554 expander outputs and inputs are already assigned to touch interrupt, backlight enable, IMU interrupts, RTC interrupt, LCD reset, system power hold and audio mode. They are not encoder candidates.

## Preferred encoder wiring proposal

Status: **OWNER SELECTED / PENDING APPROVAL; not wired or enabled.**

| Encoder terminal | Proposed board connection | Electrical mode |
| --- | --- | --- |
| A / CLK | GPIO2, expansion pad **J6-3** | Input only, internal 3.3 V pull-up. |
| B / DT | GPIO5, expansion pad **J6-6** | Input only, internal 3.3 V pull-up. |
| Common | **J6-9 GND** | Ground. |
| Push button | Not connected | Outside current scope. |

GPIO2/GPIO5 is the preferred pair because both signals are direct J6 breakouts, neither has another load in the V2 schematic, neither is an ESP32-S3 strapping pin, and neither is claimed by the current production firmware. GPIO0 and GPIO3 are rejected because they are strapping pins. GPIO1 and GPIO4 are rejected because they are active analog inputs. The remaining exposed J3/J6 GPIOs are tied to USB, UART, I2C or SD functions.

Before implementation, the owner must approve this exact wiring and confirm the physical `J6` pin-1 orientation. Later commissioning must confirm clockwise/counterclockwise polarity and the mechanical transitions-per-detent convention; swapping A and B in wiring or configuration requires a separate explicit decision based on that observation.

## Sources

- [Waveshare board page and V2 interface overview](https://docs.waveshare.com/ESP32-S3-Touch-LCD-3.49)
- [Waveshare V2 resources and Rev1.1 identification](https://docs.waveshare.com/ESP32-S3-Touch-LCD-3.49/Resources-And-Documents)
- [Official Waveshare V2 schematic](https://github.com/waveshareteam/ESP32-S3-Touch-LCD-3.49-V2/blob/main/schematic/ESP32-S3-Touch-LCD-3.49%20V2.pdf)
- [Official Waveshare V2 production pin definitions](https://github.com/waveshareteam/ESP32-S3-Touch-LCD-3.49-V2/blob/main/ESP-IDF/11_FactoryProgram/main/user_config.h)
- [Espressif ESP32-S3 datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.html)
- Private production evidence, inspected without publication: `main/user_config.h`, `components/power_management/hardware.cpp`, `components/power_management/runtime.cpp`, and existing hardware records.
