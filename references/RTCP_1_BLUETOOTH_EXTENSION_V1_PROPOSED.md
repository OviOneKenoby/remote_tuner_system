# RTCP/1 Bluetooth Extension v1 proposed profile

Status: **PROPOSED / OWNER REVIEW — NOT APPROVED, NOT IMPLEMENTED**

Short name: **BTX/1.0**. Decision candidate: **D-011**.

Authority boundary: additive authenticated RTCP/1 application profile only. RTCP/1 transport security, CCM 1.1.0 and frozen D-009 semantics are unchanged. This document grants no firmware implementation or hardware authority.

## 1. Purpose and exclusions

BTX/1.0 adds authoritative Bluetooth source, connection, playback and metadata observations plus explicit AVRCP Play, Pause, Previous and Next commands. Existing `volume.set` remains the only volume command and is not changed.

BTX/1.0 does not add source selection, pairing, Bluetooth device management, mute, artwork, catalogs, queues or phone identity. It does not change D-009 radio meanings or permit Bluetooth fields in D-009 message 11.

## 2. Unchanged RTCP/1 foundation

- The existing PSK, handshake, HKDF, AES-128-GCM record format, session ID, directional counters and replay rules remain exact.
- All BTX messages are application plaintext inside authenticated RTCP/1 records.
- Maximum plaintext remains 512 bytes; the fixed authenticated overhead remains 28-byte header plus 16-byte tag.
- All multibyte integers are unsigned big-endian.
- There is one application request in flight. Transport delivery is not command success. There is no automatic retry.
- Wrong exact length, invalid enum, nonzero reserved bit, zero required identifier/generation, malformed UTF-8 or impossible field combination is application-invalid and closes the session.
- A syntactically valid command refusal is correlated and does not close the session.

Existing IDs 1–11 and the revision-2 16-byte capability response retain their frozen layouts and meanings.

## 3. Session-scoped negotiation

### 3.1 Selected mechanism: authenticated two-query capability probe

The client first performs the existing identity exchange and sends the normal one-byte capability request, ID 3. Every TUNER, including a BTX-capable TUNER, MUST answer this first request with the exact legacy 16-byte ID 4 revision-2 response.

Immediately after accepting that response, before sending any other application request, a BTX-capable REMOTE sends the same one-byte ID 3 request once more. This second, consecutive request is the explicit BTX opt-in probe:

- a legacy TUNER returns the same legacy ID 4 response;
- a BTX-capable TUNER returns the ID 12 BTX capability response;
- ID 4 means BTX unsupported for this session and normal D-009 continues;
- valid ID 12 means BTX negotiated for this session;
- any other response, malformed ID 12, timeout, EOF or transport error closes the session and does not enable BTX.

The TUNER probe window exists only after it sends the first ID 4 and before it accepts any other application request. If the next request is not ID 3, the session is locked to legacy behavior. Additional capability probes after the window are application-invalid.

This uses the existing safe behavior of a legacy TUNER: it accepts another authenticated ID 3 and returns ID 4. It never receives an unknown request. An old REMOTE sends only one capability request and therefore always receives exact legacy behavior from a new TUNER.

### 3.2 Security and lifecycle

Negotiation is authenticated, protected by the existing record counter and scoped to one RTCP session. Neither endpoint stores the result in NVS. Reconnect, restart, sleep teardown or session replacement clears it. A new session repeats both queries before any BTX message is accepted.

An on-path party cannot forge ID 4 in place of ID 12 without failing GCM authentication. Connection loss can deny service but cannot create a negotiated capability or authorize a command.

### 3.3 Rejected mechanisms

- **New discovery request sent unconditionally:** a legacy TUNER fails closed on an unknown message, producing a deliberate disconnect and repeated reconnect failures.
- **Revision 3 or another bit in ID 4:** all eight bits are occupied and the deployed D-009 REMOTE requires revision exactly 2. This would withdraw existing radio D-009 behavior.
- **mDNS-only negotiation:** DNS-SD is useful for endpoint discovery but is not an authenticated capability authority.
- **New handshake/record version:** substantially larger change to the already accepted cryptographic transport and unnecessary for an application extension.
- **Firmware-version inference:** couples behavior to release strings rather than an explicit authenticated capability exchange.

## 4. New message IDs

| ID | Message | Direction | Exact plaintext size |
| ---: | --- | --- | ---: |
| 12 | BTX capability response | TUNER → REMOTE | 16 bytes |
| 13 | Bluetooth state request | REMOTE → TUNER | 1 byte |
| 14 | Bluetooth state response | TUNER → REMOTE | 32–255 bytes |
| 15 | Bluetooth command | REMOTE → TUNER | 19 bytes |

