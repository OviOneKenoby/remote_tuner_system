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
