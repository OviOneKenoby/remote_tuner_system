# PM follow-up authorization — 2026-10-08
Owner authorization: 2026-10-08T14:36:49Z, "engage", after review of both A-001 deliveries.

## Verified inputs
- Coordination main: 769c4dc1f50acebbf855b06d4bcf9cfc5eba7e16.
- TUNER PR #1 head: 31205936ba12ec46a4e66d1c8766cac75334f5ce.
- REMOTE PR #2 head: 2163358f2f364df768d0db2ddd4589028d4aebf2.
- Both A-001 tasks delivered inspection/documentation. Neither establishes hardware or Native acceptance.
- Coordinator merge attempt returned GitHub 403 Resource not accessible by integration. No merge/publication succeeded through that integration.
- This package is prepared and owner-authorized; it is NOT published to GitHub unless remote readback confirms publication.

## TUNER01: execute directly
You are the executing TUNER Codex session. Do not prepare another prompt.

1. Read current coordination rules and both published A-001 reports. Verify PR #1 still contains the reviewed head; integrate your documentation PR #1 using an ordinary merge with no force push. If its contents changed, review the difference before merging.
2. Publish the exact A-TUNER-002 task below at tasks/A-TUNER-002.md on a separate coordination branch/PR, citing this owner-authorized PM package. You may integrate this task document after verifying it contains only the authorized assignment. This limited administrative delegation is not permission to edit PM status/registers or the other device's files.
3. Execute A-TUNER-002 directly using your real TUNER sources. A-REMOTE-002 is not a prerequisite. If REMOTE documents are not yet merged, read the pinned REMOTE result head.
4. Preserve the other writer's changelog additions and publish both firmware and coordination result PRs. Return links, full commit hashes and test/build/hardware statuses.
5. Read and apply the mandatory footer below. Resolve the actual absolute coordination checkout path in this session before execution and record it; never invent a path.

## REMOTE01: execute directly
You are the executing REMOTE Codex session. Do not prepare another prompt.

1. Read current coordination rules and both published A-001 reports. Verify PR #2 still contains the reviewed head; integrate your documentation PR #2 using an ordinary merge with no force push. If merging after PR #1 introduces a CHANGELOG conflict, preserve both append-only entries and all original bytes of evidence/archives; do not choose one side wholesale. Review changed heads before merging.
2. Publish the exact A-REMOTE-002 task below at tasks/A-REMOTE-002.md on a separate coordination branch/PR, citing this owner-authorized PM package. You may integrate this task document after verifying it contains only the authorized assignment. This limited administrative delegation is not permission to edit PM status/registers or the other device's files.
3. Execute the A-REMOTE-002 design task directly using your real REMOTE sources. It does not authorize firmware changes and does not depend on TUNER's corrections being finished.
4. Preserve the other writer's changelog additions and publish a complete design report/evidence/handoff in a coordination PR. Return its link, full publication hash and remaining blockers.
5. Read and apply the mandatory footer below. Resolve the actual absolute coordination checkout path in this session before execution and record it; never invent a path.

If either session cannot merge/publish, report the exact blocker and deliver complete files. Do not label publication successful. Each session integrates only its own reviewed PR/task; integration of both documents does not approve the common gate or Native API.

## Exact task document: tasks/A-TUNER-002.md

