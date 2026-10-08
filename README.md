# REMOTE//01 + TUNER//01 coordination

Starter coordination repository, prepared 2026-10-08. It stores tasks, decisions and evidence references; firmware remains in the separate REMOTE and TUNER repositories.

## Structure

```text
REMOTE-TUNER-SYSTEM/
  README.md
  AGENTS.md
  PROJECT_SYNC.md
  DECISION_REGISTER.md
  API_STATUS.md
  CHANGELOG.md
  PACKAGE_VERIFICATION.md
  MANUAL_SETUP.md
  prompts/PROJECT_MANAGER_BOOTSTRAP.md
  prompts/CODEX_TASK_FOOTER.md
  templates/HANDOFF_TEMPLATE.md
  templates/TASK_TEMPLATE.md
  handoffs/REMOTE_LATEST.md
  handoffs/TUNER_LATEST.md
  archive/README.md
  archive/remote/README.md
  archive/tuner/README.md
  references/README.md
  SHA256SUMS.txt
```

## Preserved starting facts

- CCM 1.0.0: **OWNER APPROVED / FROZEN**.
- TUNER Native API v1: **UNAPPROVED / UNFROZEN / NOT IMPLEMENTED**.
- Current TUNER audited baseline: branch `main`, commit `371cdebce7ba2648ea71636d5bdb5d738b42e680`, firmware `1.1.0`.
- Common phase: **Phase A contract reconciliation + TUNER correctness/control-state foundation**.

These facts were explicitly supplied by the owner for this package. The underlying approved CCM, audit and firmware checkout were not supplied here and have not been independently inspected. An audited baseline does not prove the current checkout is still at that commit, that a build passed, or that hardware passed. REMOTE baseline and both devices' current hardware status are unknown.

## Workflow and responsibilities

1. Project Manager reads PROJECT_SYNC, API_STATUS, DECISION_REGISTER and both latest handoffs from the same recorded coordination commit. PM defines separate tasks using templates/TASK_TEMPLATE.md: outcome, dependencies, limits and acceptance gate.
2. REMOTE//01 and TUNER//01 each inspect their real device files and evidence, then translate their own PM task into a precise Codex prompt. They must not invent missing details or expand work to the other device.
3. Codex executes the authorized device task, records changes and verification, updates the device changelog, archives the previous latest handoff and publishes a complete new handoff using the exact template. Include prompts/CODEX_TASK_FOOTER.md in every task prompt.
4. The specialized chat reviews the result. PM reads both published handoffs, evaluates dependencies and the common gate, records decisions and updates PROJECT_SYNC. Completion of one device task does not close the shared gate.
5. Owner approvals are recorded with exact scope and a durable evidence link. PM coordinates; PM cannot substitute for the owner on shared-contract approval.

## Contract protection

CCM 1.0.0 remains frozen. No PM, chat or Codex actor may unilaterally change its semantics, version or approval status. Native API v1 remains an unapproved proposal and must not be represented as implemented. Fields, endpoints, commands, state meanings, errors, timing, event behavior and compatibility obligations affecting both devices are shared-contract changes.

For a proposed change: record a proposal in DECISION_REGISTER, attach the exact diff and impact on both devices, obtain both device reviews, obtain explicit owner approval, and only then schedule implementation against the approved revision. A new CCM revision requires explicit owner authorization to supersede the frozen version; never silently rewrite 1.0.0. Record proposal, approval, implementation and verification as separate states. An API implementation task must have an approved contract revision before execution.

## Publication discipline

Pull/fetch the current coordination state before work; record its commit in every task/handoff. Use separate branches or checkouts for concurrent writers. REMOTE owns its latest handoff/archive; TUNER owns its own; PM owns PROJECT_SYNC and decision/status coordination. Cross-role changes require review by the responsible role. Do not force-push or overwrite another writer's updates. Resolve conflicts by rereading evidence, never by choosing a side blindly.

Archive the previous complete handoff before replacement as `archive/<device>/YYYY-MM-DDTHHMMSSZ_<task-id>_<handoff-id>.md`; use unique IDs and never overwrite archives. Preserve old unknowns and fixes in changelogs. Firmware commit and coordination commit are separate: handoff commit means the firmware commit, and the coordination publication commit is recorded in the publication/PR message to avoid self-reference.

## Access and automation

This ZIP does not publish a repository, connect accounts, grant filesystem access, dispatch tasks or install a scheduler. Shared files provide durable handoff; each actor must be given access and invoked. A chat without repository access needs the current files uploaded or pasted by the owner. Full automatic dispatch requires a separately configured runner/integration with access, scheduling and conflict handling. Until then, use the manual cycle in MANUAL_SETUP.md. Never treat a stale uploaded copy as live repository state.

Read MANUAL_SETUP.md for the exact initialization and publication steps.
