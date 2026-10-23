# A-REMOTE-013 D-009 Round 5 hardware validation

Status: **TEST SESSION CLOSED / PARTIAL HARDWARE PASS**

Date: 2026-10-23

## Exact tested pair

| Device | Identity |
| --- | --- |
| REMOTE | source `bfce47816a8b2b8a92f41d76c6a4bc4975d25361`; 2,578,352-byte application; SHA-256 `6eb44ff4137d8c11f44dc5e0fed0a7061f77b172d4a38982e5219bbd7454e278` |
| TUNER | D-009 application; 2,040,704 bytes; SHA-256 `1e6c5968f539170656e833d023086c57986b1aa73a6c2fe982dee2b31b1ff1f6a` |
| REMOTE rollback | accepted A-REMOTE-012 application; 2,526,848 bytes; SHA-256 `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da` |

The REMOTE candidate was written once to the verified factory application
partition at `0x10000`. Independent exact-span readback matched the candidate
SHA-256. Local and separate-USB rollback material matched recorded manifests.
Boot, stored Wi-Fi, secure pairing, authenticated RTCP and authoritative volume
recovered without reprovisioning.

## Hardware PASS evidence

- Carousel 0 -> 1 -> 2, brightness, touchscreen and HOME index 2.
- Existing encoder volume and authoritative volume synchronization.
- Radio Playing/Paused state, icon and REMOTE Play/Pause operation.
- Local TUNER Pause/Resume reflected by REMOTE.
- Selected station and exact combined ICY StreamTitle, including scrolling and
  replacement after a station change.
- Previous/Next unavailable in discovered/Radio Browser context.
- TUNER restart invalidated station, metadata, playback, volume and controls;
  reconnect restored current state and encoder volume without stale display.
- A2DP playback remained functional; radio metadata and D-009 radio controls
  were withdrawn, and returning to radio restored station, StreamTitle,
  playback state and Play/Pause.

Bluetooth metadata on REMOTE and Bluetooth AVRCP are outside D-009. The upper
Playing indication remaining unchanged during a phone-side Bluetooth pause is
an observed source-semantics question, not a demonstrated D-009 radio defect.

## Remaining acceptance

1. Successful Previous/Next and wrap with at least two fixed saved stations.
2. Any approved forced-invalid-command Favorites non-mutation proof.
3. REMOTE sleep/wake and D-009 resynchronization.
4. Safe REMOTE restart if a supported method is available.
5. Representative resource/stability measurements with MP3, A2DP and web use.
6. Any remaining mandatory item in the approved D-009 hardware protocol.

REMOTE PR #4 and TUNER PR #7 remain open and unmerged. REMOTE PR #4 remains
stacked on the A-REMOTE-014 mDNS branch. Overall A-REMOTE-013 remains
**HARDWARE ACCEPTANCE PENDING**.