# A-TUNER-002: Implement bounded correctness guards
- Owner: TUNER//01
- State: ASSIGNED
- Coordination input commit: 769c4dc1f50acebbf855b06d4bcf9cfc5eba7e16; reviewed TUNER result 31205936ba12ec46a4e66d1c8766cac75334f5ce. Record actual current execution input after documentation integration.
- Objective: Correct B01 delete parsing, B04 zero-count traversal, B06 volume underflow and B03 discovered AAC Favorite codec without adding Native functionality.
- Baseline: OviOneKenoby/ESP32-WROVER-Internet-radio, executable baseline 371cdebce7ba2648ea71636d5bdb5d738b42e680, version 1.1.0; documentation-only result 48821a6071072b77a9a023303ebf215a0577ff2e. Inspect actual HEAD and preserve dirty work; newer executable differences require reconciliation before editing affected code.
- Required references: coordination AGENTS.md, README.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md, both latest handoffs, exact templates and footer; reports/A-TUNER-001.md at 31205936ba12ec46a4e66d1c8766cac75334f5ce; reports/A-REMOTE-001.md and evidence index at 2163358f2f364df768d0db2ddd4589028d4aebf2.
- Dependencies: reviewed A-TUNER-001 findings and owner authorization on 2026-10-08 ("engage"). Publication/integration of this assignment precedes execution. A-REMOTE-002 completion is not required.
- Allowed scope: minimal changes in existing delete routes, saved-list navigation, relative volume arithmetic and discovered-to-Favorite codec propagation; focused tests/build evidence; related documentation/changelogs; own handoff/archive. Value-owned station/codec copies using existing synchronization are allowed where necessary.
- Excluded scope: no Native endpoints/adapter/discovery/pairing; no station-ID or persistence-format migration; no full B04 identity redesign; no B02/B05/B07-B11 refactor; no transport/security/CCM changes; no dependency/platform/partition/GPIO changes; no flashing/upload/reset/NVS erase; no production release or modification of REMOTE.
- Shared-contract guard: CCM 1.0.0 OWNER APPROVED/FROZEN. Native API v1 UNAPPROVED/UNFROZEN/NOT IMPLEMENTED. O01-O17 OPEN. Internal guards do not establish Native support.
- Acceptance criteria: strict full decimal delete suffix validation before conversion/narrowing, overflow and actual count checks with no mutation on rejection; zero-count next/previous guards on every reachable saved-list path; saturating volume arithmetic with zero never wrapping to full volume; persist the real codec for discovered stations on every Favorite-add path, including opaque AAC URLs. Preserve existing valid-route behavior and working decoder lifetime/metadata/Recent/BT-codec fixes. Document existing unrelated defects separately.
- Verification: meaningful deterministic tests cover empty/sign/space/junk/oversized delete suffixes, 255/256 and actual count boundaries, valid deletion/no-mutation rejected cases; zero/one/many station traversal; exhaustive relative-volume cases 0-100, especially 1-4; MP3/AAC/AAC+ Favorite codec propagation and reload where testable. Run a clean build with the existing pinned target/dependencies in an isolated checkout when needed, capture package versions, RAM/flash summary and binary SHA-256. No clean/reset of the owner's working tree. Physical playback/control tests are NOT RUN unless separately authorized; supply exact owner test steps, artifact identity and expected outcomes.
- Stop/report conditions: preserve dirty work; stop affected changes if baseline differences or codec/source ownership cannot be handled within this small scope. Build failures are blockers, not PASS. Hardware absence is an explicit validation gap; it does not justify fabricated acceptance. Do not fix unrelated findings opportunistically.
- Required outputs: firmware branch/commit/PR in the device repository; device CHANGELOG; reports/A-TUNER-002.md, test/build logs and immutable links/hashes; exact-template new TUNER handoff after byte-preserved archive; append-only coordination CHANGELOG and a coordination PR. Keep implementation/build/hardware statuses distinct. READY FOR REVIEW after passing software/build checks, with hardware PENDING / NOT RUN. Never claim full device acceptance.
- PM assignment evidence: owner authorized the coordinator's proposed bounded follow-up on 2026-10-08 at 14:36:49 UTC ("engage"). This document is the concrete scope; publication status must be stated truthfully.

## Implementation boundaries
1. Recheck the exact four call paths first. Tests must exercise behavior, not merely duplicate source expressions.
2. B01 rejects invalid input without deleting any item. Do not invent a new HTTP contract; preserve valid existing behavior and document rejection behavior.
3. B04 is limited to empty-list safety and truthful local no-op/unavailable handling. Durable identity and active-item deletion semantics remain a separate task.
4. B06 saturates before narrowing. Do not introduce a new audio policy or broader BT volume mapping.
5. B03 preserves the station's actual codec; do not infer AAC solely from a URL extension or default opaque streams to MP3.
6. A build is not physical audio proof. Deliver the exact binary hash and a short owner regression checklist; do not flash automatically.

## Exact task document: tasks/A-REMOTE-002.md

