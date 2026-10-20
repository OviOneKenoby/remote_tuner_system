# RTCP/1 D-009 proposed playback and now-playing profile

Status: **PROPOSED / OWNER REVIEW — NOT APPROVED, NOT IMPLEMENTED**
Date: 2026-10-19
Coordination baseline: `aa45826492d78714ce58221ea2a832adb52ac73f`
Authority boundary: additive RTCP/1 application profile only. CCM 1.1.0 remains OWNER APPROVED / FROZEN. Native API v1 remains UNAPPROVED / NOT IMPLEMENTED.

## 1. Existing wire retained unchanged

RTCP/1 authentication, directional keys, counters, framing, 512-byte maximum plaintext, timeouts, one in-flight application request, correlation, session fencing and no-automatic-retry behavior are unchanged. Existing application messages retain their layouts:

| ID | Message | Plaintext size |
| ---: | --- | ---: |
| 1/2 | identity request/response | 4 / 5–36 bytes |
| 3/4 | capability request/response | 1 / 16 bytes |
| 5/6 | state snapshot request/response | 1 / 19 bytes |
| 7 | `volume_set` | 17 bytes |
| 8 | command result | 11 bytes |

All multibyte integers are unsigned, big-endian, as in the existing implementation. Reserved bits and bytes MUST be zero. A message with the wrong exact length, invalid reserved data, zero required identifier/generation, or impossible enum is application-invalid and closes the session. Existing volume behavior is unchanged.

## 2. Capability response extension

The 16-byte capability response layout is unchanged. Byte 1 becomes this complete bitmap:

| Bit | Capability |
| ---: | --- |
| 0 | `volume.level` observation |
| 1 | `playback.state` observation |
| 2 | `volume.set` |
| 3 | `playback.play` |
| 4 | `playback.pause` |
| 5 | `playback.previous` |
| 6 | `playback.next` |
| 7 | D-009 now-playing observation |

A D-009 TUNER advertises capability revision `2`. Bytes 10–13 remain the 2,000 ms freshness value; bytes 14–15 remain volume step `1` and maximum `100`. Capability bits indicate implemented operations. Per-context availability is carried by the now-playing response and never inferred merely from support.

An old REMOTE ignores bits 3–7 and continues the accepted volume profile. A new REMOTE sends no D-009 message unless the corresponding bit is advertised. Unknown application message IDs continue to fail closed; additive compatibility is obtained through capability gating, not by making unknown messages silently acceptable.

## 3. New message IDs

IDs 9–11 are currently unused in both production implementations and are proposed as follows:

| ID | Message | Direction | Exact plaintext size |
| ---: | --- | --- | ---: |
| 9 | playback command | REMOTE → TUNER | 19 bytes |
| 10 | now-playing request | REMOTE → TUNER | 1 byte |
| 11 | now-playing response | TUNER → REMOTE | 32–446 bytes |

### 3.1 Playback command, ID 9

| Offset | Size | Field |
| ---: | ---: | --- |
| 0 | 1 | kind = 9 |
| 1 | 8 | nonzero request ID |
| 9 | 1 | operation: 1 play, 2 pause, 3 previous, 4 next |
| 10 | 1 | expected playback state: 0 playing, 1 paused, 2 not-playing, 3 buffering |
| 11 | 8 | nonzero expected media-context generation |

The expected state and generation are captured from the fresh observations used by CCM admission. TUNER rejects a generation mismatch before execution. Play/pause also reject a state mismatch. Previous/next use the generation fence and require the current fixed saved-station context.

The response is the existing ID 8 command result. Its error byte is standardized for this profile without changing its layout:

