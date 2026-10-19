# A-REMOTE-013 control path and protocol gaps

## Existing production path

The accepted path is:

`REMOTE GPIO/touch -> user_app input router -> control_home/Core admission -> RtcpDevice::dispatch -> rtcp_client::Client -> encrypted RTCP/1 record -> rtcp_server::handleApplication -> AudioPlayer::setVolume -> command result + snapshot -> RtcpDevice::poll -> Core observation -> LVGL HOME refresh`.

The path is authenticated, counter-checked, capability-gated, correlated, single-in-flight, session-fenced and non-retrying. Disconnect, sleep and session changes invalidate pending intent. This behavior must remain the template for new controls.

## Current wire surface

TUNER `src/ccm_wire.h` and REMOTE `components/rtcp_client/wire.*` define only:

1. identity request/response;
2. capability request/response;
3. snapshot request/response;
4. `volume_set`;
5. command result.

The capability response advertises volume observation, playback observation and volume-set support. The snapshot contains volume, a playback value, sequence and media generation. `RtcpDevice::install` registers `volume.set`, `volume.level` and `playback.state`; `RtcpDevice::dispatch` rejects every operation except `volume.set`. RTCP plaintext is capped at 512 bytes.

## Required paths and their first missing link

| Function | Intended end-to-end path | First missing link | Required error behavior |
| --- | --- | --- | --- |
| Play/pause | REMOTE touch/KEY -> Core operation -> RTCP command -> `handlePlayingInput`-equivalent owner -> playback snapshot -> HOME | Approved RTCP command IDs/payloads and TUNER owner adapter | Reject when wrong source/state; correlate result; no retry after uncertain delivery |
| Previous/next | REMOTE touch/buttons -> Core -> RTCP -> guarded TUNER traversal -> station/media snapshot | Traversal semantics and RTCP binding | Empty/mutated catalog must fail without wrap/underflow or stale selection |
| Source select | REMOTE source UI -> Core `source.select` -> RTCP -> radio/BT lifecycle owner -> source snapshot | Stable source IDs and Bluetooth availability semantics | Fail closed on unavailable BT; retain current source truth |
| Station select | REMOTE catalog selection reference -> Core guard -> RTCP -> TUNER station authority -> media/catalog state | Durable station ID, catalog generation, paging and activation message | Reject stale/deleted/mismatched generation; never select by mutable array index alone |
| Favorites/Recent | TUNER catalog snapshot/page -> REMOTE Core/UI -> guarded activation | Production catalog ingress and approved mapping | Complete/partial truth, bounded result, explicit stale/reconnect invalidation |
| Metadata | TUNER copied state -> bounded snapshot -> REMOTE observation -> LVGL | RTCP fields, size/UTF-8 bounds and context generation | Stale metadata must not attach to the next station/source |
| Codec | TUNER codec authority -> optional field -> REMOTE display | No frozen CCM codec field | Remain unknown unless an approved extension exists |
| Station logo | TUNER station identity/approved locator -> REMOTE bounded fetch/decode/cache -> LVGL | Locator policy and all production pipeline stages | No raw private URL disclosure; bounded time/bytes/dimensions; placeholder on failure |

## TUNER ownership

- `src/main.cpp` owns UI mode and current station context.
- `src/audio.*` owns playback, source lifecycle, audio volume, URL, codec and metadata snapshots.
- `src/stations.*` owns saved stations, Favorites and Recent in default NVS.
- `src/browser.*` owns temporary Radio Browser countries/tags/results.
- `src/rtcp_server.*` owns authenticated server sessions and application dispatch.

The new adapter must enter the existing main-loop owner. It must not invoke UI handlers blindly, duplicate state in a network task, or expose web-manager routes as REMOTE control endpoints.

## REMOTE ownership

- `components/user_app/user_app.cpp` owns GPIO sampling, context routing and LVGL updates.
- `components/control/*` owns schema, capability, admission, correlation, freshness and catalog foundations.
- `components/rtcp_client/*` owns secure transport and the current TUNER adapter.
- `components/persistence_backend/*` owns bounded `remote_ctl` durable association state.

Physical-button events are currently distinct but intentionally actionless. The HOME previous/toggle/next widgets and station/navigation rows are present, but capability gating correctly prevents unsupported commands. The intermittent QMI8658 initialization issue belongs to motion wake, not button input.

## Contract blockers

CCM 1.1.0 already names neutral playback and source operations and includes media/reference/catalog structures. Reusing those meanings does not require changing CCM. The missing production RTCP projection still requires explicit approval because it affects both devices, message compatibility and resource bounds.

The Native API v1 proposal is not a shortcut: it remains unapproved and unimplemented. A-REMOTE-013 should extend the accepted RTCP/1 binding rather than declare the Native proposal effective.

Open decisions that block implementation are:

- O07/O14: durable station identity, source/station/traversal roles and guarded selection;
- O13: play, pause, stop, resume and source-specific playback semantics;
- O08: Bluetooth exposure and AVRCP mapping;
- O09: Favorites, Recent, browse and search release scope;
- O11: catalog/page/string/resource limits;
- O12: authoritative revisions and reconnect synchronization;
- O15: station-logo locator, privacy and cache boundary;
- O16/O17: persistence/reset boundary and secure legacy compatibility.

O01/O02/O05/O06 are satisfied for the already accepted RTCP/1 volume profile only. They remain open for the Native proposal and do not automatically approve additional RTCP message types.

## Compatibility recommendation

Use additive capability bits and message types. A new REMOTE must retain volume-only operation with the current TUNER, and a new TUNER must retain the current binding with the current REMOTE. Unknown messages must fail closed without ending an otherwise valid legacy session where the approved framing permits that behavior. Install and validate TUNER first, then REMOTE, for each cross-device slice.
