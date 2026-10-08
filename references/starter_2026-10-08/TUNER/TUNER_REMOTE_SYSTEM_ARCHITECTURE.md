# TUNER//01 and REMOTE//01 system architecture

2026-10-07. **DESIGN REQUIREMENT**, not an implemented or frozen Native API. Actual baseline/support and defects: [implementation audit](TUNER_IMPLEMENTATION_AUDIT.md).

## Product boundary

TUNER owns internet-radio stream acquisition, decoding, audio output, native stations/Favorites/Recent and authoritative media state. REMOTE is a physically separate, direct LAN client: it does not decode radio audio and works without Home Assistant/openHAB. Optional smart-home systems are additional clients, not required gateways or the primary command/state owner.

```text
TUNER authoritative command/state owner
             |
      stable TUNER Native API
             |
      +------+----------------+----------------+
      |                       |                |
REMOTE direct client   optional HA adapter  optional openHAB adapter
      |                       |                |
protocol-neutral Core    system-specific mappings    future clients
```

Physical controls and existing web manager must converge on the same TUNER command/state authority as future LAN clients. Preserve the working decoder/I2S chain and its lifetime synchronization. No independent endpoint may synthesize state from a button gesture or rewrite shared media structures concurrently. A future ownership mechanism must serialize validated mutations, return truthful admission/execution results and publish bounded immutable observations with identity/context. This document does not prescribe a new task/queue implementation.

## Identity, discovery and association

Recovered REMOTE decision register selects mDNS discovery with manual IP/hostname fallback allowed; TUNER does not implement it today. Service name, TXT fields, port and Native device-ID format remain unresolved. A discovered address is only a candidate endpoint, not an authenticated association.

Explicit user association must bind persistent device identity and authorization, survive reboot/DHCP changes and distinguish multiple TUNERs. Unpair/replacement must invalidate previous authorization and stale work. Persistent identity must not be an IP address, friendly name, array index or truncated MAC fragment. Hardware MAC is an available input, not an approved final identifier format. Pairing storage/secret exchange/revocation/reset scope require design before implementation.

## State and control contract

REMOTE CCM1.0.0 remains frozen and protocol-neutral. Native wire representation is separate; an adapter needs evidence for every advertised capability, context guard, selection token, completion claim and retry guarantee. Preserve distinct native favorites and remote-recipe semantics; this product's station persistence belongs on TUNER. Current mute-pause, discovered Next=add-favorite and optimistic BT toggle must be described truthfully or corrected before mapping explicit operations.

Define current source/media identity, observed playback, volume and catalogs independently of UI focus/mode. Station IDs and catalog generations must survive reorder without targeting a different item. Media/context revisions must prevent stale title/artwork mixing. REMOTE owns active-stream artwork lookup/retrieval/cache/display according to the recovered decision register; TUNER must provide truthful context/locator data, not invent artwork support. Asset/security boundary and exact retrieval policy remain design work.

After REMOTE sleep/network loss, reacquire identity/session/current state and invalidate stale selections/unsent work. Never blindly replay commands with unknown execution outcome. Define multi-client ordering, correlation, deduplication, bounded history and authority for physical/web/REMOTE/HA/openHAB alike.

## Transport, security and resources

No transport freeze: synchronous HTTP/JSON is existing infrastructure, WebSocket/push/MQTT are absent. Compare bounded polling versus push with reconnect, client/socket quotas, backpressure, latency, fragmentation and radio/BT coexistence evidence. MQTT integration cannot introduce a mandatory broker for REMOTE operation. mDNS is discovery, not transport security.

Current port80 mutations are unauthenticated; setup MAC-derived password is not random association security. Define authorization, replay policy, request bounds and safe error/redaction rules before Native mutation is exposed. Existing WEB_SECURITY OTA proposal is not automatically the Native authentication design. REMOTE's no-password LAN OTA product access decision does not authorize unauthenticated TUNER control or change image trust requirements.

TUNER has an active single-app 4MiB-target layout and historically tight hypothetical dual-slot margin. Do not transplant REMOTE's16MiB partition layout or enable OTA here. Measure exact future artifacts and runtime budgets before accepting API/integration capacity.

## Evidence gates

Current implementation: legacy web manager, radio/BT audio and local catalogs only. Standalone Native control, persistent association and HA/openHAB compatibility are **UNKNOWN / REQUIRES IMPLEMENTATION**. Only hardware regression plus protocol/adapter conformance can promote these to verified support. See [dependency plan](TUNER_REMOTE_IMPLEMENTATION_PLAN.md).
