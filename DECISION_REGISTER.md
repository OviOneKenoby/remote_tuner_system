# Decision register

Never delete previous decisions. Supersede them with a linked new entry. Initial entries record owner-supplied facts; the starter package does not issue new owner approvals.

| ID | Topic | State | Authority/evidence | Impact |
| --- | --- | --- | --- | --- |
| D-001 | CCM 1.0.0 | OWNER APPROVED / FROZEN | Explicit owner instruction for starter; original approval artifact pending | Both devices; no unilateral changes |
| D-002 | TUNER Native API v1 | UNAPPROVED / UNFROZEN / NOT IMPLEMENTED | Explicit owner instruction for starter | Candidate only; implementation gate closed |
| D-003 | TUNER audited baseline | RECORDED FACT | Owner: main commit 371cdebce7ba2648ea71636d5bdb5d738b42e680, firmware 1.1.0; audit pending | Starting audit reference, not current checkout proof |
| D-004 | Common phase | RECORDED FACT | Owner: Phase A contract reconciliation + TUNER correctness/control-state foundation | Shared planning boundary |

## Exact new-decision template

```markdown
### D-<unique-id>: <title>
- Date (UTC): <timestamp>
- Task / proposal ID: <id>
- State: <PROPOSED / UNDER REVIEW / OWNER APPROVED / REJECTED / SUPERSEDED>
- Problem and evidence: <paths, revisions, observations>
- Exact proposed change: <diff or immutable artifact link>
- CCM impact: <none with reason, or exact clauses/version impacted>
- Native API impact: <none with reason, or exact candidate revision impacted>
- REMOTE impact and review: <reviewer, date, result, evidence>
- TUNER impact and review: <reviewer, date, result, evidence>
- Alternatives and compatibility: <assessment>
- Owner approval: <exact scope, date, durable evidence; PENDING if absent>
- Effective approved revision: <revision/hash or NONE>
- Implementation tasks/commits: <separate device references or NOT IMPLEMENTED>
- Verification: <evidence or NOT VERIFIED>
- Supersedes / superseded by: <IDs or NONE>
```

## Phase A open shared design register — imported 2026-10-08
Source: references/starter_2026-10-08/SHARED/TUNER_REQUIREMENTS_FROM_REMOTE.md section24; SHA-256 fc6303f73c231e3abad91171ce0ea29ad05afe2b4c27833c5bd8743f79246c12.
All entries OPEN / UNRESOLVED. Importing/grouping them issues no new owner approval and supersedes none of D-001 through D-004.

| ID | Topic | PM dependency grouping | State |
| --- | --- | --- | --- |
| O01 | Native transport/serialization | Resource-dependent; before API freeze | OPEN |
| O02 | State synchronization | Resource-dependent; before API freeze | OPEN |
| O03 | Device-ID representation | Foundational design | OPEN |
| O04 | mDNS profile | Foundational design; exact profile still open | OPEN |
| O05 | Association/authentication | Resource/security-dependent; before API freeze | OPEN |
| O06 | API port/path layout | Foundational design | OPEN |
| O07 | Station durable-ID policy | Foundational design | OPEN |
| O08 | Bluetooth Native scope | Optional release scope; explicit deferral possible | OPEN |
| O09 | Browse/Recent/search release scope | Optional release scope; explicit deferral possible | OPEN |
| O10 | Command result retention/recovery | Resource/durability-dependent; before API freeze | OPEN |
| O11 | Resource/client bounds | Measurement-dependent; before API freeze | OPEN |
| O12 | Native state/revision contract | Foundational design | OPEN |
| O13 | Playback operation semantics | Foundational design | OPEN |
| O14 | Source/station/traversal mapping | Foundational design | OPEN |
| O15 | Artwork/locator boundary | Full pipeline can defer; privacy before locator exposure | OPEN |
| O16 | Reset/persistence domains | Foundational design | OPEN |
| O17 | Security/legacy coexistence | Resource/security-dependent; before API freeze | OPEN |

### D-009: A-REMOTE-013 additive RTCP playback-control profile
- Date (UTC): 2026-10-19
- Task / proposal ID: A-REMOTE-013 Phase 1
- State: OWNER APPROVED / FROZEN; implementation NOT AUTHORIZED / NOT STARTED
- Problem and evidence: the accepted RTCP binding carries authenticated volume control and playback observation, while TUNER local radio play/pause/previous/next and REMOTE HOME controls are not connected; [gap analysis](reports/A-REMOTE-013_CONTROL_PATH_AND_PROTOCOL_GAPS.md).
- Exact proposed change: [RTCP/1 D-009 proposed profile](references/RTCP_1_D009_PROPOSED.md): retain IDs 1–8 and the 16-byte capability layout; assign capability bits 3–7 and IDs 9 playback command, 10 now-playing request and 11 now-playing response. The exact profile defines state/generation preconditions, result codes 0–7, fixed-list-only traversal, combined StreamTitle behavior, UTF-8 and string bounds, 446-byte maximum plaintext, freshness, session invalidation and mixed-version compatibility. Stop/mute/source/BT/catalog operations are excluded.
- CCM impact: NONE; reuse existing CCM 1.1.0 operation/field meanings without modifying the frozen contract.
- Native API impact: NONE; v1 remains UNAPPROVED / UNFROZEN / NOT IMPLEMENTED and O01-O17 remain open.
- REMOTE impact and review: adapter capability/dispatch/observation additions and existing HOME control/text bindings; generated carousel/graphics unchanged; source audit complete, implementation NOT AUTHORIZED.
- TUNER impact and review: fixed-size main-loop-owned command/projection over existing radio authority; discovered Next Favorite mutation and Bluetooth AVRCP excluded; source audit complete, implementation NOT AUTHORIZED.
- Alternatives and compatibility: implementing Native v1 or exposing web routes was rejected for this slice. Additive capabilities permit old/new volume-only interoperability. TUNER-first installation is recommended.
- Owner approval: PENDING.
- Effective approved revision: NONE.
- Implementation tasks/commits: NOT IMPLEMENTED.
- Verification: exact reviewed commit `4237eadf7e641308a77ba673afadd0e39b52e5d1`; specification SHA-256 `ad6fa343c7ea6363febfffa143c6ffb62e401c19d994abcdaa7287bd0ded6c92`; source review and exact serialized-size calculation only; no build or hardware verification. [Owner approval](references/D009_OWNER_APPROVAL_2026-10-19.md); [decision record](decisions/D-009_OWNER_REVIEW.md).
- Supersedes / superseded by: NONE.

