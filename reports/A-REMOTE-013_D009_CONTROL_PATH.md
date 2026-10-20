# A-REMOTE-013 D-009 playback and metadata control path

## Source-backed TUNER authority

| State/action | Actual owner | Evidence and boundary |
| --- | --- | --- |
| selected station name/context | `src/main.cpp`: `nowPlayingName`, `nowPlayingContext` | Updated after successful `playStation()` / `playDiscoveredStation()`; main-loop ownership |
| fixed-list traversal | `handlePlayingInput()`, `CorrectnessGuards::{previous,next}StationIndex()` | Wraps through the saved list; empty/stale selection is refused |
| discovered context | `handlePlayingInput()` | Previous unavailable; local Next adds Favorite, so it cannot be reused by D-009 |
| playback/source | `AudioPlayer::playbackState`, `currentSource` in `src/audio.*` | Audio mutex protects lifecycle changes; audio task owns decoder service |
| radio metadata | `AudioPlayer::nowPlaying[256]` and `nowPlayingMux` | ICY `StreamTitle` callback supplies one combined string; `getNowPlaying()` makes a bounded copy |
| radio play/pause | `AudioPlayer::resume()` / `pause()` | Explicit state transitions; D-009 must not emulate them with a toggle |
| RTCP session | `src/rtcp_server.*`, `src/ccm_wire.*` | Main-loop-polled authenticated server, fixed 512-byte plaintext buffers |

The smallest safe TUNER implementation adds a bounded queue/projection owned and serviced by the existing main loop. RTCP decoding validates and enqueues one command. The main loop performs only the approved radio operation and returns a correlated outcome. It does not call the general UI input handler because that handler has context-dependent Favorite and Bluetooth behavior.

## Source-backed REMOTE path

The existing path is retained:

`HOME touch/input -> user_app bounded intent -> control_home::Facade -> CCM admission -> RtcpDevice -> rtcp_client -> TUNER -> correlated result + authoritative refresh -> Core -> HOME mailbox -> LVGL timer`.

Required additions are limited to wire codecs for IDs 9–11, capability registration, D-009 dispatch/result mapping, metadata observations and the existing HOME controls/text binding. Single-in-flight, no retry, session generation and freshness remain unchanged.

## State transition rules

1. Successful identity and capability exchange still precede any application feature.
2. Existing snapshot establishes playback state and media generation.
3. Now-playing response with the same generation establishes station/metadata and contextual operation availability.
4. A station/source transition increments generation and invalidates old track text before new text is accepted.
5. Command admission captures fresh state and generation. TUNER compares both before execution.
6. Command result completes/refuses the request; it does not manufacture playback/media truth.
7. An immediate state + now-playing refresh supplies authoritative post-command observations.
8. Disconnect, sleep or session replacement clears pending state and current UI truth; reconnect resynchronizes.

## Confirmed limitations

- Radio artist/title are not independently owned in v1.1.12. Only combined StreamTitle is trustworthy.
- Fixed saved stations have ordered traversal. Discovered/favorite/recent playback does not.
- Bluetooth metadata and AVRCP are excluded even though separate Bluetooth title/artist storage exists.
- No station identity/catalog or artwork feature is added; those remain D-010 scope.
