# Exact PM task template

```markdown
# <task-id>: <title>
- Owner: <REMOTE//01 / TUNER//01 / PM>
- State: <DRAFT / ASSIGNED / BLOCKED / DONE>
- Coordination input commit: <full hash>
- Objective: <observable outcome>
- Baseline: <repository, branch, full commit, firmware version, dirty-tree policy>
- Required references: <paths and revisions/hashes>
- Dependencies: <task/decision IDs and their required states>
- Allowed scope: <files/subsystem/device>
- Excluded scope: <boundaries>
- Shared-contract guard: <frozen CCM 1.0.0; API status; approved decision IDs or NONE>
- Acceptance criteria: <specific evidence required for completion>
- Verification: <required checks; distinguish build and hardware>
- Stop/report conditions: <missing evidence, baseline mismatch, contract ambiguity>
- Required outputs: <changes, logs, device changelog, complete archived/latest handoff>
- PM assignment evidence: <date and published assignment reference>
```