### D-010: A-REMOTE-013 station catalog and selected-logo boundary
- Date (UTC): 2026-10-19
- Task / proposal ID: A-REMOTE-013 Phase 1
- State: PROPOSED / OWNER REVIEW
- Problem and evidence: current station arrays use mutable positions/names/URLs, RTCP has no catalog messages, a 20-item result exceeds current REMOTE resource and 512-byte record assumptions, and no logo pipeline exists; [matrix](reports/A-REMOTE-013_CAPABILITY_MATRIX.md) and [risk assessment](reports/A-REMOTE-013_RESOURCE_RISK.md).
- Exact proposed change: before station implementation, approve TUNER-owned durable opaque station IDs, monotonic catalog revisions, guarded activation, bounded paging/continuation and selected-radio-station-only logo locators. REMOTE owns a bounded volatile logo fetch/decode/cache and placeholder; raw credentials/private payloads are excluded. Exact page, string, image byte/dimension/format and timeout limits require measured design review.
- CCM impact: NONE proposed; use existing reference/catalog foundations. Any missing field or executable slice requires a separate exact CCM proposal rather than silent extension.
- Native API impact: NONE; the unapproved candidate is not made effective.
- REMOTE impact and review: new catalog ingress/UI and bounded logo pipeline; implementation NOT AUTHORIZED; `remote_ctl` use is excluded absent a separate persistence decision.
- TUNER impact and review: durable identity/migration, catalog snapshots/pages and sanitized logo locator; implementation NOT AUTHORIZED.
- Alternatives and compatibility: raw array indices, names or URLs are rejected as durable identity; sending whole catalogs or image bytes in one RTCP record is rejected. Deferring logo and optional browse/search remains compatible.
- Owner approval: PENDING.
- Effective approved revision: NONE.
- Implementation tasks/commits: NOT IMPLEMENTED.
- Verification: source/resource review only; no build or hardware verification.
- Supersedes / superseded by: NONE.

### D-011: RTCP/1 Bluetooth Extension v1
- Date (UTC): 2026-10-22
- Task / proposal ID: Bluetooth RTCP Extension Phase 2
- State: OWNER APPROVED / FROZEN / TUNER IMPLEMENTATION AUTHORIZED
- Problem and evidence: TUNER owns working A2DP, local AVRCP commands and bounded artist/title metadata, but frozen D-009 context 3 intentionally carries no Bluetooth metadata or operation availability. REMOTE therefore cannot present or control those functions without a separate profile.
- Exact approved change: [BTX/1.0](references/RTCP_1_BLUETOOTH_EXTENSION_V1_PROPOSED.md) preserves the first revision-2 ID 3/4 exchange, uses one immediate second authenticated ID 3 as an opt-in probe, and assigns IDs 12–15 for extension capability, bounded Bluetooth state and explicit AVRCP command. Existing correlated result ID 8 is reused. Maximum BTX plaintext/authenticated size is 255/299 bytes.
- CCM impact: NONE proposed; existing source, playback and media meanings remain authoritative and generation-fenced. Frozen CCM 1.1.0 is unchanged.
- Native API impact: NONE; v1 remains UNAPPROVED / UNFROZEN / NOT IMPLEMENTED.
- REMOTE impact and review: session-scoped negotiation, strict codecs, source/metadata/availability projection and a bounded 195-byte HOME title-buffer increase; implementation NOT AUTHORIZED.
- TUNER impact and review: A2DP callback authority, fixed projection and main-loop AVRCP owner; existing metadata arrays and transport buffers are reused; Phase 3 implementation AUTHORIZED.
- Alternatives and compatibility: revision/bit reuse, unsolicited unknown requests, mDNS authority, firmware-version inference and transport-version changes are rejected. [Compatibility matrix](reports/RTCP_BLUETOOTH_EXTENSION_COMPATIBILITY.md) preserves old/new D-009 and volume behavior.
- Owner approval: RECORDED 2026-10-22 for negotiation, IDs/layouts, bounds, state authority, result semantics, resource budgets and TUNER-first rollout; [evidence](references/D011_OWNER_APPROVAL_2026-10-22.md).
- Effective approved revision: BTX/1.0 at proposal head `e5bec2d639ec6c99cd52aabaafa3e52582754105`.
- Implementation tasks/commits: [bounded plan](tasks/RTCP_BLUETOOTH_EXTENSION_IMPLEMENTATION_PLAN.md); TUNER Phase 3 ASSIGNED / IN PROGRESS; REMOTE NOT AUTHORIZED.
- Verification: deterministic public application-codec vectors and 17 focused host tests PASS; no production build or hardware verification.
- Supersedes / superseded by: NONE; D-009 and D-010 remain separate.

