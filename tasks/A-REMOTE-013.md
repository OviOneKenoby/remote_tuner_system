# A-REMOTE-013: Functional Controls and UI Integration

- Owner: REMOTE//01 with coordinated TUNER//01 changes
- State: PLANNING / OWNER REVIEW
- Coordination baseline: planning PR #19 merged at `aa45826492d78714ce58221ea2a832adb52ac73f`
- TUNER baseline: v1.1.12, executable source `d112dd0bbef7d86bd22090ec75d76cad3be77677`, integration merge `4977b49756820edc149acbe1abe4d387a96aa992`
- REMOTE installed baseline: 2,526,848-byte application, SHA-256 `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da`
- Objective: extend the accepted authenticated REMOTE/TUNER link from volume-only control to bounded playback, station navigation, authoritative UI state and selected-station logo support.
- Phase 1 scope: source audit, gap analysis, decisions, implementation sequence and hardware acceptance planning only.
- Exclusions: firmware edits/builds/flashing, device access, CCM changes, Native API implementation, pairing/NVS/partition changes, MQTT, SmartThings and AAC/AAC+.
- Acceptance for Phase 1: a source-backed planning package and reviewable unmerged PR. Firmware implementation requires a separate owner decision.

## Verified starting point

A-REMOTE-012 remains **CLOSED / ACCEPTED** and is not reopened. TUNER v1.1.12 is the published hardware-tested baseline: 2,037,632 bytes, SHA-256 `6d7f2ebfa833bd09f287b8a7024071d736dfb2bf02356f889de94d7b980fdf6a`. The private REMOTE baseline identity above was reverified locally without publishing the artifact. The current RTCP/1 binding provides authenticated identity, capability and state synchronization for `volume.level`, `playback.state`, and correlated `volume.set`; rapid volume, reconnect, sleep/wake, MP3, A2DP and HTTP/RTCP coexistence retain their accepted A-REMOTE-012 evidence.

CCM 1.1.0 remains OWNER APPROVED / FROZEN. The Native API v1 proposal remains UNAPPROVED / UNFROZEN / NOT IMPLEMENTED, and O01-O17 remain open. A-REMOTE-013 may reuse existing CCM semantics, but an exact RTCP application-binding extension and its bounds require owner approval before implementation.

## Phase 1 deliverables

- [Capability matrix](../reports/A-REMOTE-013_CAPABILITY_MATRIX.md)
- [Control path and protocol gaps](../reports/A-REMOTE-013_CONTROL_PATH_AND_PROTOCOL_GAPS.md)
- [Resource and risk assessment](../reports/A-REMOTE-013_RESOURCE_RISK.md)
- [Incremental implementation plan](../reports/A-REMOTE-013_IMPLEMENTATION_PLAN.md)
- [Unexecuted hardware acceptance checklist](../protocols/A-REMOTE-013_HARDWARE_ACCEPTANCE.md)
- [Exact proposed D-009 profile](../references/RTCP_1_D009_PROPOSED.md)
- [D-009 owner-review record](../decisions/D-009_OWNER_REVIEW.md)
- [Proposed D-009 implementation task](A-REMOTE-013-D009-IMPLEMENTATION.md)
- [D-009 unexecuted hardware protocol](../protocols/A-REMOTE-013-D009-HARDWARE-VALIDATION.md)
- Proposed decisions D-009 and D-010 in the [decision register](../DECISION_REGISTER.md)

## Phase 1 result

The source audit found that TUNER already owns most local playback, radio browsing, Favorites, Recent, Bluetooth and metadata behavior. REMOTE already has authenticated volume control, input acquisition, a HOME control surface and bounded persistence. The missing layer is an approved, bounded, authoritative RTCP application binding for playback/source/catalog/media data plus REMOTE UI adapters. Station entries have no durable opaque identity, current RTCP plaintext is limited to 512 bytes, and no production station-logo locator/cache pipeline exists.

The recommended first implementation task is the smallest independent slice: freeze an additive RTCP/1 playback-control profile for `playback.play`, `playback.pause`, `playback.previous` and `playback.next`, plus authoritative playback/media feedback. It must remain capability-gated, correlated, session-fenced and backward compatible with the volume-only binding. Stop/resume, mute, Bluetooth source selection and all station catalogs remain outside that first slice until their open semantics are decided.

No firmware repository, binary, device, credential, pairing record, NVS partition or published release was changed in Phase 1.
