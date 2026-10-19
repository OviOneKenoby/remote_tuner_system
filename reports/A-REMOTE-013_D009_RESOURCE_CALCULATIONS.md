# A-REMOTE-013 D-009 resource and serialized-size review

No build or hardware measurement was performed. Baseline values are accepted A-REMOTE-012 evidence; implementation deltas remain estimates until production builds.

## Exact wire sizes

| Record | Plaintext | Authenticated wire size (`28 + plaintext + 16`) | Existing 556-byte buffer margin |
| --- | ---: | ---: | ---: |
| playback command | 19 | 63 | 493 |
| command result | 11 | 55 | 501 |
| now-playing request | 1 | 45 | 511 |
| combined now-playing maximum | 350 | 394 | 162 |
| split now-playing maximum | 446 | 490 | 66 |

The maximum plaintext remains below 512 bytes. Existing TUNER and REMOTE encrypted-record arrays remain 556 bytes, so D-009 requires no transport buffer increase.

## Device budgets and expected deltas

| Device | Accepted baseline | D-009 fixed-data expectation | Risk |
| --- | --- | --- | --- |
| TUNER | 2,037,632-byte app; 1,108,096-byte slot headroom; 87,512-byte static RAM; A2DP minimum internal heap 22,468 and largest block 16,372 | one bounded main-loop command slot plus station/metadata projection; target no more than 512 bytes persistent static data; response uses existing 512-byte stack/record storage | Low if no dynamic allocation or browser/e-paper work enters RTCP; must remeasure A2DP heap/largest block |
| REMOTE | 2,526,848-byte app; 618,880-byte slot headroom; 47,388-byte static RAM | wire buffers unchanged; bounded decoded text/Core ownership and HOME snapshot expansion, expected under 1 KiB fixed/retained data | Low-to-moderate; verify diagnostic/storage guards and UI-task copying |

TUNER already owns a 256-byte radio metadata buffer and 64-byte station-name buffer. The implementation should snapshot them into fixed storage and serialize directly into the existing response buffer. It must not allocate a second 512-byte transport buffer or use `String`/unbounded heap allocation in the RTCP path.

REMOTE may retain at most 63 station bytes, 255 title/combined bytes and 96 artist bytes, plus Core observation overhead. Presentation copies remain bounded. Frequent metadata changes replace the current bounded observations; they must not grow history without the existing Core limits.

## Scheduling controls

- One extra request/response follows each normal 1-second state snapshot only when capability bit 7 is present.
- Commands retain priority and one-in-flight behavior.
- Metadata copying/validation is bounded by 414 source text bytes; LVGL updates stay on the existing 20 ms UI timer.
- No HTTPS, JSON, station browsing, image decode, e-paper refresh or Bluetooth lifecycle work is added to the RTCP handler.

Production builds must report exact app size, slot headroom and static RAM for both devices. TUNER hardware validation must record internal free heap, minimum heap, largest block, allocation failures and resets during MP3 and A2DP/web/RTCP coexistence. The Classic-only Bluetooth memory correction remains untouched.
