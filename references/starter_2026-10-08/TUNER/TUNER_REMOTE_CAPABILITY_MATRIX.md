# TUNER//01 to REMOTE//01 capability matrix

2026-10-07; baseline main371cdeb / firmware1.1.0. Internal/external columns are **VERIFIED CURRENT IMPLEMENTATION** from [audit](TUNER_IMPLEMENTATION_AUDIT.md). Requirement/action columns are **DESIGN REQUIREMENT**; unimplemented capabilities remain **UNKNOWN / REQUIRES IMPLEMENTATION**. External means existing HTTP, unless explicitly serial; not a Native capability claim.

| Capability | Internal implementation | External exposure | Stable identity/state available? | REMOTE requirement | HA/openHAB relevance | Action required |
|---|---|---|---|---|---|---|
| Radio play URL | HTTP(S) MP3/AAC decoder start | No HTTP; mode-dependent serial UI | URL only; no media generation | Explicit verified play | Media play/select | Serialized owner, context/result contract |
| Radio pause/resume | Gain mute + decoder task stops while paused | Serial UI toggle only | Local state, no stream-time guarantee | Explicit operations, truthful variant | Pause/play | Resolve semantics; no toggle substitution |
| Stop | Internal teardown | No HTTP command | NONE/STOPPED on explicit stop | Declared stop side effects | Stop | Owner command and observation |
| Next/previous | Saved list wrap; discoveredNext adds favorite/Prev unavailable | Serial mode-dependent | Mutable index; no traversal context | Advertise per-context behavior | Track/station traversal | Separate favorite action; guard empty list |
| Volume absolute/step | 0..100,+/-5; BT mapped0..127 | No HTTP; serial steps | Numeric level only, unsynchronized getter | Normalized mapping, explicit level | Volume control | Fix step underflow; serialized validated setter |
| Source selection | Radio/ClassicBT local paths | Serial UI only | Enum, no durable source IDs | Source catalog/select | Source selector | Define catalogs/identity/availability |
| Playback/source/codec/URL | Local diagnostics snapshot | GET /api/diagnostics | Partial mutex, no generations; BT state optimistic | Verified coherent snapshot | State/availability | Fix truthfulness/synchronization; sanitize URLs |
| Current station name/identity | UI name plus saved index | Name only via catalogs/serial; URL diagnostics | No durable current-item ID | Current context | Media title/channel | Unified current-item snapshot |
| ICY title | Protected caller-owned copy | Serial/UI, not HTTP metadata | Text, no media-context version | Metadata bound to current media | Media title | Add guarded snapshot fields |
| Bluetooth audio | A2DP sink/SBC | Phone ClassicBT, diagnostics source | Live connection getter | Only supported BT controls | BT source/player | Distinguish connected from playing |
| BT metadata/AVRCP | Artist/title, play/pause toggle,next,prev | PhoneBT/local input, not HTTP | Optimistic toggle; shared text snapshot | Verified actions/state | Media transport | Explicit operations/feedback and safe copies |
| Saved stations | 15 persistedNVS append/delete | GET/POST stations, DELETE station | Array positions only | Native catalog if supported | Browse/select | DurableIDs, revisions, strict parsing |
| Native Favorites | 10 persistedNVS exactURL dedup | GET stations favorites/DELETE favorite | Array positions only | DEVICE_NATIVE favorites | Favorites/presets | Codec consistency; stable selection/activation |
| Recent | 5 persistedNVS discovered-attemptMRU | No HTTP | Reorderedpositions | Optional truthful history | Recent browsing | Decide semantics/export; IDs/context |
| Directory search | Countries/tags/MP3AAC results | Local/serial UI only | URL/name, no UUID retained | Optional catalog discovery | Browse | Bound/background work and identity policy |
| Artwork | No pipeline in TUNER | None | None | REMOTE owns lookup/cache; context safety | Optional media artwork | Truthful URL/context; retrieval policy separate |
| Wi-Fi provisioning | Saved EEPROM API + setupAP/DNS | POST wifi/status/root | Cached connection can stale | Independent local connectivity | Availability | Runtime truth/recovery; preserve credential policy |
| Device discovery | None (directory lookup is different) | None | MACfragment setupSSID only | mDNS direction + fallback | Device discovery | Define/implement service, not pairing |
| Persistent association | None | None | No Native device identity/registry | Direct standalone association | Optional separate clients | Identity/auth/user approval/revocation/recovery |
| Push/events | None | None | No revisions/sequence gaps | Reconnect/full-state correctness | State updates | Choose bounded polling/push transport |
| Multi-client mutations | Main-loop serialization only; audio-task gaps | Legacy web configuration only | No unified command/results owner | Physical/web/direct coexist | Concurrent automation | Owner/snapshot foundation first |
| Diagnostics | Heap/PSRAM/reset/version/audio | GET diagnostics/status | Build identity; no Native device identity | Debug/availability | Diagnostics | Bounds/redaction; don't infer field truth |
| OTA | No writer; inactive proposedCSV | None | No trust/trial/rollback | Separate required direction | Maintenance | Verify hardware/headroom/security; separate milestone |
| HA/openHAB/MQTT/Matter/BLE-control | No integration code | None | None | Hubs optional | Adapter-specific | Native contract first; no implementation in audit |
