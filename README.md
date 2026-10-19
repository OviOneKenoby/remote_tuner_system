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
- Initial historical TUNER audited baseline: branch `main`, commit `371cdebce7ba2648ea71636d5bdb5d738b42e680`, firmware `1.1.0`.
- Common phase: **Phase A contract reconciliation + TUNER correctness/control-state foundation**.

These starting facts were supplied for the initial 2026-10-08 package; the missing-evidence description here is historical. The underlying approved CCM, audit and firmware checkout were not supplied here and have not been independently inspected. An audited baseline does not prove the current checkout is still at that commit, that a build passed, or that hardware passed. REMOTE baseline and both devices' current hardware status are unknown.

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


## Current coordination state - 2026-10-19

A-REMOTE-012 is **CLOSED / ACCEPTED**. Coordination PR [#18](https://github.com/OviOneKenoby/remote_tuner_system/pull/18) merged normally into `main` at `449d4fd7190b23d48e1374176ae69bd1c1a7038b`. TUNER `v1.1.12` is published from executable source `d112dd0bbef7d86bd22090ec75d76cad3be77677` and TUNER integration merge `4977b49756820edc149acbe1abe4d387a96aa992`; the exact 2,037,632-byte application SHA-256 is `6d7f2ebfa833bd09f287b8a7024071d736dfb2bf02356f889de94d7b980fdf6a`. REMOTE firmware and private rollback artifacts remain unchanged. Quantitative latency is owner-waived for A-REMOTE-012 and was not measured. Historical failures and evidence remain preserved. No next milestone is assigned.

## Historical coordination state - 2026-10-11
TUNER final v1.1.11 supersedes the initial baseline; [current report](reports/TUNER_V1_1_11_RECONCILIATION.md). PR7/8/9 evidence integrated; REMOTE A003 production qualification FAIL/BLOCKED and A004 conditional host PASS / production BLOCKED. [PROJECT_SYNC](PROJECT_SYNC.md), [PM review](reports/A-PM-003_RECONCILIATION.md), [evidence index](references/pm/2026-10-11/INDEX.md) record exact identity/limits. CCM/Native/O01-O17/common gate unchanged; no automatic D1/device authorization.

## D-006 owner approval and CCM1.1.0 publication - 2026-10-11
P-REMOTE-V1-001 exact PR11 head03c1be0b34df6ff9904cdaf78a0f5de79fd7ac0c is OWNER APPROVED by [exact scope](references/P_REMOTE_V1_001_OWNER_APPROVAL_2026-10-11.md). Current new revision [CCM1.1.0](references/CCM_1_1_0.md) OWNER APPROVED/FROZEN; [publication hashes](references/CCM_1_1_0_PUBLICATION.json). Supersedes only the prior pending-approval/current1.0.0 pointer for this approved REMOTE persistence threat delta; historical1.0.0/proposal/reviews/old task verdicts remain unchanged. G1a REQUIRED, G1b OUTSIDE for intentional complete coherent restoration. This is contract publication, not implementation or device acceptance. Capacity48KiB conditional recommendation; actual capacity/ordering/durability/migration unqualified. Core/NVS/partition/firmware/Native/TUNER/hardware untouched. Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED, O01-O17 OPEN, common gate OPEN/NOT PASSED;006-009/D1-D5 unassigned. No automatic task execution.


## Owner hobby-beta scope — 2026-10-12

[references/PROJECT_HOBBY_BETA_SCOPE_2026-10-12.md](references/PROJECT_HOBBY_BETA_SCOPE_2026-10-12.md) records product distribution, practical validation priorities, roadmap, Bluetooth/network coexistence and station artwork requirements. It grants no automatic task or shared-contract approval.