Product boundaries, direct LAN operation, TUNER catalog ownership, REMOTE artwork ownership and mDNS discovery direction are already recorded in the supplied canonical handoff; this table does not reopen them. Optional deferral is a future explicit release-scope decision, not silently enacted here.

## Administrative PM assignment record
At 2026-10-08T13:55:34Z, PM assigned A-REMOTE-001 and A-TUNER-001 under the owner's current request to inspect the common repo and decide work for both chats. Exact task files and PROJECT_SYNC.md are the assignment evidence. Inspection/documentation scope only; no firmware/Native implementation or O01-O17 closure. A-PM-001 indexing is complete for available evidence; final approved-model provenance remains pending.

## PM follow-up publication record - 2026-10-08
Both owner-reviewed A-001 inspection/documentation deliveries are integrated and complete for that scope. Recovered CCM artifact/provenance is available in REMOTE A-001 evidence; earlier missing-evidence entries remain historical. [Authorization index](references/PM_FOLLOW_UP_INDEX.md) links the unchanged owner package and exact A-002 assignments. A-TUNER-002: bounded internal guards; A-REMOTE-002: design only. No new CCM/Native approval or O01-O17 closure. Common gate OPEN / NOT PASSED; hardware gaps remain explicit in PROJECT_SYNC.md.


### D-005: Current TUNER final v1.1.11 factual baseline
- Date (UTC): 2026-10-11T17:37:47Z
- Task / proposal ID: A-PM-003 reconciliation
- State: OWNER APPROVED
- Problem and evidence: D-003 initial 1.1.0 and A-TUNER003 artifact are historical; [current report](reports/TUNER_V1_1_11_RECONCILIATION.md), [release metadata](references/pm/2026-10-11/tuner-v1.1.11/release.json).
- Exact proposed change: Current pointer main/tag/merge `5fb92c95d228d744d1182ae3956e850c5be2f277`, executable source `124e84801b06f9e07764dabc3985a573dffaff3b`, build_git_id `124e84801b06`; history preserved.
- CCM impact: none; D-001 remains frozen, no semantics/version/approval changes.
- Native API impact: none; D-002 UNAPPROVED/UNFROZEN/NOT IMPLEMENTED, O01-O17 OPEN.
- REMOTE impact and review: PM 2026-10-11T17:37:47Z; no device acceptance; A003/A004 reviewed production BLOCKED, [PM report](reports/A-PM-003_RECONCILIATION.md).
- TUNER impact and review: PM 2026-10-11T17:37:47Z; public PR5/main/tag/final release/assets checked; functional PASS only recorded BT/web/ping/recovery windows, zero-DMA FAIL and 30-minute soak NOT COMPLETED.
- Alternatives and compatibility: retain D-003/old reports historical, no case-specific hardware acceptance inferred.
- Owner approval: 2026-10-11 functional acceptance/merge/release scope in pinned FINAL_VALIDATION; [technical reconciliation scope](references/PM_RECONCILIATION_SCOPE_2026-10-11.md). No new shared approval.
- Effective approved revision: v1.1.11 / `5fb92c95d228d744d1182ae3956e850c5be2f277`, executable source above; explicit esp32-lwip-psram.
- Implementation tasks/commits: firmware PR5 previously merged; no firmware implementation in A-PM-003; coordination merges recorded in PM report.
- Verification: all five release asset SHA checks PASS; pinned functional hardware PASS with limits; B01/B03/B06/B04 empty/stale physical PENDING, full B04/B02/B05/B07-B11 unresolved.
- Supersedes / superseded by: D-003 only as current baseline pointer; D-003 retained historical; superseded by NONE.

### D-006: REMOTE v1 practical rollback model
- Date (UTC): 2026-10-11
- Task / proposal ID: A-PM-005 / P-REMOTE-V1-001
- State: PROPOSED / NOT APPROVED
- Problem and evidence: PR10 normal merge `4588adc63c4856d31f144913aad59e599993c233`; [review](proposals/P-REMOTE-V1-001/PR10_REVIEW.md); A005 strict G1 FAIL/acceptance BLOCKED.
- Exact proposed change: [normative diff](proposals/P-REMOTE-V1-001/CCM_EXACT_DIFF.patch), SHA256 `90d40c161d9d5b87fc83ec5a4daa1cb1e74f410647f9380f68c17651fd07d8a6`; [manifest](proposals/P-REMOTE-V1-001/DIFF_MANIFEST.json).
- CCM impact: proposed section2 qualification/new12.1 only, separately approved new revision required; frozen1.0.0 unchanged.
- Native API impact: NONE; UNAPPROVED/UNFROZEN/NOT IMPLEMENTED, O01-O17 OPEN.
- REMOTE impact and review: PM2026-10-11 [desk review](proposals/P-REMOTE-V1-001/REMOTE_REVIEW.md), conditionally implementable design, backend NOT QUALIFIED.
- TUNER impact and review: PM2026-10-11 [desk review](proposals/P-REMOTE-V1-001/TUNER_REVIEW.md), no required firmware/storage/authority/protocol change; no independent device-session approval claimed.
- Alternatives and compatibility: strict monotonic service retains old threat scope; practical model excludes coherent adversarial restoration only; [migration/task bounds](proposals/P-REMOTE-V1-001/IMPLEMENTATION_AND_MIGRATION.md).
- Owner approval: PENDING; [exact wording](proposals/P-REMOTE-V1-001/OWNER_APPROVAL_REQUIRED.md); current request authorizes proposal, not exact diff approval.
- Effective approved revision: NONE; CCM1.0.0 still effective.
- Implementation tasks/commits: NOT IMPLEMENTED;006-009 proposed only, D1-D5 unassigned.
- Verification: PR10 reproduction PASS;12 capacity ledger cases; physical NOT RUN; [proposal](proposals/P-REMOTE-V1-001/README.md).
- Supersedes / superseded by: NONE; no approved decision superseded.

