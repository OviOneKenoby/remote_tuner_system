# Shared contract status
Updated: 2026-10-08T13:55:34Z
Authority: D-001 through D-004 and references/INDEX.md; original approved-model provenance still pending.

| Contract | Version | Approval | Freeze | Implementation |
| --- | --- | --- | --- | --- |
| Common Control Model (CCM) | 1.0.0 | OWNER APPROVED | FROZEN | Current device conformance NOT VERIFIED here |
| TUNER Native API | v1 | UNAPPROVED | UNFROZEN | NOT IMPLEMENTED |

TUNER audited baseline: main / 371cdebce7ba2648ea71636d5bdb5d738b42e680, firmware 1.1.0. PM independently confirmed the current remote main ref and config version; actual local checkout/build/flashed artifact/runtime margins remain unverified.
Common phase: Phase A contract reconciliation + TUNER correctness/control-state foundation.

## Reference register
| Reference | Required artifact | Available here |
| --- | --- | --- |
| REF-CCM | Actual owner-approved frozen CCM 1.0.0 and original approval record | NO; historical candidate.4 and later freeze records available |
| REF-API | Native candidate with revision/hash | YES; pre-audit candidate.1, historical/unapproved; reconciled version not yet available |
| REF-AUDIT | TUNER audit for exact baseline | YES; supplied 2026-10-07 audit and companion records, hashes in references/INDEX.md |
| REF-HANDOFF | Canonical cross-device requirements and O01-O17 | YES; supplied 2026-10-07 handoff, normative obligations not implementation |
| REF-REMOTE | Current baseline, decisions/changelog and evidence | PARTIAL; supplied historical decisions/architecture/changelog through 2026-10-06; live baseline/latest results missing |

Imported originals are read-only snapshots under references/starter_2026-10-08/. Candidate headers and earlier transport/asset preferences do not override current owner-approved status or the later canonical handoff.

## Change gate
Proposal ID -> exact diff -> REMOTE review -> TUNER review -> explicit owner approval evidence -> approved revision -> scoped implementation -> verification.
O01-O17 are OPEN. PM task assignments authorize only their stated inspection/documentation scope, never shared-contract approval. No Native implementation is assigned.