The existing ID 8 command result is reused without changing its 11-byte layout or error-code domain. IDs 12–15 are valid only after successful BTX negotiation.

## 5. BTX capability response, ID 12

| Offset | Size | Field |
| ---: | ---: | --- |
| 0 | 1 | kind = 12 |
| 1 | 1 | BTX major = 1 |
| 2 | 1 | BTX minor = 0 |
| 3 | 1 | feature bitmap |
| 4 | 1 | maximum artist bytes, 0–96 |
| 5 | 1 | maximum title bytes, 0–127 |
| 6 | 2 | freshness in milliseconds = 2000 |
| 8 | 8 | capability revision = 1 |

Feature bitmap:

| Bit | Meaning |
| ---: | --- |
| 0 | Bluetooth state/source observation |
| 1 | artist/title metadata |
| 2 | explicit Play |
| 3 | explicit Pause |
| 4 | Previous |
| 5 | Next |
| 6–7 | reserved, zero |

Bit 0 is required. If bit 1 is clear, both metadata maxima are zero. If bit 1 is set, at least one maximum is nonzero. A full implementation advertises bitmap `0x3f`, artist maximum 96 and title maximum 127.

This response describes implementation support. Current command availability comes only from a fresh ID 14 response.

## 6. Bluetooth state request and response

### 6.1 Request, ID 13

The request is exactly the single byte `0x0d`. It is read-only and valid only in a negotiated session.

### 6.2 Response, ID 14

| Offset | Size | Field |
| ---: | ---: | --- |
| 0 | 1 | kind = 14 |
| 1 | 1 | BTX major = 1 |
| 2 | 1 | active source |
| 3 | 1 | Bluetooth connection state |
| 4 | 1 | authoritative Bluetooth playback state |
| 5 | 1 | validity/availability flags |
| 6 | 1 | artist byte length, 0–96 |
| 7 | 1 | title byte length, 0–127 |
| 8 | 8 | nonzero sample sequence |
| 16 | 8 | nonzero source generation |
| 24 | 8 | nonzero metadata revision |
| 32 | variable | artist bytes followed by title bytes |

Active source:

| Value | Meaning |
| ---: | --- |
| 0 | no active audio source |
| 1 | Internet radio |
| 2 | Bluetooth |
| 3 | other source |

Bluetooth connection state:

| Value | Meaning |
| ---: | --- |
| 0 | not applicable because Bluetooth is not active |
| 1 | Bluetooth active, connection state not yet authoritative |
| 2 | Bluetooth active, phone disconnected/listening |
| 3 | Bluetooth active, phone connected |

Bluetooth playback state:

| Value | Meaning |
| ---: | --- |
| 0 | unknown or not applicable |
| 1 | stopped |
| 2 | playing |
| 3 | paused/remote-suspended |

Flags:

| Bit | Meaning |
| ---: | --- |
| 0 | artist valid; artist length is nonzero |
| 1 | title valid; title length is nonzero |
| 2 | Play currently available |
| 3 | Pause currently available |
| 4 | Previous currently available |
| 5 | Next currently available |
| 6–7 | reserved, zero |

Canonical rules:

- For a source other than Bluetooth, connection is 0, playback is 0, all flags are clear and both text lengths are zero. Such a response actively clears prior Bluetooth state.
- For Bluetooth, connection is 1–3. When connection is not 3, playback is 0, all flags are clear and both text lengths are zero.
- Play is available only when the connected authoritative state is stopped or paused. Pause is available only when it is playing.
- Previous/Next availability means the connected AVRCP controller path is ready for local submission. It does not guarantee the phone will honor the action.
- Text validity flags and lengths agree exactly. At least one valid text field is allowed; no placeholder is sent.
- Total size is exactly `32 + artist_length + title_length`.

## 7. State authority and generations

TUNER is the authority. Bluetooth mode entry is not playback evidence.

The implementation maps the A2DP library callbacks as follows:

- connection callback pending/unobserved → connection unknown;
- disconnected callback/query → disconnected;
- connected callback/query → connected;
- `ESP_A2D_AUDIO_STATE_STARTED` → playing;
- `ESP_A2D_AUDIO_STATE_REMOTE_SUSPEND` → paused;
- `ESP_A2D_AUDIO_STATE_STOPPED` while connected → stopped;
- any unrecognized or not-yet-observed audio state → unknown.