| Code | Meaning | CCM result mapping |
| ---: | --- | --- |
| 0 | accepted and completed | complete / acknowledged |
| 1 | invalid argument | `INVALID_ARGUMENT` |
| 2 | operation unsupported | `UNSUPPORTED_OPERATION` |
| 3 | operation unavailable in the current source/context | `UNAVAILABLE` |
| 4 | stale state or media-generation precondition | `STALE_PRECONDITION` |
| 5 | target execution failed | `UNAVAILABLE`, target failure detail |
| 6 | target busy/order gate refused execution | `ORDERING_BLOCKED` |
| 7 | bounded internal failure before confirmed execution | `UNAVAILABLE`, target failure detail |
| 8–255 | reserved | invalid for D-009 |

Code 1 preserves the existing invalid-volume-argument meaning. `accepted=1` requires error 0; `accepted=0` requires one of 1–7. A syntactically valid refusal is correlated and does not close the session. Malformed frames close it. A disconnect after command transmission remains ambiguous delivery; REMOTE does not retry.

### 3.2 Now-playing request, ID 10

The request is the single byte `0x0A`. It carries no mutation and is valid only after identity/capability acceptance.

### 3.3 Now-playing response, ID 11

| Offset | Size | Field |
| ---: | ---: | --- |
| 0 | 1 | kind = 11 |
| 1 | 1 | flags |
| 2 | 1 | context |
| 3 | 1 | station length, 0–63 |
| 4 | 1 | artist length, 0–96 |
| 5 | 1 | title length, 0–255 |
| 6 | 2 | combined StreamTitle length, 0–255 |
| 8 | 8 | nonzero sample sequence |
| 16 | 8 | nonzero media-context generation |
| 24 | 8 | nonzero metadata revision |
| 32 | variable | station, artist, title, combined bytes in that order |

Context values are: 0 no applicable source, 1 fixed saved-list radio, 2 discovered/favorite/recent radio, 3 Bluetooth, and 4 other. Contexts 3 and 4 are reported only to invalidate radio data in this slice; Bluetooth AVRCP and Bluetooth metadata are not exposed by D-009.

Flags are:

| Bit | Meaning |
| ---: | --- |
| 0 | station valid |
| 1 | metadata valid |
| 2 | metadata is trustworthy split artist/title |
| 3 | at least one source string was truncated at a UTF-8 codepoint boundary |
| 4 | play currently available |
| 5 | pause currently available |
| 6 | previous currently available |
| 7 | next currently available |

Validation rules are exact:

- Station-valid requires radio context and station length 1–63. Otherwise station length is zero.
- Metadata-invalid requires split clear and all three metadata lengths zero.
- Metadata-valid with split clear requires artist/title lengths zero and combined length 1–255.
- Metadata-valid with split set requires combined length zero, artist length 0–96, title length 0–255, and at least one split field nonempty.
- D-009 v1.1.12 radio metadata always uses the combined form because the production ICY path owns only one StreamTitle string. It MUST NOT guess artist/title by splitting punctuation.
- Operation availability must agree with context and state. Play is available only for paused radio and pause only for playing radio, in either fixed or discovered radio context. Previous/next are available only for a valid fixed saved-list station with a valid nonempty traversal list; they are clear for discovered radio. All four are clear for Bluetooth, other, or absent contexts.

## 4. Strings and exact size bounds

Strings contain no terminator. They MUST be well-formed UTF-8 and MUST NOT contain NUL, C0 control characters, or DEL. Malformed source text is reported unavailable rather than repaired or guessed. Oversized valid text is truncated only at a complete UTF-8 codepoint and sets the truncated flag. Unicode normalization is not performed.

The radio StreamTitle on TUNER is already a bounded 255-byte C string produced by the existing metadata callback and simplifier. D-009 transports that projected string exactly when valid. The internal placeholder `Live stream` is not metadata and is reported as metadata-invalid.

Maximum plaintext calculations:

- Combined: `32 + 63 + 255 = 350` bytes.
- Split: `32 + 63 + 96 + 255 = 446` bytes.
- Playback command: `19` bytes.
- Request: `1` byte.

