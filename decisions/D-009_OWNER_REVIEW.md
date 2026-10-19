# D-009 owner review package

Status: **PROPOSED / OWNER REVIEW**
Effective revision: NONE
Implementation: NOT AUTHORIZED / NOT STARTED

## Proposed decision

Approve [RTCP/1 D-009](../references/RTCP_1_D009_PROPOSED.md) as the exact additive binding for the first A-REMOTE-013 slice:

- authenticated radio play, pause, previous and next;
- authoritative station name, playback state and bounded now-playing text;
- fixed-list-only previous/next with discovered contexts explicitly unavailable;
- combined ICY StreamTitle unless TUNER owns trustworthy split artist/title fields;
- existing HOME labels and controls only, with no new screen, widget, artwork or carousel change;
- TUNER-first backward-compatible rollout.

## Contract assessment

No CCM 1.1.0 change is required. The proposal uses existing `playback.*`, `playback.state`, `media.title`, `media.artist` and `media.subtitle` semantics with the required media-context generation, freshness, correlation and session rules. Native API v1 remains unapproved and unimplemented.

## Alternatives rejected

- Reusing discovered-mode local Next was rejected because it adds a Favorite and is not `playback.next`.
- Splitting StreamTitle at punctuation was rejected because TUNER has no reliable radio artist/title parser.
- Reusing web-manager endpoints was rejected because they are not the authenticated RTCP binding.
- Adding screens, graphical widgets, station logos or artwork was rejected as outside this slice.
- Sending commands to old firmware without advertised bits was rejected as unsafe and incompatible.

## Owner decision requested

Approve or reject the exact proposed profile, including IDs 9–11, capability bits 3–7, command preconditions, error codes, metadata layout/bounds, CCM field projection, fixed-list traversal restriction and rollout sequence. Approval authorizes specification freeze only; firmware implementation remains a separate task authorization.
