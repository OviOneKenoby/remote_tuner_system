# A-TUNER-002 — bounded correctness guards

Date (UTC): 2026-10-08T15:00:49Z
Coordination execution input: `d172db8615ca2da53d510d65c6a6ffcc5b21dd4a`
Coordination publication base: `8e1ab9d87c4647964bbc48d0e50982472a0b9cca`
Firmware result: `8fac1da6ccd749a47843d99dc746fc3d6e4bf19b`
Status: READY FOR REVIEW; software/build PASS, physical hardware NOT RUN.

## Scope and baseline

The live firmware tree was clean on the documentation result
`48821a6071072b77a9a023303ebf215a0577ff2e`, whose executable parent is the
assigned V1.1.0 baseline `371cdebce7ba2648ea71636d5bdb5d738b42e680`.
There were no newer executable differences to reconcile. The task corrected
only B01 strict delete parsing, B04 empty/stale saved-list traversal, B06
relative-volume underflow and B03 discovered Favorite codec propagation.

No Native endpoint/adapter/discovery/pairing, station identity migration,
persistence format, dependency, platform, partition, GPIO, REMOTE source or
shared contract changed. B02/B05/B07–B11 remain outside this task.

## Implemented changes

### B01 — strict destructive-route index validation

`src/correctness_guards.h::parseListIndex` accepts a nonempty one-to-three
character ASCII decimal suffix only, rejects signs/space/junk/overlong input,
checks overflow before narrowing to `uint8_t`, and requires the value to be
strictly below the current list count. Both existing DELETE handlers validate
before calling their mutation. Valid routes retain the existing 200 response;
invalid/missing/out-of-range routes retain the existing 404 error response.

This closes the confirmed `toInt()`/narrowing paths where nonnumeric text or
`256` could become index zero. Rejected inputs never call the remove method.

### B04 — bounded saved-list Next/Previous

`nextStationIndex` and `previousStationIndex` reject count zero and a stale
current index. `handlePlayingInput` logs an unavailable/no-op result instead of
performing modulo zero or `count - 1` underflow. One-item and normal wrapping
behavior are preserved. Durable station identity and deletion-before-current
semantics remain explicitly unresolved and outside this small correction.

### B06 — saturating relative volume

`volumeDown` now performs the subtraction in a bounded helper: values 1–5
become zero, larger values subtract five, and the existing zero no-op remains.
No audio or Bluetooth volume policy changed.

### B03 — actual discovered codec in Favorites

The current playing context now owns the resolved `StationCodec` and whether
the source is discovered. Every successful saved/discovered play updates that
context. The later discovered `+Favorite` path uses the stored codec instead of
hard-coding MP3. Immediate Browse/Recent/Favorite add paths continue using the
same resolved codec. `stationCodecForURL` was moved to a host-testable header;
it preserves the supplied codec for opaque URLs and only upgrades legacy MP3
records when `.aac` is explicit.

Thus an opaque AAC/AAC+ locator persists AAC across Favorite storage/reload;
opaque MP3 remains MP3. Existing Recent pointer-copy, decoder lifetime,
metadata synchronization and Bluetooth codec fixes were not altered.

## Verification

| Check | Result | Evidence |
| --- | --- | --- |
| Host compile with warnings as errors | PASS | MSYS2 GCC 16.2.0, `-std=c++17 -Wall -Wextra -Werror` |
| Deterministic guard suite | PASS, 249 checks | `tests/test_correctness_guards.cpp`; [build/test evidence](../references/device_evidence/tuner/A-TUNER-002/BUILD_AND_TEST.md) |
| Clean isolated PlatformIO build | PASS | esp32-dev / espressif32 7.0.1 / pinned dependencies; 136.93 s |
| RAM | PASS for build | 83,056 / 327,680 bytes (25.3%) |
| Flash | PASS for build | 1,992,833 / 3,145,728 bytes (63.4%) |
| Binary identity | PASS | 1,999,408 bytes; SHA-256 `AF066BA215F863A7D2583A6313ACEE00020CCFAD4F8F8C3168DEDA76BCD6F5D4` |
| Diff/scope/config | PASS | no platform/dependency/partition/GPIO/version change |
| Firmware PR | OPEN / published | https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/pull/2 |
| Upload/physical regression | NOT RUN | explicitly excluded without separate authorization |

The initial network clone of the pinned A2DP dependency stalled before
compilation. The successful clean build used copied, locally resolved
dependency directories after verifying both pinned Git HEADs. This does not
change the dependency revisions and is recorded rather than hidden.

## Owner hardware regression checklist

Use only the reviewed PR artifact or rebuild commit `8fac1da6…`; record the
flashed binary hash and full serial log.

1. Create sacrificial saved/Favorite entries. Send DELETE requests with empty,
   signed, spaced, junk, overlong, `255`, `256` and current-count suffixes.
   Expect 404 and byte-for-byte unchanged lists. Delete a valid middle and zero
   item; expect only the selected item removed and HTTP 200.
2. Play a saved station, delete every saved station via the web manager, then
   issue physical and serial Next/Previous. Expect the explicit unavailable
   log, no reboot/panic and no attempted playback. Repeat normal one/many wrap.
3. Reduce volume from 5 to 0 and press Down again in radio and Bluetooth modes.
   Expect zero to remain zero and never jump to 100. Values 1–4 are exhaustively
   software-tested; exercise them physically only through an approved harness.
4. Play an opaque AAC/AAC+ stream such as the KIIS-style URL, add it to
   Favorites using the playing-screen action, reboot, verify it is still shown
   as AAC and plays with the AAC decoder. Repeat an opaque MP3 station and an
   explicit uppercase/lowercase `.aac` URL.
5. Regression: HTTP/HTTPS MP3, HTTPS AAC+, Recent, Favorite add/play/remove,
   web manager, local encoder/buttons and Bluetooth transition/audio.

## Remaining limitations

- Hardware behavior and actual flashed artifact are PENDING / NOT RUN.
- B04 durable identity and active-item deletion semantics remain open.
- B02/B05/B07–B11 and O01–O17 remain open; this task does not establish Native
  support, truthful whole-device state or common-gate acceptance.
- Existing unauthenticated legacy web-route/security questions remain O17 and
  were not expanded or changed.

## Publication boundary

The firmware branch/commit/PR and the coordination report/evidence/handoff PR
are published separately. The coordination result branch started from current
main `8e1ab9d87c4647964bbc48d0e50982472a0b9cca`, preserving concurrent PM and
REMOTE additions.

Before result publication, this session had already integrated reviewed
A-TUNER-001 PR #1 (`13c7ff66d8d02e53d8cc163c10620ff21f17db9f`) and the exact
A-TUNER-002 assignment PR #4 (`d172db8615ca2da53d510d65c6a6ffcc5b21dd4a`).

CCM 1.0.0 remains OWNER APPROVED/FROZEN. TUNER Native API v1 remains
UNAPPROVED/UNFROZEN/NOT IMPLEMENTED. No common contract approval is claimed.