## D-006 owner approval and CCM1.1.0 publication - 2026-10-11
P-REMOTE-V1-001 exact PR11 head03c1be0b34df6ff9904cdaf78a0f5de79fd7ac0c is OWNER APPROVED by [exact scope](references/P_REMOTE_V1_001_OWNER_APPROVAL_2026-10-11.md). Current new revision [CCM1.1.0](references/CCM_1_1_0.md) OWNER APPROVED/FROZEN; [publication hashes](references/CCM_1_1_0_PUBLICATION.json). Supersedes only the prior pending-approval/current1.0.0 pointer for this approved REMOTE persistence threat delta; historical1.0.0/proposal/reviews/old task verdicts remain unchanged. G1a REQUIRED, G1b OUTSIDE for intentional complete coherent restoration. This is contract publication, not implementation or device acceptance. Capacity48KiB conditional recommendation; actual capacity/ordering/durability/migration unqualified. Core/NVS/partition/firmware/Native/TUNER/hardware untouched. Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED, O01-O17 OPEN, common gate OPEN/NOT PASSED;006-009/D1-D5 unassigned. No automatic task execution.

D-006 state: OWNER APPROVED. Effective approved revision: CCM1.1.0, frozen. Owner evidence above; exact patch SHA25690d40c161d9d5b87fc83ec5a4daa1cb1e74f410647f9380f68c17651fd07d8a6. D-0011.0.0 approval remains historical; no other decision superseded. Implementation NOT IMPLEMENTED.

### D-007: Dedicated REMOTE control storage layout
- Date (UTC): 2026-10-11
- Task / proposal ID: A-REMOTE-006 layout analysis
- State: PROPOSED
- Problem and evidence: [A006 report](reports/A-REMOTE-006_FLASH_LAYOUT.md); current24KiB insufficient under conservative control profile, physical capacity UNKNOWN.
- Exact proposed change: [64KiB patch](references/device_evidence/remote/A-REMOTE-006/A_64KiB.patch); [48KiB fallback](references/device_evidence/remote/A-REMOTE-006/B_48KiB.patch); not applied.
- CCM impact: NONE;1.1.0 frozen preserved, G1a REQUIRED/G1b OUTSIDE; mandatory history/barriers/non-reuse retained.
- Native API impact: NONE; unapproved/unfrozen/not implemented.
- REMOTE impact and review: PM/REMOTE direct read-only analysis,64 preferred conditional, physical/deployment BLOCKED; all4036 existing files unchanged.
- TUNER impact and review: NONE; no TUNER code/storage/authority/protocol obligation or task.
- Alternatives and compatibility:48 conditional minimum; current negative witness; single-table update/old firmware authority compatibility unresolved; migration report.
- Owner approval: PENDING for layout and safe deployment/recovery route. Current authorization is analysis only.
- Effective approved revision: NONE for partition/layout; current CCM1.1.0 remains effective.
- Implementation tasks/commits: NOT IMPLEMENTED; next007 recommendation unassigned.
- Verification: selected5.5.3 offline decode/reencode/alignment/slot checks PASS; physical NOT RUN, source/flashed UNKNOWN.
- Supersedes / superseded by: NONE; D-006 remains approved contract scope only. O01-O17/gate OPEN.