With the existing 28-byte authenticated header and 16-byte GCM tag, the largest D-009 record is `28 + 446 + 16 = 490` bytes, leaving 66 bytes in the existing 556-byte wire buffer and 66 bytes below the 512-byte plaintext ceiling.

## 5. Authoritative projection and freshness

TUNER owns the state. The main loop publishes a fixed-size copied projection from `nowPlayingName`, `nowPlayingContext`, `AudioPlayer::getSource()`, `getState()` and `getNowPlaying()`; the RTCP handler never calls LVGL/e-paper handlers or browser operations.

- Sample sequence is the same strictly increasing sequence domain used by the existing state snapshot. It increments for every emitted snapshot or now-playing response and never wraps.
- Media-context generation increments before publication whenever source, selected station, or station context changes. A station-change attempt invalidates old track metadata before the new selection can be published.
- Metadata revision starts nonzero and increments only when station validity/text, metadata validity/text/form, context, or operation availability changes. It never wraps or reuses a value in one boot.
- All `playback.state` and `media.*` observations carry the matching media-context generation.
- D-009 fields use the existing 2,000 ms `VERIFIED_SEQUENCE` policy with the same authenticated request/reply sample clock contract. REMOTE requests a state snapshot every 1,000 ms and, after each successful snapshot, requests one now-playing response when bit 7 is present. A post-command authoritative refresh uses the same sequence. Commands keep priority; there is still only one application request in flight.
- On disconnect or session replacement, REMOTE withdraws dynamic operation availability and invalidates station/metadata observations. Reconnect obtains identity, capabilities, state snapshot and now-playing response before these fields become current again.

CCM mapping is:

| Wire value | CCM field |
| --- | --- |
| selected station display name | `media.subtitle` |
| exact combined StreamTitle, or trustworthy split title | `media.title` |
| trustworthy split artist only | `media.artist` |
| playback byte | existing `playback.state` |

This uses the existing generic string fields without changing their frozen type or authority rules. A combined StreamTitle remains one `media.title`; an artist observation is absent rather than fabricated. The HOME presentation may label station and now-playing text differently, but Core truth remains in the fields above.

## 6. Playback semantics

- `playback.pause`: valid only for the current radio context in PLAYING; calls the existing radio pause authority and acknowledges only after PAUSED is observed locally.
- `playback.play`: valid only for the current radio context in PAUSED; calls the existing resume authority and acknowledges only after PLAYING is observed locally.
- `playback.previous` / `playback.next`: valid only for the fixed saved-station list. They use the existing guarded previous/next index rules, including existing wrap behavior. Empty or stale selection refuses without execution.
- Discovered/favorite/recent one-off playback reports previous/next unavailable. The local discovered-mode Next gesture adds a favorite; D-009 MUST NOT invoke or expose that mutation as `playback.next`.
- Bluetooth, AVRCP, source selection, stop, mute, catalogs, favorites mutation and artwork are outside this profile.

TUNER executes through a dedicated main-loop-owned command adapter. The network handler enqueues at most one bounded command and never calls `handlePlayingInput()` blindly. A result is accepted only after the authoritative owner completes or refuses that exact request. REMOTE never treats send completion as operation success and never applies an old result to a replaced session.

## 7. Compatibility and failure behavior

1. Install TUNER first. New TUNER plus old REMOTE continues IDs 1–8; upper capability bits are ignored.
2. New REMOTE plus old TUNER sees bits 3–7 clear and leaves controls/media unavailable while volume remains functional.
3. New/new enables D-009 only after revision/capability validation.
4. Rollback of either application restores the corresponding old capability surface; pairing, NVS and partitions are unchanged.
5. Every uncertain delivery, timeout, disconnect or session change clears pending presentation and requires fresh observations. There is no automatic playback retry.

## 8. Approval gate

Owner approval must explicitly accept the message IDs/layouts, capability bits, field projection, fixed-list-only traversal, combined StreamTitle rule, bounds and rollout order. Until then this document is not an effective protocol and no firmware task is assigned.
