# Exact handoff template

Copy the block unchanged, retaining every heading. Use explicit UNKNOWN/NONE/NOT RUN with reasons. Use UTC timestamps and unique handoff IDs. No claim of verification without evidence.

```markdown
# <REMOTE//01 or TUNER//01> handoff

## Metadata
- Handoff ID: <unique-id>
- Updated (UTC): <timestamp>
- Task ID: <PM task-id or NONE>
- Status: <NOT STARTED / IN PROGRESS / BLOCKED / READY FOR REVIEW / ACCEPTED>
- Prepared by: <actor>
- Coordination input commit: <full commit or UNKNOWN>

## Milestone
<assigned outcome and acceptance criteria; achieved/not achieved>

## Baseline
- Device repository: <path/URL or UNKNOWN>
- Branch: <branch or UNKNOWN>
- Firmware baseline commit: <full hash or UNKNOWN>
- Firmware version: <version or UNKNOWN>
- Working tree at start: <clean/dirty, relevant differences or NOT INSPECTED>
- Contract references: <CCM revision, API candidate revision, decision IDs>

## Changes
<actual changes, paths and rationale; NONE if none>

## Verification
| Check | Command/procedure | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| <check> | <exact command/procedure> | <tool versions/board/config> | <PASS/FAIL/NOT RUN> | <log path or immutable link> |

## Remaining unknowns
<unverified facts and how to resolve them>

## Shared-contract impact
- CCM 1.0.0: <NO CHANGE with explanation, or proposal ID; never silently edit>
- TUNER Native API v1: <NO CHANGE with explanation, or proposal ID>
- Other device impact: <assessment/evidence or UNKNOWN>
- Approval evidence: <decision ID and approved scope, or NONE>

## Blockers
<blocker, responsible actor, required input; NONE if none>

## PM decision required
<precise decision and options; NONE if none; shared changes require owner approval>

## Recommended next task
<scoped outcome, dependency and gate; recommendation is not assignment>

## Commit
- Firmware result commit(s): <full hashes or NONE; distinguish uncommitted work>
- Device changelog: <path/revision or NONE>
- Coordination publication: <branch/PR; final coordination hash in publication message>
- Previous handoff archive: <path or NONE for first handoff>

## Hardware status
- Physical device tested: <YES/NO>
- Board / hardware configuration: <exact reference or UNKNOWN>
- Procedure and result: <evidence or NOT RUN>
- Firmware actually flashed: <full commit/version or UNKNOWN>
- Build-only or simulated checks: <list; do not claim physical validation>
```