### D-008: Owner-approved REMOTE v1 dedicated control layout and USB migration architecture
- Date (UTC): 2026-10-11
- Task / proposal ID: A-REMOTE-006/A-REMOTE-007; A-REMOTE-008 source-to-build gate
- State: OWNER APPROVED (architectural target only)
- Problem and evidence: D-007 already PROPOSED; [A007 report](reports/A-REMOTE-007_DEVICE_IDENTITY.md) verifies16MiB, exact table, factory/local image and erased64KiB candidate. PR13 normal merge `72875788767840d27c7085faf994b012d1babefd` accepts bounded observations only.
- Exact proposed change: approved data/nvs remote_ctl offset0xE20000 size0x10000/64KiB, [A006 exact layout](references/device_evidence/remote/A-REMOTE-006/A_64KiB.csv);48KiB fallback unselected. Existing partitions/two3MiB OTA slots preserved.
- CCM impact: NONE; CCM1.1.0 OWNER APPROVED/FROZEN, G1a and all fail-closed/no-replay/barriers/non-reuse/capacity/migration obligations retained.
- Native API impact: NONE; UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; O01-O17 OPEN.
- REMOTE impact and review: A006 layout analysis and A007 exact evidence verified; physical facts accepted, source-to-build UNKNOWN pending A008. No implementation/flash/authority activation.
- TUNER impact and review: NONE; no TUNER change or task/approval inferred.
- Alternatives and compatibility:48KiB fallback not selected; migration ONLY controlled service USB, OTA partition-table migration excluded; interrupted migration recovery through ROM bootloader mandatory. Recovery procedure NOT QUALIFIED; exact downgrade boundary required before new authority activation.
- Owner approval: [technical scope](references/REMOTE_V1_LAYOUT_OWNER_APPROVAL_2026-10-11.md), owner2026-10-11 explicit layout/service/recovery architecture approval; no hardware writes authorized.
- Effective approved revision:64KiB architectural layout target; installed table remains existing six-partition layout. Production/backend/migration qualification NOT GRANTED.
- Implementation tasks/commits: NONE; A008 private reproducibility only, A009 not started/assigned.
- Verification: PR13 head8c6135b298783e740cce7b334d7c8b894075d04d;21 evidence/369 canonical hashes PASS;4036 original workspace files unchanged; owner basic return confirmed. No persistent-write command; source-to-build UNKNOWN.
- Supersedes / superseded by: D-007 pending layout-selection scope only; historical proposal unchanged. D-006/CCM unchanged; superseded by NONE. O01-O17/common gate OPEN/NOT PASSED.

## A008 conditional exclusion verification — 2026-10-12T04:05:06Z
Owner2026-10-12 conditionally authorizes full esp_wifi_bsp transfer omission only after every requested no-influence/invariance test, with all new material in English. [Disposable A/B results](references/device_evidence/remote/A-REMOTE-008/EXCLUSION_CHECK_REPORT.md): configuration exits0/0; effective list and1449 full compiler commands unchanged, sdkconfig/CMakeCache/build.ninja byte-identical. Generated project_description.json all_component_info loses the excluded component discovery/dependency entry; no selected-code dependency found, but strict no-generated-record/configuration/graph-change condition is not met. Remaining preprocessing/transitive-header/full-link/artifact/dependency certificates not completed after gate. No transfer exclusion/bundle/protocol/full secret scan/second-host tests. Restricted component directory hash remains local/unpublished, originals intact. Owner clarification required only for non-selected discovery metadata variance; no exception applied. A008 IN PROGRESS, verdict INCONCLUSIVE — BUILD REPRODUCTION BLOCKED BY INTERMITTENT COMPILER PROCESS FAILURE; source-to-build UNKNOWN. A009 BLOCKED/NOT STARTED, PR14 OPEN/unmerged. CCM/Native/TUNER/O01–O17/common gate and hardware/production gaps unchanged.

## A008 permitted-discovery-metadata continuation — 2026-10-12T04:31:08Z
Owner2026-10-12 permits exact non-selected discovery delta only; prior metadata-only blocker superseded. [Current verification](references/device_evidence/remote/A-REMOTE-008/EXCLUSION_PREPROCESS_REVIEW.md): actual SCons1549 command entries identical; RGB preprocessing byte-identical/no normalization, app-descriptor preprocessing differs only __TIME__-derived .time initializer. Temporal macro difference, no attribution to component omission or source/hardware defect. Macro/source-content normalization not applied under owner limits. EXCLUSION NOT VALIDATED; remaining all-unit/transitive/full-link/generated-input/dependency/clean-build proofs incomplete, no bundle/secret-scan/protocol/transfer/second-host run. Raw negatives/restricted directory hash remain private; originals unchanged. A008 IN PROGRESS; INCONCLUSIVE — BUILD REPRODUCTION BLOCKED BY INTERMITTENT COMPILER PROCESS FAILURE, source-to-build UNKNOWN. A009 BLOCKED/NOT STARTED, PR14 OPEN/unmerged, no firmware/SDK/hardware/CCM/TUNER/Native/gate changes.

## A008 controlled temporal normalization — 2026-10-12T04:39:16Z
[Current English review](references/device_evidence/remote/A-REMOTE-008/CONTROLLED_TIME_NORMALIZATION_REVIEW.md): owner-authorized app-descriptor .time-only normalization PASS, raw preserved/hashed and complete normalized output identical. Command counts reconciled: CMake1449 vs actual SCons1549 (1449−4 scaffolding+104 bootloader,12 new sources+92 extra contexts), both A/B unchanged;1457 actual unique files/1531 C/C++ contexts. First additional PP difference is esp_bootloader_desc.date_time (__TIME__/__DATE__), observed in application and bootloader contexts; outside app-only allowance, not normalized. Mandatory owner additional-difference STOP, not attribution to component omission or source/hardware defect. All-unit/header/full-graph/link/clean-build certificate incomplete. No archive/remaining full secret scan/protocol/transfer/second-host run. A008 IN PROGRESS; INCONCLUSIVE — BUILD REPRODUCTION BLOCKED BY INTERMITTENT COMPILER PROCESS FAILURE, source-to-build UNKNOWN. A009 BLOCKED/NOT STARTED, PR14 OPEN/unmerged, originals/SDK/hardware/shared gates unchanged; historical evidence retained.