The existing local `bluetoothPlaybackPaused` toggle is not authoritative. Explicit network Play calls the A2DP sink `play()` operation; explicit Pause calls `pause()`. Previous and Next call their corresponding AVRCP controller operations. Bluetooth callbacks write only fixed state under the existing bounded synchronization mechanism. The main-loop owner copies that state, revalidates commands and performs AVRCP calls.

Counters:

- Sample sequence shares the existing strictly increasing RTCP observation sequence and advances for every emitted snapshot, D-009 response or BTX state response.
- Source generation increments before publication on every active-source change and on every Bluetooth phone connection/disconnection epoch. This prevents a command captured for an old phone or source from executing after replacement.
- Metadata revision starts nonzero and increments when artist/title validity or bytes change, and when disconnect/source change clears them. It never wraps or reuses a value in one boot.

REMOTE treats state as authoritative only while the authenticated sample is fresh. It withdraws the source, metadata and operation availability on RTCP disconnect, session change, sleep teardown or freshness expiry.

## 8. Bluetooth command, ID 15

| Offset | Size | Field |
| ---: | ---: | --- |
| 0 | 1 | kind = 15 |
| 1 | 8 | nonzero request ID |
| 9 | 1 | operation: 1 Play, 2 Pause, 3 Previous, 4 Next |
| 10 | 1 | expected playback state: 0 unknown, 1 stopped, 2 playing, 3 paused |
| 11 | 8 | nonzero expected source generation |

REMOTE captures expected state and generation from the same fresh ID 14 observation used for CCM admission. Only one command may await a result.

TUNER first validates the record and negotiated feature bit, then queues at most one bounded command. The main-loop owner immediately before execution revalidates:

1. source is Bluetooth;
2. phone is connected;
3. source generation equals the command value;
4. playback state equals the command value;
5. the requested operation remains available.

A source/phone generation change or playback mismatch produces error 4 and no execution. Disconnect or withdrawn operation produces error 3. No stale command is rebased onto a new generation.

## 9. Command results and failures

ID 8 remains `kind[1] || request_id[8] || accepted[1] || error[1]`.

| Code | Meaning |
| ---: | --- |
| 0 | main-loop owner revalidated and submitted the exact AVRCP action |
| 1 | invalid argument |
| 2 | operation unsupported by the negotiated extension |
| 3 | unavailable in current source/connection/context |
| 4 | stale playback/source-generation precondition |
| 5 | local AVRCP submission failed where the API reports failure |
| 6 | bounded busy/order gate refused execution |
| 7 | bounded internal failure before confirmed submission |
| 8–255 | reserved and invalid |

`accepted=1` requires error 0; `accepted=0` requires 1–7. Because the pinned A2DP controller methods do not all report phone-side completion, accepted means local authoritative admission and submission completed. It does not claim the phone applied the action. REMOTE changes authoritative playback presentation only after a later fresh ID 14 observation. Previous/Next may be followed by metadata changes but those changes are not required for result correlation.

Timeout, EOF or disconnect after transmission is ambiguous delivery. REMOTE clears the pending request and never retries automatically.

## 10. Polling and coexistence with D-009

After negotiation, REMOTE requests the standard snapshot. It then requests BTX state:

- if ID 14 reports Bluetooth, that response supplies source, playback, metadata and Bluetooth operation availability; no Bluetooth data is requested through D-009;
- if ID 14 reports radio, REMOTE continues the existing ID 10/11 request to obtain frozen D-009 radio context and metadata;
- an implementation may still issue the legacy ID 10 request in Bluetooth mode, but the TUNER response remains the exact empty context-3 D-009 response.

The target cadence remains one state cycle per 1,000 ms with 2,000 ms freshness. Commands have priority. The client never has more than one request in flight.

## 11. Metadata and HOME presentation

Wire metadata consists of separate artist and title fields. TUNER uses the last values reported by AVRCP for the current Bluetooth connection epoch. It clears both on Bluetooth entry, phone disconnect, source exit and new phone connection before new metadata becomes valid.

Text requirements:

- UTF-8 only; no embedded NUL, C0 control or DEL characters.
- Artist is at most 96 bytes. Title is at most 127 bytes.
- Locally sourced text exceeding a bound is truncated to the largest prefix at or below the bound that ends on a complete UTF-8 code point.
- Invalid locally sourced UTF-8 makes that field absent; it must not cause an RTCP session failure.
- Invalid UTF-8 or noncanonical lengths received on the wire close the RTCP session.

