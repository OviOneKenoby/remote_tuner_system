# A-REMOTE-011 Stage 5 GPIO resolution

Date: 2026-10-14  
Verdict: **WIRING PROPOSAL READY FOR OWNER APPROVAL; implementation remains stopped.**

The official V2 schematic, Waveshare interface table, ESP32-S3 strapping rules and current production source were cross-checked. The earlier GPIO4/GPIO5 assignment remains rejected because GPIO4 is the active battery ADC. GPIO1 remains occupied by owner-installed external-power sensing.

The V2 board exposes GPIO0 through GPIO5 on expansion row J6. GPIO0 and GPIO3 are strapping pins. GPIO1 and GPIO4 are active analog inputs. GPIO2 at J6-3 and GPIO5 at J6-6 are direct MCU breakouts with no other load shown by the V2 schematic, no production firmware claim, and no strapping role. They are the only verified pair on J6 meeting the stated constraints.

Preferred proposal:

- encoder A/CLK: GPIO2 at J6-3;
- encoder B/DT: GPIO5 at J6-6;
- encoder common: J6-9 GND;
- both signals input-only with internal 3.3 V pull-ups;
- push button unconnected.

The complete evidence-based map is in [`docs/REMOTE_GPIO_MAP.md`](../docs/REMOTE_GPIO_MAP.md). The proposal distinguishes schematic facts, production assignments and owner-selected pending wiring. No production source was edited, no build or test ran, and no device was accessed.

The required next action is owner approval of the exact J6-3/J6-6/J6-9 wiring after confirming the physical J6 pin-1 orientation. Stage 5 implementation and commissioning remain stopped.
