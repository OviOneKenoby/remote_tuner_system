# A-REMOTE-006: Read-only flash layout and dedicated storage feasibility
- Owner: REMOTE//01 / PM direct read-only analyst
- State: ASSIGNED
- Coordination input commit: 00d190a7484aa76185c47b7185c0c7f9a1854711
- Objective: Determine build-selected flash layout and dedicated64KiB/preferred or48KiB/minimum control-storage feasibility; exact proposed layout/migration/rollback evidence only.
- Baseline: REMOTE C:/Users/RYZEN/Documents/REMOTE01/Code; may be Git-less; preserve all user files, source/binary/flashed identity UNKNOWN; coordination clean input above.
- Required references: CCM1.1.0 references/CCM_1_1_0.md SHA89a566c4af0a3fb05f318efad17f663174dd90bd541cf1123b9f3e511ec76eee; D-006 approval; A005 report/source/SDK/capacity; actual local build evidence.
- Dependencies: D-006 OWNER APPROVED; A005 integrated/BLOCKED; current owner assigns this layout analysis, replacing only prospective006 host-model scope (not executed).
- Allowed scope: Read-only REMOTE config/source/build/selectedSDK; isolated temporary partition decoding/generation; coordination reports/evidence/status/changelog and result PR.
- Excluded scope: No production/Core/SDK/partition/firmware/device NVS/flash/erase/reboot/upload/hardware/release/backend/TUNER/Native changes; no automatic merge of result.
- Shared-contract guard: CCM1.1.0 FROZEN unchanged; G1a REQUIRED/G1b OUTSIDE; Native UNAPPROVED; O01-O17/gate OPEN.
- Acceptance criteria: Classified current layout/artifact-source comparison; exact64/48/current tables/headroom/capacity; proposed-only partition/config diff; staged migration power-loss matrix/downgrade cutoff; missing device evidence explicit; result PR OPEN.
- Verification: Hash analyzed artifacts/source and whole existing workspace inventory before/after; exact selected5.5.3 partition utility decode/reencode; candidate alignment/overlap/size checks; no target build unless essential in temporary copy, hardware NOT RUN.
- Stop/report conditions: Input/head mismatch, concurrent changes or missing selected-toolchain evidence; no physical flash size/installed image claims from config alone.
- Required outputs: reports/A-REMOTE-006_FLASH_LAYOUT.md; references/device_evidence/remote/A-REMOTE-006/{CURRENT_LAYOUT,CANDIDATE_LAYOUTS,MIGRATION_AND_ROLLBACK,EVIDENCE_MANIFEST}.md; hashes; task/status/changelog and separate OPEN result PR. Device changelog/handoff not replaced for read-only analysis; no invented authorization transcript.
- PM assignment evidence: 2026-10-11 direct owner request for technical read-only flash/layout analysis; this published assignment is its concise scope. No hardware/layout implementation approval.

## Read-only result disposition - 2026-10-11
- State: BLOCKED (deployment/acceptance pending owner review and missing device/recovery evidence; read-only analysis delivered).
[Report](../reports/A-REMOTE-006_FLASH_LAYOUT.md).64/48 configured-fit conditional, prefer64 without OTA shrink; physical NOT RUN, production NOT IMPLEMENTED. Original ASSIGNED fields retained as assignment history. No next device task assigned.