REMOTE keeps source identity separate from metadata and formats HOME as follows:

| Condition | Station/source label | StreamTitle label |
| --- | --- | --- |
| Bluetooth active, connected, artist + title | `Bluetooth` | `artist - title` |
| Bluetooth active, connected, artist only | `Bluetooth` | artist |
| Bluetooth active, connected, title only | `Bluetooth` | title |
| Bluetooth active, connected, neither | `Bluetooth` | `--` |
| Bluetooth active, disconnected/unknown | `Bluetooth` | `Phone disconnected` / `--` respectively |
| Radio active | fresh D-009 station | fresh D-009 StreamTitle |
| No fresh source | `--` | `--` |

The separator is the three ASCII bytes `" - "`. Maximum combined presentation is `96 + 3 + 127 = 226` bytes. The existing 32-byte HOME title presentation buffer therefore increases to 227 bytes including NUL; this is the smallest bound that preserves every valid BTX artist/title pair. Existing geometry, fonts, label objects and bidirectional scrolling remain unchanged. Presentation is never moved optimistically on a command.

## 12. Size and resource budget

| Message | Plaintext | Authenticated record |
| --- | ---: | ---: |
| legacy/BTX capability | 16 | 60 |
| state request | 1 | 45 |
| state response, no metadata | 32 | 76 |
| maximum state response | 255 | 299 |
| Bluetooth command | 19 | 63 |
| command result | 11 | 55 |

BTX does not increase the system maximum: frozen D-009 remains 446-byte plaintext / 490-byte authenticated record. BTX retains 257 bytes of plaintext margin and 257 bytes in the existing 556-byte authenticated buffer.

Implementation budget:

- TUNER reuses existing 128-byte title, 128-byte artist and RTCP transmit/receive buffers. New persistent scalar state and session negotiation state are limited to 64 bytes. No new heap allocation, task, queue or transport buffer is permitted.
- REMOTE reuses existing RTCP artist/title arrays and transport buffers. The required HOME title increase is 195 bytes; all additional negotiation/state scalars must keep total new persistent storage at or below 320 bytes. The temporary UI snapshot adds at most 195 bytes of task-stack use. No new heap allocation or network task is permitted.
- The host reference codec uses ordinary Python objects and is not an on-device memory implementation.

Accepted baselines are TUNER static RAM 89,832 bytes with 1,076,576 bytes application headroom, and REMOTE static RAM 56,460 bytes with 567,376 bytes compatible application headroom. Actual firmware builds must measure the delta. Hardware acceptance must measure TUNER internal free heap, minimum heap, largest internal block and allocation-failure counters during A2DP plus RTCP and web-manager activity; no runtime heap value is claimed here.

## 13. Compatibility, rollout and rollback

| Combination | Required result |
| --- | --- |
| Old REMOTE + New TUNER | One ID 3 only; exact revision-2 ID 4, exact D-009 behavior, radio and volume retained, no BTX message |
| New REMOTE + Old TUNER | Second ID 3 receives ID 4; BTX unavailable, D-009 and volume retained |
| New REMOTE + New TUNER | First ID 3/4 remains legacy; second ID 3/12 negotiates BTX; radio D-009 remains unchanged |
| Reconnect/restart/sleep | Both sides forget BTX state and repeat negotiation; no stale observations or commands |
| TUNER rollback | New REMOTE receives ID 4 to its probe and falls back to D-009 |
| REMOTE rollback | New TUNER sees no second ID 3 and remains an exact legacy server |

Rollout is TUNER first. Before REMOTE installation, the new TUNER must be tested with the installed old REMOTE to prove exact legacy behavior. Pairing, PSK, Wi-Fi, NVS, partition layouts and cryptographic framing remain unchanged.

## 14. Reference artifacts and approval gate

Executable application-codec vectors are in `tools/qualification/rtcp_bluetooth_v1`. They do not implement cryptography and contain no operational identity, metadata or secret.

Owner approval must explicitly accept:

1. BTX/1.0 and D-011 status;
2. the consecutive second-ID-3 opt-in mechanism;
3. IDs 12–15 and reuse of correlated ID 8;
4. state enums, availability and result semantics;
5. artist 96/title 127 bounds and HOME formatting;
6. callback-based playback authority and source/phone generation rules;
7. resource limits and TUNER-first rollout.

Until that approval is recorded, BTX/1.0 remains PROPOSED and neither firmware implementation is assigned.
