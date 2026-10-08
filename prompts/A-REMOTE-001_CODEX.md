# Codex execution instruction ? A-REMOTE-001

Prepared 2026-10-08 from coordination commit `769c4dc1f50acebbf855b06d4bcf9cfc5eba7e16`.
Publication of this prompt is not task completion or API approval.

Execute A-REMOTE-001 in `C:\Users\RYZEN\Documents\REMOTE01\Code`.
Coordination checkout: `C:\Users\RYZEN\Documents\REMOTE-TUNER-SYSTEM\remote_tuner_system`.
Before starting, fetch current coordination main, read the live assignment and
all required references at one recorded revision. Preserve local work; use a
separate branch/worktree. The checkout's working files may lag origin/main;
read the selected revision or its isolated worktree, not stale main files.
If the live assignment differs, reconcile its scope before execution.
Record the actual execution-input commit; the PM planning hash is not it.
No build, upload or firmware modification is authorized. Recommendations are
not approval; all remaining contract gates stay open. Follow the exact task
below and append its evidence-backed report/handoff under the stated rules.

## Assigned task text at the preparation revision

# A-REMOTE-001: Recover the live baseline and reconcile the Native candidate with frozen CCM
- Owner: REMOTE//01
- State: ASSIGNED
- Coordination input commit: dd63c07e485218dfc34ceb6a8855c8a929b4ae89
- Objective: Return a source-backed REMOTE baseline, exact frozen-model provenance, bidirectional minimum-Native mapping and implementation prerequisites without changing firmware.
- Baseline: Supplied snapshot identifies C:/Users/RYZEN/Documents/REMOTE01/Code with no Git metadata. Current repository/path/branch/HEAD/version/dirty state and flashed artifact are UNKNOWN; inspect the actual owner-provided checkout, do not initialize Git or assume the October 6 snapshot is current.
- Required references: README.md, AGENTS.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md, both latest handoffs, templates/HANDOFF_TEMPLATE.md, prompts/CODEX_TASK_FOOTER.md, references/INDEX.md, reports/A-PM-001.md; references/starter_2026-10-08/SHARED/TUNER_REQUIREMENTS_FROM_REMOTE.md sections 20,22-24; references/starter_2026-10-08/REMOTE/COMMON_CONTROL_MODEL_V1_PRE_FREEZE_REFERENCE.md (historical candidate.4 ONLY); references/starter_2026-10-08/REMOTE/TUNER_NATIVE_API_V1_PRE_AUDIT_CANDIDATE.md; references/starter_2026-10-08/REMOTE/CONTROL_ARCHITECTURE.md; references/starter_2026-10-08/REMOTE/REMOTE01_PRODUCT_DECISIONS.md; references/starter_2026-10-08/REMOTE/REMOTE_CHANGELOG_AVAILABLE_2026-10-06.md; references/starter_2026-10-08/TUNER/TUNER_IMPLEMENTATION_AUDIT.md.
- Dependencies: A-PM-001 reference indexing locally verified; publication pending. Execute after coordination publication. Approved CCM artifact/approval provenance and current device baseline may be recovered within this task; missing evidence must not block independent inspection, but blocks dependent acceptance.
- Allowed scope: REMOTE read-only source/evidence inspection; a device-local documentation report/changelog; reports/A-REMOTE-001.md; additive byte-preserved REMOTE evidence/approved-model copies with provenance under references/device_evidence/remote/; own latest handoff/archive and append-only coordination changelog.
- Excluded scope: No executable firmware changes, new adapter/server/discovery/pairing code, dependency/toolchain/partition upgrades, upload, reset, NVS erase, unsolicited hardware test, automatic scheduling, or other-device changes. Do not edit frozen/read-only reference copies or the other device's handoff.
- Shared-contract guard: CCM 1.0.0 OWNER APPROVED/FROZEN; Native API v1 UNAPPROVED/UNFROZEN/NOT IMPLEMENTED. O01-O17 remain OPEN; proposals are not decisions. No implementation authorization or shared-contract approval is issued.
- Acceptance criteria: Identify actual checkout and recoverable artifact; locate/hash actual frozen CCM 1.0.0 and its original freeze evidence, or report them missing. Inventory Core/Mock/generic ingress and durable journal/non-reuse/effect-barrier support from current source. Map every proposed minimum capability both directions, including absence/freshness, quantization, identities/context guards, results/dedup/restart. Distinguish existing behavior from requirements/proposals; identify mismatches with owner/O decision and explicit unavailable/deferred handling. Report current sleep/rollback evidence separately from earlier accepted firmware. No real Native support badge.
- Verification: Read-only source/config/version/working-tree inspection; exact artifact hashes and documented evidence commands/results. Validate report links, complete handoff headings and archive preservation. Existing test/build/hardware evidence must retain its exact artifact/scope/date; fresh build/upload/hardware NOT REQUIRED and must not be invented.
- Stop/report conditions: Preserve dirty work; never reset/rewrite the checkout. Report baseline mismatch and use only explicitly identified source for claims. Missing source prevents that part of inspection; missing frozen artifact prevents final conformance, not source inventory. Shared ambiguity prevents dependent implementation. Missing publication access requires complete UNPUBLISHED outputs. Do not substitute old snapshots for current evidence.
- Required outputs: reports/A-REMOTE-001.md plus proposed CCM/Native mapping matrix and exact evidence index. Return recommendations for O01-O17, dependencies and questions for TUNER; do not close them. Update device changelog for actual documentation changes. Archive the previous complete handoffs/REMOTE_LATEST.md under archive/remote/ using README naming; publish a new complete latest handoff using the exact template. Add actual work to coordination CHANGELOG.md without overwriting other writers. Handoff status READY FOR REVIEW when complete, or BLOCKED with exact missing input; never self-mark common gate PASS.
- PM assignment evidence: 2026-10-08T13:55:34Z; this task and PROJECT_SYNC.md prepared locally by PM, pending publication, under the owner's 2026-10-08 request to assign both projects. Specialized chat translates this task into its own Codex prompt and appends the filled mandatory footer.

