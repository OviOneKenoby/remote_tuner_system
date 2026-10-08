# TUNER//01 and REMOTE//01 implementation plan

2026-10-07. **DESIGN REQUIREMENT** planning only. Baseline main371cdeb/v1.1.0; [audit](TUNER_IMPLEMENTATION_AUDIT.md) supplies evidence and defects. No transport/device-ID/API freeze, firmware change, upgrade, build or upload authorized by this document.

## Dependency order and acceptance gates

| Order | Workstream | Scope | Gate / evidence required |
|---|---|---|---|
| 1 | TUNER firmware | Control/state correctness foundation: regress source-proven failures, strict indexed mutation validation, empty-list/traversal safety, truthful codec/state/volume outcomes and persistence errors. Define one mutation authority and copied coherent snapshots; preserve audio lifetime lock/working output. | Focused deterministic tests for B01-B11 as applicable, normal radio/AAC+/BT/web/encoder hardware regression; no unmeasured concurrent writer assumption. |
| 2 | Shared protocol documentation | Specify semantic subset, stable device/source/station identities, catalog/media/session contexts, observed state, admission/completion evidence, command/result correlation, stale selections, retries/dedup/barriers, bounds and multi-client ordering. Reconcile current mute/BT/Next semantics with frozen CCM without changing CCM. | Reviewed unambiguous conformance vectors; unsupported/unknown distinctions and owner decisions explicit. |
| 3 | Shared protocol + TUNER design | Select transport and discoveryservice details; persistent association/user approval/auth/revocation/reset scope and DHCP/multiple-device recovery. Budget sockets/queues/body sizes/timeouts/history; benchmark memory constraints. | Transport/security/identity review before NativeAPIv1 freeze; mDNS direction not equivalent to pairing. |
| 4 | TUNER firmware | Implement selected bounded Native API over authoritative owner and snapshots, discovery advertisement and association persistence. Keep existing provisioning independent. No HA/openHAB mandatory gateway. | Endpoint/schema/security/correlation tests, slow-client/load/reconnect/power-loss tests; measured radio/BT/TLS/client coexistence. |
| 5 | REMOTE firmware | Native adapter through existing protocol-neutral Core, association UI/storage, discovery/manual fallback, state/catalog mapping and sleep reconnect. Read TUNER favorites; no local radio decoding or REMOTE favorite station DB. Artwork remains REMOTE-owned, context-safe. | FrozenCCM adapter vectors; stale replies/selections, uncertain execution, first-touch wake and network-recovery tests; no direct UI bypass of Core. |
| 6 | Hardware end-to-end | Direct REMOTE/TUNER onLAN with hubs absent, playback/volume/favorite activation, physical+web+REMOTE concurrency, DHCP/AP restart, REMOTE sleep, TUNER restart, multipleTUNER/unpair/replacement. | Owner physical acceptance plus bounded heap/task/client/resource measurements; no synthetic success from local command admission. |
| 7 | Optional smart-home adapters | HA integration and openHAB binding/adapter use same stable Native contract. Define supported media/source/catalog mappings, availability, optional discovery and client auth. | Hub-independent operation remains PASS; adapter tests incl concurrent direct control and stale state/reconnect. |
| Separate | TUNER OTA/resources | Confirm physical flash; finalartifact measurements, layout/trust/transfer/trial/rollback design and tests. Current proposed4MiB margin insufficient; REMOTE16MiB migration does not authorize TUNER layout. | Separate owner-approved milestone; no OTA implementation now. |

Step1 is the recommended next implementation milestone: **TUNER control/state correctness and ownership foundation**, with exact corrective scope approved separately. Do not bolt playback routes onto the current mutable getters. Decompose foundation changes so working audio is regression-tested after each correction; this audit is not authority to refactor or apply all fixes in one pass.

## Decisions required before Native API v1 freeze

- Supported first-release operation/source/catalog subset; true radio pause variant, BT explicit command/observation guarantees and traversal policy.
- Durable device/station identity allocation/continuity and catalog selection guards; URL changes/duplicates/replacement semantics.
- Command acceptance versus execution evidence, result correlation/dedup/retention, ordering and reconnect uncertainty rules.
- Request/response versus bounded push; transport security/authentication/replay; mDNS service/TXT/ports and fallback behavior. No automatic WebSocket+HTTPS freeze.
- Persistent association lifecycle/authorization for multiple REMOTEs/automation clients; revocation/replacement/reset erase domains. Discovery alone is insufficient.
- State freshness/gap/full-snapshot rules after REMOTE sleep and TUNER restart; BT metadata/playback unknown handling.
- Concrete resource/client/message bounds demonstrated alongside MP3/AAC+/TLS/BT; no reliance on old reference build size.
- Native asset/context exposure consistent with REMOTE-owned artwork; private URL credentials not leaked into common/UI fields.

TUNER station/Favorites/Recent persistence exists today; REMOTE-owned association/settings/artwork are recovered product direction, not unimplemented TUNER storage proof. No hub dependency and physically separate audio ownership are requirements already established, not open design choices. Frozen CCM1.0.0 stays unchanged; any mismatch requires an explicit adapter contract or TUNER correction, not model relaxation.

## Verification boundary for this audit

Four documents created plus historical CHANGELOG appended. Validation: source/routes/constants/ancestry cross-check, relative links and docs-only git diff. No build/test/hardware results fabricated. Current release artifact size, runtime heap margins and new Native behavior remain unmeasured/unimplemented.