## A008 fixed-epoch first non-temporal difference — 2026-10-12T05:21:29Z
[Current experiment](references/device_evidence/remote/A-REMOTE-008/FIXED_EPOCH_FIRST_LINK_DIFFERENCE.md): epoch1791763200/2026-10-12T00:00:00Z, fresh same-physical-path A/B, identical actual1549 commands and complete environments. All3098 PP/dependency calls PASS,1549raw pairs byte-identical/no normalization, no esp_wifi_bsp dependency; exact inventory removal only. First remaining difference is application linker library order/expanded command: A libxtensa.a vs B libapp_trace.a at position0, same122library multiset, target ENV identical. Same-A variation observed; causation by component omission not established. Mandatory non-temporal STOP, no sorting or workaround, exclusion NOT VALIDATED. A clean build exit1 SCons _Null/str TypeError after ELF/map, no ICE/no complete BIN; B clean build not run after stop. No bundle/remaining secret scan/protocol/transfer/second-host. A008 IN PROGRESS; INCONCLUSIVE — BUILD REPRODUCTION BLOCKED BY INTERMITTENT COMPILER PROCESS FAILURE/source-to-build UNKNOWN. A009 BLOCKED/NOT STARTED, PR14 OPEN/unmerged; originals/tools/hardware/shared contracts/gate unchanged.


## A008 private Dell readiness — 2026-10-12T15:46:33.352221+00:00
[Owner acceptance](references/A008_DELL_OWNER_ACCEPTANCE_2026-10-12.md) accepts full esp_wifi_bsp transfer exclusion with residual hobby-beta uncertainty, superseding prior metadata/timestamp/link-order preparation stops. [Project scope](references/PROJECT_HOBBY_BETA_SCOPE_2026-10-12.md); [ready record](references/device_evidence/remote/A-REMOTE-008/DELL_BUNDLE_READY.md). Private offline archive locally verified: 1449621481 bytes/29832 files, SHA-2568ef30f580b8d27280863679abc9780ec94afe5b8b100f06767d0f6de9683887d; archive/source/contents not published. Complete scoped secret scan/private review PASS, no recognized operational secret in retained effective inputs. Fresh extraction/all SHA entries/PS syntax/VerifyOnly/isolated configuration/two smoke compiles PASS; Dell20+20+three clean builds NOT RUN, no transfer/hardware. Owner-accepted exclusion is not an industrial no-influence certificate; prior evidence and observed library multiset/order variation retained.

A008 IN PROGRESS; INCONCLUSIVE — BUILD REPRODUCTION BLOCKED BY INTERMITTENT COMPILER PROCESS FAILURE, source-to-build UNKNOWN. A009 BLOCKED / NOT STARTED, same PR14 OPEN/unmerged. Originals/installed tools/TUNER unchanged; CCM frozen/Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED/O01–O17 OPEN/common gate OPEN/NOT PASSED, backend/migration/hardware gaps and ADC FAIL/rollback PENDING retained. No task dispatch or merge.


## A008 Dell practical closure — 2026-10-12T17:57:51.204673+00:00

[Dell review](reports/A-REMOTE-008_DELL_REVIEW.md): **PASS — PRACTICAL DELL SOURCE-TO-BUILD REPRODUCTION (HOBBY / PUBLIC-BETA SCOPE)**. A008 execution/review DONE / READY FOR OWNER REVIEW; previous current INCONCLUSIVE/build-blocked disposition superseded, historical evidence retained. Verified results archive1,597,657,193bytes/SHA792432a5581ce92a2ddec35c4b2d6f9deec57ef03593912c34aa3a7aa6c593ec. Dell1configuration+20frozen+20source+3serial -j1 clean builds PASS,0FAIL/ICE;44 actual records/log hashes/40objects/all build artifacts independently verified.1,613 source files each/effective historical+Dell configurations/partitions identical;895 selected archive members equal. BIN/ELF/map/bootloader raw bytes differ, build3 app256bytes smaller; bounded identical pre-link code/relocations and same providers support link-layout/relaxation variation, not source/configuration change. Historical BIN byte identity and runtime semantic equivalence NOT DEMONSTRATED. Ryzen classified intermittent host/environment/compiler-process failure, not a reproducible source defect in these tests; exact cause UNKNOWN, no proven hardware fault.

Recommend owner acceptance and documentation-only PR14 merge after review; PR stays OPEN/unmerged. A009 BLOCKED / NOT STARTED, no automatic task. No source/archive/SDK/toolchain/artifact/private-path publication or production/hardware/partition changes. CCM frozen, Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED, O01–O17/common gate OPEN/NOT PASSED; backend/migration/runtime/ADC/rollback gaps retained. Historical scope records remain byte-unchanged; current task status is this new review, not prior snapshot.


## A008 final owner acceptance — 2026-10-12T18:08:36.987171+00:00

**A-REMOTE-008: DONE / OWNER ACCEPTED. PASS — PRACTICAL DELL SOURCE-TO-BUILD REPRODUCTION (HOBBY / PUBLIC-BETA SCOPE).**

The owner accepts the reviewed evidence at the previously approved practical hobby/public-beta assurance level. Dell passed 20/20 frozen-input compilations, 20/20 original-source compilations and 3/3 serial clean builds; configuration also passed. No reproducible source defect was demonstrated. Ryzen experienced an intermittent host/environment/compiler-process failure; its exact cause remains UNKNOWN, with no proven hardware fault.

The three Dell clean-build artifacts are not byte-identical. Reproducible byte-identical builds and exact historical installed/A-006 runtime equivalence remain UNPROVEN, but are not blockers for the owner-approved hobby/public-beta level. All historical investigation, negative results, temporal/layout observations, Dell evidence and proportional limitations remain preserved. This acceptance does not claim hardware/runtime, persistence, migration or production qualification.

