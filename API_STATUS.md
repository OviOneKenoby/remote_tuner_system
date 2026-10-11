# Shared contract status
Updated: 2026-10-11T17:37:47Z
Authority: D-001 through D-004; historical starting facts retained. Recovered artifact/provenance is indexed in references/device_evidence/remote/A-REMOTE-001/INDEX.md; no new approval or conformance claim.

| Contract | Version | Approval | Freeze | Implementation |
| --- | --- | --- | --- | --- |
| Common Control Model (CCM) | 1.0.0 | OWNER APPROVED | FROZEN | Current device conformance NOT VERIFIED here |
| TUNER Native API | v1 | UNAPPROVED | UNFROZEN | NOT IMPLEMENTED |

Current TUNER final baseline: v1.1.11, main/tag/merge `5fb92c95d228d744d1182ae3956e850c5be2f277`; executable source `124e84801b06f9e07764dabc3985a573dffaff3b`, build_git_id `124e84801b06`, explicit `esp32-lwip-psram`. [Exact artifact/accepted hardware scope and limits](reports/TUNER_V1_1_11_RECONCILIATION.md); D-005. Initial audited `371cdebce7ba2648ea71636d5bdb5d738b42e680` /1.1.0 is historical D-003, not current state. No new conformance or Native approval.
Common phase: Phase A contract reconciliation + TUNER correctness/control-state foundation.

## Reference register
| Reference | Required artifact | Available here |
| --- | --- | --- |
| REF-CCM | Actual owner-approved frozen CCM 1.0.0 and original approval record | YES; recovered frozen artifact SHA-256 7a46f9fffe706476de458aac078d0af1c94844df339248d3f9f4b5cf033011d7 and original approval excerpt in REMOTE A-001 evidence; timestamp/signature limits retained |
| REF-API | Native candidate with revision/hash | YES; pre-audit candidate.1, historical/unapproved; reconciled version not yet available |
| REF-AUDIT | TUNER audit for exact baseline | YES; supplied 2026-10-07 audit and companion records, hashes in references/INDEX.md |
| REF-HANDOFF | Canonical cross-device requirements and O01-O17 | YES; supplied 2026-10-07 handoff, normative obligations not implementation |
| REF-REMOTE | Current baseline, decisions/changelog and evidence | YES for inspected Git-less baseline/source inventory and reports/A-REMOTE-001.md; current artifact/source/flashed correspondence and rollback residency remain UNKNOWN/PENDING |

Imported originals are read-only snapshots under references/starter_2026-10-08/. Candidate headers and earlier transport/asset preferences do not override current owner-approved status or the later canonical handoff.

## Change gate
Proposal ID -> exact diff -> REMOTE review -> TUNER review -> explicit owner approval evidence -> approved revision -> scoped implementation -> verification.
O01-O17 are OPEN. PM assignments authorize only their exact task scope, never shared-contract approval. A-001 inspections are complete; A-TUNER-002 assigns four bounded internal correctness guards, A-REMOTE-002 design only. No Native implementation is assigned.


## Current REMOTE qualification boundary - 2026-10-11
A003 execution complete, production qualification FAIL/BLOCKED. A004 execution complete, conditional host delivery reviewed, READY FOR REVIEW / production integration BLOCKED. Concrete root/ordered-record backend and physical capacity unqualified; hardware NOT RUN. D1-D5 unassigned. [PM review](reports/A-PM-003_RECONCILIATION.md). Earlier assignment paragraphs retain historical dated scope only.

## D-006 owner approval and CCM1.1.0 publication - 2026-10-11
P-REMOTE-V1-001 exact PR11 head03c1be0b34df6ff9904cdaf78a0f5de79fd7ac0c is OWNER APPROVED by [exact scope](references/P_REMOTE_V1_001_OWNER_APPROVAL_2026-10-11.md). Current new revision [CCM1.1.0](references/CCM_1_1_0.md) OWNER APPROVED/FROZEN; [publication hashes](references/CCM_1_1_0_PUBLICATION.json). Supersedes only the prior pending-approval/current1.0.0 pointer for this approved REMOTE persistence threat delta; historical1.0.0/proposal/reviews/old task verdicts remain unchanged. G1a REQUIRED, G1b OUTSIDE for intentional complete coherent restoration. This is contract publication, not implementation or device acceptance. Capacity48KiB conditional recommendation; actual capacity/ordering/durability/migration unqualified. Core/NVS/partition/firmware/Native/TUNER/hardware untouched. Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED, O01-O17 OPEN, common gate OPEN/NOT PASSED;006-009/D1-D5 unassigned. No automatic task execution.

## A-REMOTE-006 result - 2026-10-11
[Read-only report](reports/A-REMOTE-006_FLASH_LAYOUT.md) delivered under assignment `81d7d2f4d2c3d7625d6c6f5618785ffd90b93940`; result requires review in separate OPEN PR, acceptance/deployment BLOCKED. Effective customCSV/currentBIN byte-identical; configured16MiB tail admits64/48KiB at0xE20000 with zero OTA shrink. Prefer64 CONDITIONAL; slot headroom659904 bytes20.9778%. Physical flash/source-flashed identity UNKNOWN; automatic rollback disabled; table-sector interruption/recovery unresolved. Dedicated948-entry bound vs conservative1222;64 margin1068/794,48 margin564/290. Wi-Fi defaultNVS preserved by addressing, actual physical UNKNOWN. No device edits/operations/build/release/merge;4036-file workspace unchanged. CCM1.1.0 frozen unchanged; Native unapproved; O01-O17/gate OPEN; ADC historical FAIL/rollback residency PENDING; A005 BLOCKED. Next007 design/host recommendation only, not assigned.