## Detailed task
1. Confirm the real checkout, relevant files, configuration and artifact identity. With no Git metadata, use a reproducible source inventory/checksum manifest and explicit path/date instead of fabricating a commit.
2. Recover the real frozen CCM and freeze record. The supplied candidate.4 semantics are historical reference; do not rename/promote that file into the approved artifact. Report exact clause/version changes if live files conflict.
3. Inspect current Core, generic adapter ingress, HOME integration, persistence and reconnect/sleep boundaries. Earlier Core/Mock acceptance does not prove Native conformance or durable reboot recovery.
4. Reconcile the pre-audit API candidate against the October 7 TUNER audit and canonical handoff. Propose a conservative minimum: identity/compatibility/capabilities, coherent state, saved/Favorite guarded activation, explicit radio operations, absolute volume, correlated results, deliberate association and recovery. Source/station role and truthful pause remain open. Independently optional capabilities must not be enabled to fill a UI row.
5. Provide one table with common intent -> Native requirement and one with TUNER observation/result -> CCM evidence; include required proof and UNSUPPORTED/UNKNOWN where it cannot be supplied. Native counters must not become Core-owned generations.
6. List durable command-history/non-reuse/barrier prerequisites separately from last-associated-TUNER settings and artwork cache. No persistence implementation is authorized.
7. Reconcile sleep records: product register item22 was superseded by later owner policy; accepted approximately 23 mA sleep baseline is separate from the ADC optimization hardware FAIL and rollback-control hardware PENDING. Recover newer owner evidence if present; do not rerun/fix power work under this task.
8. Return source/baseline and mapping findings for PM review. Production UI, physical input integration, artwork implementation, OTA/SD and deep-sleep optimization remain outside this assignment.

## Execution and publication
The hash above is the PM planning input. Before starting, read the current coordination commit containing this assignment and record that actual execution-input hash in your handoff. Append the complete text of prompts/CODEX_TASK_FOOTER.md to the generated Codex prompt; fill the actual absolute coordination checkout path rather than inventing one. Publish on a separate device branch; reread current main and preserve concurrent updates. If merged before the other device finishes, the other task may continue after rereading: neither task depends on the other's completion. The owner still invokes the specialized chat/Codex; publication does not automatically dispatch it.

## Filled mandatory execution footer

Coordination checkout: C:\Users\RYZEN\Documents\REMOTE-TUNER-SYSTEM\remote_tuner_system
Device: REMOTE
Read AGENTS.md, README.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md and both latest handoffs. Record the coordination input commit. Confirm the real firmware baseline before editing. Missing evidence must be reported, not guessed.

Execute only the assigned task. CCM 1.0.0 is OWNER APPROVED/FROZEN. TUNER Native API v1 is UNAPPROVED/UNFROZEN/NOT IMPLEMENTED unless a later explicit owner-approved decision with evidence supersedes that status. Do not make unilateral shared-contract changes. Stop dependent implementation and submit a proposal if the task requires one.

At completion or blockage, update the device changelog and coordination CHANGELOG.md. Archive the prior handoffs/REMOTE_LATEST.md under archive/remote/ using the naming rule in README.md. Replace the latest file with the exact templates/HANDOFF_TEMPLATE.md structure, filled completely: milestone, baseline, changes, verification, remaining unknowns, shared-contract impact, blockers, PM decision required, recommended next task, commit and hardware status, plus metadata.

Separate inspected facts, planned work, implemented work, build evidence and physical hardware evidence. Include exact procedures, results and evidence references. Do not mark the common gate passed or a contract approved. Publish the handoff with the firmware commit and report the final coordination publication commit separately. Reread current coordination state before publication and resolve concurrent changes without overwriting them. If access/publication is unavailable, provide the complete handoff and report it as UNPUBLISHED.
