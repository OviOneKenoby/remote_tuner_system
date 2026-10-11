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
