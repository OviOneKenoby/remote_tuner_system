# A-REMOTE-004: Bounded storage/recovery redesign and isolated qualification
- Owner: REMOTE//01
- State: ASSIGNED
- Coordination input commit: 531aa8cd0435ed9813ab39664888992583df0d28
- Objective: Redesign bounded complete safety persistence, recovery/compaction and qualify it with a standalone fake backend;publish exact capacity/fault evidence without production integration.
- Baseline: Git-less C:/Users/RYZEN/Documents/REMOTE01/Code;A-003 result74e4f1a681cd589625aff63e91f917076cc22586 / pending PR8;actual flashed identity UNKNOWN. Preserve all concurrent work and A-003 evidence/PR.
- Required references: current rules/README/PROJECT_SYNC/API_STATUS/DECISION_REGISTER,both latest handoffs/templates/footer;frozen CCM,current Core/model/storage/SDK;A-003 complete projection/size ledger/stale-valid-anchor counterexample at pinned result.
- Dependencies: explicit owner authorization in this task;A-003 evidence available without merging PR8. No TUNER hardware/Native approval prerequisite for isolated work.
- Allowed scope: new standalone host prototype/fake backend/tests;complete narrow profile/field trace,typed records,recovery/crash-safe compaction,offline capacity measurements;own docs/changelogs/task/report/evidence/handoff/archive and publication metadata.
- Excluded scope: production Core integration,live NVS or credential access,flashing,partition/config changes,Native implementation,TUNER changes,merging PR8 or approving shared contracts/common gate.
- Shared-contract guard: CCM1.0.0 frozen;Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED;O01-O17 OPEN;common gate OPEN/NOT PASSED.
- Acceptance criteria: mandatory identities/requests/attempts/proofs/conflict/barrier/non-reuse data retained or unsupported inputs refused before handover;future proof growth reserved;bounded compaction with newest-intent guarantees stated;independent emission oracle and recovery zero emission;exact max legal encoding/peak storage including overlap/compaction/other occupancy;host facts distinct from physical assumptions;block when newest integrity unestablished.
- Verification: isolated roundtrip/max/corruption/migration/allocation/proof growth/exhaustion tests;interrupted/ambiguous write/root/compaction tests;reproduceA003counterexample;reinventory source and preserve firmware/artifacts;no target build or hardware needed.
- Stop/report conditions: missing newest-intent integrity or safe capacity => production BLOCKED,not semantic weakening;larger partition alternative docs only;no guessed hardware guarantee.
- Required outputs: this authorization, reports/A-REMOTE-004.md,reproducible evidence/tests/size/fault ledger;device+coordination changelog;byte-original prior handoff archives and complete latest;separate result PR/full hashes/results/verdict/physical guarantees.
- PM assignment evidence: direct explicit owner message2026-10-08 authorizes A-REMOTE-004 publication and execution;original message timestamp unavailable. No inferred PM or shared-contract approval.

## Exact owner authorization

Execute A-REMOTE-004 directly: bounded storage and recovery redesign, followed by isolated host qualification.

Read current coordination rules and main HEAD. Review A-REMOTE-003 at commit `74e4f1a681cd589625aff63e91f917076cc22586` / PR #8, including its complete projection, size ledger and stale-valid-anchor counterexample. Preserve that evidence and pending PR.

Authorized scope:

1. Define a minimum useful, complete supported profile. Derive exact bounds from frozen CCM and current source. Preserve mandatory identities, requests, attempts, proofs, conflict barriers and allocation/non-reuse obligations. Unsupported inputs must refuse before handover; reserve future resolution growth.
2. Design bounded typed records, recovery and crash-safe compaction. Explicitly state the backend guarantees needed to establish the newest intent. Hash chains or readback alone must not be presented as anti-rollback proof.
3. Implement only a standalone qualification prototype and fake backend. Reproduce the A-003 counterexample and test interrupted/ambiguous writes, stale roots and records, exhaustion, proof growth, allocation, compaction and migration. Use an independent emission oracle; recovery must emit nothing.
4. Measure maximum legal encoded state and peak storage footprint, including update overlap, compaction, metadata, other occupancy assumptions and resolution reserve. Assess the existing partition first. Any larger partition remains a documented alternative only.
5. Distinguish guarantees proven by host tests from assumptions requiring physical qualification. If newest-intent integrity cannot be established, preserve explicit blocking and document the reconciliation prerequisites.

No production Core integration, live NVS access, credential access, flashing, partition/configuration changes or Native API implementation. Hardware remains NOT RUN.

Publish `tasks/A-REMOTE-004.md` with this authorization, `reports/A-REMOTE-004.md`, reproducible evidence and tests, and a complete new REMOTE handoff. Archive the previous handoff byte-for-byte, preserve concurrent changes, and open a separate result PR. Return full commit hashes, test results, capacity verdict and remaining physical guarantees. Do not merge PR #8, modify TUNER, approve Native or pass the common gate.

## Mandatory execution footer (applied to this execution)

Coordination checkout: C:/Users/RYZEN/AppData/Local/Temp/remote-a004
Device: REMOTE
Read AGENTS.md, README.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md and both latest handoffs. Record the coordination input commit. Confirm the real firmware baseline before editing. Missing evidence must be reported, not guessed.

Execute only the assigned task. CCM 1.0.0 is OWNER APPROVED/FROZEN. TUNER Native API v1 is UNAPPROVED/UNFROZEN/NOT IMPLEMENTED unless a later explicit owner-approved decision with evidence supersedes that status. Do not make unilateral shared-contract changes. Stop dependent implementation and submit a proposal if the task requires one.

At completion or blockage, update the device changelog and coordination CHANGELOG.md. Archive the prior handoffs/REMOTE_LATEST.md under archive/remote/ using the naming rule in README.md. Replace the latest file with the exact templates/HANDOFF_TEMPLATE.md structure, filled completely: milestone, baseline, changes, verification, remaining unknowns, shared-contract impact, blockers, PM decision required, recommended next task, commit and hardware status, plus metadata.

Separate inspected facts, planned work, implemented work, build evidence and physical hardware evidence. Include exact procedures, results and evidence references. Do not mark the common gate passed or a contract approved. Publish the handoff with the firmware commit and report the final coordination publication commit separately. Reread current coordination state before publication and resolve concurrent changes without overwriting them. If access/publication is unavailable, provide the complete handoff and report it as UNPUBLISHED.
