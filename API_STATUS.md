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
