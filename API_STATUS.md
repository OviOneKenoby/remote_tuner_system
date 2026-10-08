# Shared contract status

Snapshot: 2026-10-08. Authority: explicit owner-provided starting facts; source artifacts pending.

| Contract | Version | Approval | Freeze | Implementation |
| --- | --- | --- | --- | --- |
| Common Control Model (CCM) | 1.0.0 | OWNER APPROVED | FROZEN | Device conformance NOT VERIFIED here |
| TUNER Native API | v1 | UNAPPROVED | UNFROZEN | NOT IMPLEMENTED |

TUNER audited baseline: `main`, `371cdebce7ba2648ea71636d5bdb5d738b42e680`, firmware `1.1.0`.
Common phase: **Phase A contract reconciliation + TUNER correctness/control-state foundation**.

## Reference register

| Reference | Required artifact | Available here |
| --- | --- | --- |
| REF-CCM | Owner-approved frozen CCM 1.0.0 and approval evidence | NO |
| REF-API | Native API v1 candidate with revision/hash | NO |
| REF-AUDIT | TUNER audit for the exact baseline | NO |
| REF-REMOTE | Current REMOTE baseline, decisions and changelog | NO |

Historical candidate.4 CCM or pre-audit API files, if supplied later, are historical references. Their header status must not override this current status. No endpoints or schemas are invented in this starter.

## Change gate

Proposal ID -> exact diff -> REMOTE review -> TUNER review -> explicit owner approval evidence -> approved revision -> scoped implementation -> verification. Record each transition in DECISION_REGISTER. Update status only with supporting evidence and responsible review. Approval alone never proves implementation or device conformance.
