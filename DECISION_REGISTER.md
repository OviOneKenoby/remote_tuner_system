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