# A-REMOTE-002: Design bounded durable recovery and minimum operation support
- Owner: REMOTE//01
- State: ASSIGNED
- Coordination input commit: 769c4dc1f50acebbf855b06d4bcf9cfc5eba7e16; reviewed REMOTE result 2163358f2f364df768d0db2ddd4589028d4aebf2. Record actual current execution input after documentation integration.
- Objective: Produce an implementation-ready, bounded design for durable Core recovery and the missing catalog/reference/numeric operation support, keeping shared Native choices as proposals.
- Baseline: C:/Users/RYZEN/Documents/REMOTE01/Code, Git-less baseline captured in A-REMOTE-001; published non-.pio inventory and exact evidence snapshots at 2163358f2f364df768d0db2ddd4589028d4aebf2. Reinventory and compare relevant files; do not initialize Git or assume existing artifacts match current sources/flashed hardware.
- Required references: coordination AGENTS.md, README.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md, both latest handoffs and exact templates/footer; both A-001 reports; recovered frozen docs/COMMON_CONTROL_MODEL_V1.md SHA-256 7a46f9fffe706476de458aac078d0af1c94844df339248d3f9f4b5cf033011d7 and original approval excerpt; live Core/storage/ingress/facade/runtime code.
- Dependencies: reviewed A-REMOTE-001 findings and owner authorization on 2026-10-08 ("engage"). Publication/integration of this assignment precedes execution. TUNER correction completion is not required for design; target guarantees remain dependencies of actual execution.
- Allowed scope: source inspection and design documents, evidence index, precise future code touchpoints and acceptance/fault vectors; own documentation/changelog/handoff/archive. Evaluate storage alternatives and memory bounds using inspected facts and labeled estimates.
- Excluded scope: no executable firmware/test/config changes; no actual journal/adapter/server/pairing implementation; no build/upload/reset/NVS erase; no sleep/ADC/production-UI/artwork/OTA work; no source-control initialization; no shared protocol/CCM changes or unilateral O01-O17 closure; no TUNER edits.
- Shared-contract guard: CCM 1.0.0 OWNER APPROVED/FROZEN. Native API v1 UNAPPROVED/UNFROZEN/NOT IMPLEMENTED. O01-O17 OPEN. Recovered approval is historical provenance, not permission to change the model.
- Acceptance criteria: a concrete commit-before-dispatch/recovery design with persistent identity and lifetime ID allocation, immutable correlation, independent unresolved effect/barrier retention, bounded result pruning, atomicity/corruption/interrupted-write/failure/exhaustion/migration behavior and fail-closed recovery. Separate association/settings from effect history. Define minimal existing-CCM catalog/reference ingress and Favorite/content operation execution support and exact rational-volume domain mapping, without selecting the unresolved station role or wire transport. Supply dependency-ordered implementation slices and clear gates.
- Verification: every requirement maps to frozen CCM clauses and current source touchpoints; capacities and storage guarantees labeled measured/source-derived/estimated/unknown; explicit fault matrix and expected no-replay/barrier outcomes; validate links, hashes, exact handoff structure and unchanged source/config/artifact bytes. No fresh build or hardware test under this design task.
- Stop/report conditions: do not weaken CCM to fit existing code. A normative conflict is a proposal/blocker. Missing physical storage behavior or target guarantee remains unknown. Do not certify the unmatched BIN or rollback residency. Preserve all prior work and evidence.
- Required outputs: reports/A-REMOTE-002.md with architecture alternatives, recommended bounded design, capacity arithmetic, failure/recovery matrix, ingress/operation/numeric slice plan and exact later implementation acceptance; additive evidence; device changelog; byte-preserved previous handoff archive and complete new REMOTE handoff; append-only coordination CHANGELOG and coordination PR. READY FOR REVIEW for design only.
- PM assignment evidence: owner authorized the coordinator's proposed bounded follow-up on 2026-10-08 at 14:36:49 UTC ("engage"). This design scope issues no implementation or contract approval.

## Required design detail
1. Show the real order: reserve/commit request and unresolved effect evidence before any handover, then record delivery/outcome; explain each crash boundary.
2. Specify how torn writes, corruption, allocation exhaustion and incompatible migration block affected actions. Do not treat a new random boot epoch as ID non-reuse proof.
3. Preserve unresolved historical barriers independently of full result retention. New session/association/reset cannot erase uncertainty by default or authorize blind replay.
4. Compare at least two feasible durable-storage strategies; describe atomicity, wear/capacity and recovery assumptions. Recommend one subject to verification, without changing partitions.
5. Quantify proposed record/queue/catalog sizes from concrete representations where possible; totals are estimates until measured on the implementation.
6. Design reference/catalog ingress and the missing Favorite/content operation slices using existing frozen types. Station content/source/channel role remains O07/O14; document alternatives and dependencies.
7. Define the normalized Rational-to-TUNER integer 0..100 mapping proposal, exact representability/rejection/inverse rules and descriptor proof. UI rounding is not an adapter contract.
8. Separate REMOTE-local implementation prerequisites from TUNER-required state/context/selection/result/ledger guarantees. A journal alone cannot create remote execution proof.
9. Keep sleep rollback/artifact mismatch as a separate evidence gap. Do not begin its repair under this task.

## Mandatory footer for each session

The footer is reproduced unchanged. Fill the actual device and absolute coordination checkout path in your execution record before starting. You are already the executor; this is not an instruction to create a prompt for another session.

# Mandatory Codex task footer

Append this text to each scoped device prompt, filling the device and coordination path:

```text
Coordination checkout: <absolute-path>
Device: <REMOTE or TUNER>
Read AGENTS.md, README.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md and both latest handoffs. Record the coordination input commit. Confirm the real firmware baseline before editing. Missing evidence must be reported, not guessed.

Execute only the assigned task. CCM 1.0.0 is OWNER APPROVED/FROZEN. TUNER Native API v1 is UNAPPROVED/UNFROZEN/NOT IMPLEMENTED unless a later explicit owner-approved decision with evidence supersedes that status. Do not make unilateral shared-contract changes. Stop dependent implementation and submit a proposal if the task requires one.

At completion or blockage, update the device changelog and coordination CHANGELOG.md. Archive the prior handoffs/<DEVICE>_LATEST.md under archive/<device>/ using the naming rule in README.md. Replace the latest file with the exact templates/HANDOFF_TEMPLATE.md structure, filled completely: milestone, baseline, changes, verification, remaining unknowns, shared-contract impact, blockers, PM decision required, recommended next task, commit and hardware status, plus metadata.

Separate inspected facts, planned work, implemented work, build evidence and physical hardware evidence. Include exact procedures, results and evidence references. Do not mark the common gate passed or a contract approved. Publish the handoff with the firmware commit and report the final coordination publication commit separately. Reread current coordination state before publication and resolve concurrent changes without overwriting them. If access/publication is unavailable, provide the complete handoff and report it as UNPUBLISHED.
```