A-REMOTE-009 remains BLOCKED / NOT STARTED; this acceptance creates no assignment or execution authority. No hardware access, upload/flash, partition change, production-code change or private source/bundle publication. CCM1.1.0 remains frozen; historical CCM1.0.0 unchanged. Native API remains UNAPPROVED / UNFROZEN / NOT IMPLEMENTED; O01–O17 and the common gate remain OPEN / NOT PASSED. TUNER and all existing hardware, backend, ADC and rollback limitations remain unchanged.

[Owner acceptance](references/A008_FINAL_OWNER_ACCEPTANCE_2026-10-12.md); normal [PR14 merge](https://github.com/OviOneKenoby/remote_tuner_system/commit/36b819e79b6f6385e9e5abf380ffcb4cc412f0dc) of reviewed head `0f90de668b4b36c67b1f3ad8d572614a6a8affdb`. This current status supersedes prior pending-review or INCONCLUSIVE labels without altering their historical evidence. A009 proposal only: approved 64KiB layout preparation and bounded USB/ROM recovery test/rollback protocol; no assignment or execution.


## A009 preparation ready for owner review — 2026-10-12T18:35:41.124995+00:00
**PASS — HOST LAYOUT/RECOVERY PREPARATION; HARDWARE NOT RUN.** [Report](reports/A-REMOTE-009_PREPARATION.md), [assignment](tasks/A-REMOTE-009.md), [unexecuted owner protocol](protocols/A-REMOTE-009_USB_ROM_RECOVERY.md). Add remote_ctl64KiB at0xE20000; six baseline records byte-identical, all offsets/sizes/factory/both3MiB OTA slots preserved; bounds/alignment/no-overlap PASS. Clean -j1 build PASS, firmware2485584bytes/headroom660144bytes per OTA slot. Only disposable layout candidate; no production source/tool/hardware change. PR15 OPEN/unmerged. A009 preparation complete; hardware phase BLOCKED pending explicit owner approval and fresh full-backup preflight. A008 DONE/OWNER ACCEPTED unchanged; A010 NOT STARTED; no backend/API/TUNER/CCM changes. Native unapproved; O01–O17/common gate OPEN/NOT PASSED. Hardware/USB-recovery/migration/backend qualification NOT RUN.


## A009 accepted preparation and read-only preflight — 2026-10-12T19:36:49.377474+00:00
Preparation OWNER ACCEPTED; **PASS — READ-ONLY HARDWARE PREFLIGHT; PERSISTENT OPERATIONS NOT AUTHORIZED**. [Report](reports/A-REMOTE-009_READ_ONLY_PREFLIGHT.md), [owner scope](references/A009_READ_ONLY_PREFLIGHT_OWNER_AUTHORIZATION_2026-10-12.md). Exact prior device privately identified; ROM USB/no JTAG, ESP32-S3revision0.2/physical16MiB/securitydisabled confirmed. Two16777216-byte full reads byte/SHA-identical, structurally valid; backup SHA `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`. Independent table byte-identical to A007; target65536bytes allFF; installed factory image byte-identical to A006/A007, source/runtime equivalence not claimed. Both backups privately preserved locally; external copy deferred by owner and mandatory before any future write. Stop in ROM/stub at first-write checkpoint: no normal app return reset, zero persistent write/erase/upload/NVS/rollback commands. Table-only0x8000 candidate remains proposed/not executed, no hardware write approval or PR merge. PR15 OPEN/unmerged; A010 NOT STARTED/A008 accepted/CCM frozen/Native unapproved/O01–O17/common gate OPEN.


## A009 table-only hardware result — 2026-10-12T20:24:27.882825+00:00
A009 backup-bound table-only operation **PASS / READY FOR OWNER REVIEW**, [report](reports/A-REMOTE-009_TABLE_ONLY_HARDWARE_VALIDATION.md), [owner scope](references/A009_TABLE_ONLY_WRITE_OWNER_AUTHORIZATION_2026-10-12.md). One table-sector write0x8000–0x8FFF/exit0; readback candidate+FF exact, independent seven-entry decode, six old records/both3MiB OTA slots preserved. Target65536FF; full pre-reboot16MiB read byte-identical outside table sector. Same factory boots, passive logs clean, owner confirms normal UI/configuration without mutation. Rollback not required/not executed; ROM restoration write remains untested. Local backup rehashed; separate-storage copy size/hash OWNER VERIFIED. PR15 OPEN/unmerged; A009 owner acceptance pending, no A010/backend/API/TUNER/CCM change. A008 accepted, Native unapproved/O01–O17/common gate OPEN. Earlier persistent-NOT-AUTHORIZED snapshots superseded only for this completed exact write; no ongoing write authorization.


## A009 final owner acceptance — 2026-10-12T20:29:15.774597+00:00

**A-REMOTE-009: DONE / OWNER ACCEPTED. PASS at the approved practical hobby/public-beta assurance level.**

Installed physical state from accepted evidence: seven partition entries; `remote_ctl`, data/nvs, offset `0xE20000`, size `0x10000` (64 KiB), flags0. All six earlier entries, factory at0x10000 and both3MiB OTA slots remain unchanged. The new region was read as65536bytes of0xFF after table writing and confirmed in the full pre-reboot read; it remains erased/unused in the accepted state, no backend initialized. Existing factory firmware is unchanged and booted normally; owner confirmed ordinary display/UI and existing observable configuration without mutation.

Preserve preparation, read-only preflight, complete16MiB backup identity, independent sector readback/decode, and full before-reboot preservation evidence: every byte outside0x8000–0x8FFF was identical to the verified backup,50 changed bytes all inside the table sector. One authorized table-only command, no firmware upload or other-region write. ROM/USB download/read access remains available without JTAG; an actual restoration write was NOT physically exercised. No rollback was required/executed. Normal firmware housekeeping after boot is not a claim of globally frozen flash bytes.

Primary recovery backup16777216bytes/SHA256 `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8` retained privately; owner separately verified an Orange Pi copy with the same size/hash. Original4096-byte0x8000–0x8FFF sector retained privately, SHA256 `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46`. Absolute private paths/backup contents/identifiers remain unpublished.

No new hardware access/write/recovery test, firmware/source/tool/NVS/remote_ctl/TUNER/common-API change occurred during acceptance. A010 remains NOT ASSIGNED / NOT STARTED. A008 stays DONE/OWNER ACCEPTED with byte-reproducibility/historical runtime-equivalence unproven and exact Ryzen compiler-process failure cause UNKNOWN. CCM1.1.0 frozen/historical1.0.0 unchanged, Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; O01–O17/common gate OPEN/NOT PASSED. Backend/durability/G1a/migration limits remain separate.

[Owner acceptance](references/A009_FINAL_OWNER_ACCEPTANCE_2026-10-12.md); normal PR15 merge `9b12c9b2642fcba3e9c7a9f3c3171e831430f108`, reviewed head `52f99887cb1a88772bed98f7bc7cfb60529de4e6`. A010 proposal only: minimum private remote_ctl persistence backend with focused host interruption/error tests and separate hardware authorization; not assigned or executed.


## A010 private implementation assigned — 2026-10-12
[Task](tasks/A-REMOTE-010.md), [owner scope](references/A010_PRIVATE_IMPLEMENTATION_OWNER_AUTHORIZATION_2026-10-12.md). Owner authorizes A-REMOTE-010 assignment and private implementation, focused host tests and a clean serial build at practical hobby/public-beta assurance. Dedicated installed remote_ctl data/nvs partition only,0xE20000/0x10000. No hardware access, flash/write/erase, default NVS migration, partition-layout change, common API, TUNER, MQTT/SmartThings/UI, A011 or reopening A008/A009. Stop before any future hardware write and request explicit approval. Publish only English sanitized reports/test results/hashes/protocol in new OPEN/unmerged PR; private source/secrets/payloads/full images remain unpublished. A008/A009 accepted; CCM frozen/Native unapproved/O01–O17/common gate OPEN.

## A010 private backend ready for owner review — 2026-10-13T03:35:07.084328+00:00
**PASS — PRIVATE IMPLEMENTATION / HOST VERIFIED / CLEAN BUILD; HARDWARE NOT RUN.** [Report](reports/A-REMOTE-010_PRIVATE_BACKEND.md), [task](tasks/A-REMOTE-010.md), [evidence](references/device_evidence/remote/A-REMOTE-010/RESULT.json), [unexecuted protocol](protocols/A-REMOTE-010_HARDWARE_VALIDATION.md). Private schema-v1 `remote_ctl` backend uses explicit initialization, durable generation fence → CRC record → authority root ordering, three slots, one authoritative 4096-byte-max envelope, strict UInt64 next-generation/no-reuse, and fail-closed corruption/ambiguity handling. Host tests 14/14 PASS; clean serial target build PASS; firmware 2,496,400 bytes / 649,328 bytes OTA headroom; generated table exact A-009. No boot caller, source/artifact/secret publication, hardware access/write/erase/upload, common API/TUNER change, or A011. Physical NVS behavior NOT RUN; exact diagnostic activation and owner write approval remain required. PR16 OPEN/unmerged; A010 READY FOR OWNER REVIEW. CCM1.1.0 frozen, Native unapproved, O01–O17/common gate OPEN.

## A010 diagnostic candidate ready for owner review — 2026-10-13T06:43:09.576743+00:00
**PASS — DIAGNOSTIC CANDIDATE IMPLEMENTED / HOST VERIFIED / CLEAN BUILD; HARDWARE NOT RUN.** [Report](reports/A-REMOTE-010_DIAGNOSTIC_CANDIDATE.md), [task](tasks/A-REMOTE-010.md), [evidence](references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_RESULT.json), [protocol](protocols/A-REMOTE-010_HARDWARE_VALIDATION.md), [owner scope](references/A010_DIAGNOSTIC_CONTINUATION_OWNER_AUTHORIZATION_2026-10-13.md). Normal build diagnostic disabled; candidate `remote01_a010_diag` only. Exact `!A010` UART commands, per-mutation confirmation tokens and fixed remote_ctl identity guard. Boot persistence activity NONE. Tests 28/28 PASS; adapter review PASS; clean build PASS; firmware 2,503,936 bytes / 641,792 bytes OTA headroom; table exact A009. No hardware/source/artifact/payload/secret publication, no upload/write/erase, no TUNER/common API/layout change. PR16 OPEN/unmerged; A010 continues awaiting exact hardware decision; A011 NOT STARTED; CCM frozen, Native unapproved, O01–O17/common gate OPEN.
