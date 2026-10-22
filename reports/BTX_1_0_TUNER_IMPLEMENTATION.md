# BTX/1.0 TUNER Phase 3 implementation

Status: **SOFTWARE VERIFIED / HARDWARE NOT RUN**  
Date: 2026-10-22

The owner-approved frozen BTX/1.0 contract was implemented on TUNER branch
`tuner/btx-1.0-implementation`, based exactly on D-009 + mDNS commit
`216f5a14d375652543d3f722141acbf526bee8c8`. The executable source commit is
`bc9c148a942732c890fcba6e6b15769bc4cd9067`; documentation commit is
`1ac32909f0fe1697f0a7301cd1d3c79956b1a92f`; review is TUNER
[PR #9](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/pull/9).

Implemented behavior:

- exact legacy first ID 3/4 exchange and session-scoped immediate second-ID-3
  BTX opt-in;
- exact IDs 12-15 and correlated ID 8 result;
- callback-authoritative A2DP connection/playback state;
- bounded UTF-8 artist/title handling at 96/127 bytes;
- source/phone generation and playback-state command fencing;
- one fixed mailbox with main-loop Play/Pause/Previous/Next ownership;
- session/disconnect clearing and no automatic command retry.

IDs 1-11, D-009 radio semantics, volume, RTCP security/framing/counters, mDNS,
pairing and NVS are unchanged. REMOTE source and firmware are unchanged.

Focused BTX and relevant compatibility verification passed 183
assertions/checks. The `esp32-lwip-psram` production build passed:

| Item | Result |
| --- | ---: |
| Embedded build ID | `bc9c148a9427` |
| Application size | 2,072,960 bytes |
| Application SHA-256 | `67fbeb56082fffddb6104f5ed948395bc862262cf5bcb10602292b08cb3ad590` |
| ELF SHA-256 | `e4807c7929941cf0a0255a24b98633342ed9a435d6da31a4973ca31e2eaace99` |
| Static RAM | 89,904 / 327,680 bytes |
| Application-slot headroom | 1,072,768 bytes |
| New persistent scalar/session state | 60 bytes; guarded at <=64 |
| Maximum plaintext / authenticated record | 255 / 299 bytes |

No firmware binary, secret, pairing material or private backup was published.
No hardware was accessed. TUNER-first validation must verify the exact private
candidate and rollback image, application-only readback, old-REMOTE legacy
compatibility, radio/web/mDNS behavior, A2DP and physical AVRCP operation, and
internal heap/minimum/largest-block/allocation-failure margins during A2DP plus
RTCP plus web-manager coexistence. BTX end-to-end tests wait for separately
authorized REMOTE implementation.
